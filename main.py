from logging import basicConfig, DEBUG
from sys import argv

from colorama import init

from cure import CureArgParser


def main():
    arg_parser = CureArgParser(argv)
    arg_parser.parse()


def setup_logger():
    basicConfig(
        filename='debug.log', filemode='w',
        format='%(filename)s (line %(lineno)d) [%(levelname)s] - %(message)s',
        encoding='utf-8', level=DEBUG
    )



if __name__ == '__main__':
    init()
    setup_logger()
    main()
