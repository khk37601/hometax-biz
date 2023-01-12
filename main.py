import argparse

from process import start


if '__main__' == __name__:
    parser = argparse.ArgumentParser(description='Hometax')
    parser.add_argument('-s', '--status', action='store_true', help='update business status')
    args = parser.parse_args()
    if args.status:
        start()
