import time
import requests
import traceback
import xml.etree.ElementTree as Xml

from random import uniform
from requests import Response
from logger import logger_core


NAME = 0
COMPANY_NUMBER = 1
PAST_COMPANY_TYPE = 2
URL = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&" \
      "screenId=UTEABAAA13&popupYn=false&realScreenId="
REQUEST_XML = '<map id="ATTABZAA001R08">' \
                    '<pubcUserNo/><mobYn>N</mobYn>' \
                    '<inqrTrgtClCd>1</inqrTrgtClCd>' \
                    '<txprDscmNo>{}</txprDscmNo>' \
                    '<dongCode>81</dongCode>' \
                    '<psbSearch>Y</psbSearch>' \
                    '<map id="userReqInfoVO"/></map>' \
                    '<nts<nts>nts>6972PGjXYpIRLHKe6efvlCnea5OAZ8yxZf7TCGdcI58'


def hometax(biz_no: str) -> Response:
    if isinstance(biz_no, int) or isinstance(biz_no, float):
        biz_no = str(biz_no)
    time.sleep(uniform(4, 5))
    try:
        xml = requests.post(url=URL, headers={'Content-Type': 'application/xml'}, data=REQUEST_XML.format(biz_no))
        root = Xml.fromstring(xml.text)
        response = root.find('trtCntn').text
    except Exception:
        logger_core(traceback.format_exc())
        return ''
    return response
