import time
import datetime
import traceback
import multiprocessing

from pypika import Table, MySQLQuery
from multiprocessing import Process
from tqdm import tqdm

from logger import logger_core
from database.mariadb import MariaDB
from api import hometax
from mail import send_mail
from typing import List, Dict

# 

def run(_start: int,
        _end: int,
        member: list,
        message: List) -> None:
    pbar = tqdm(total=_end - _start)
    for index in tqdm(range(_start, _end)):
        response: str = str(hometax(member[index].get('사업자번호').replace('-', '')))
        pbar.update(1)
        update(response, member[index], message)


def update(status: str,
           detail: Dict,
           message: List) -> None:
    table_status = Table('사업자멤버')
    with MariaDB() as db:
        if status:

            if status == '국세청에 등록되지 않은 사업자등록번호입니다.':
                status_type = 'P'
            else:
                status_type = 'N' if '폐업자' in status else 'Y'

            if previous_status := db.fetchone(MySQLQuery\
                    .from_(table_status).select('no', 'state')\
                    .where(table_status.member_fk == detail.get('no'))):

                if previous_status.get('state') == 'Y' \
                                    and status_type == 'N':
                    message.append({
                            '이름': detail.get('store_name'),
                            '사업자번호': detail.get('biz_number'),
                            '상태': status
                    })
                db.execute(
                        MySQLQuery.update(table_status)
                            .set(table_status.상태, status)
                            .set(table_status.유형, status_type)
                            .set(table_status.reg_unixtime, int(time.time()))
                            .where(table_status.인덱스 == detail.get('no'))
                    )
            else:
                db.execute(
                            MySQLQuery
                                .into(table_status)
                                .columns(table_status.멤버,
                                         table_status.내용,
                                         table_status.상태,
                                         table_status.reg_unixtime)
                                .insert(detail.get('no'),
                                        status,
                                        status_type,
                                        int(time.time()))
                        )


def start():
    try:
        table_member = Table('wp_member')
        process_list = []
        message = multiprocessing.Manager().list()

        with MariaDB() as db:
            member: List = [_ for _ in db.fetchall(MySQLQuery.from_(table_member).select('인덱스', '사업자번호', '가게이름'))]
            total = len(member)
            for start, end in [(0, total//2), (total//2, total)]:
                multiprocess = Process(target=run, args=(
                    start,
                    end,
                    member,
                    message,
                ))
                process_list.append(multiprocess)
                multiprocess.start()
            for _ in process_list:
                _.join()

        if message:
            closure_store_count = len(message)
            body = '\n'.join([f'매장명: {_.get("store_name")} \n'
                              f'사업자번호: {_.get("biz_number")} \n'
                              f'내용: {_.get("message")} \n\n' for _ in message])
            body += f'\n조회일시: {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}'
            send_mail(data={
                'subject': f'[폐업알림] {message[0].get("store_name") + f" 외 {closure_store_count}" if closure_store_count >= 2 else message[0].get("store_name")}',
                'body': body
            })
    except Exception:
        logger_core(error=traceback.format_exc(), name='hometax')
