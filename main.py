from logging import basicConfig, info, DEBUG
from platform import system
from sys import argv

from colorama import init

from cure import ArgParser


def main():
    info('Cure version 0.1.0')
    info('Backend: LLVM')
    info(f'Platform: {system()}')

    arg_parser = ArgParser(argv[1:])
    arg_parser.parse()


if __name__ == '__main__':
    init()
    basicConfig(
        filename='compile.log', level=DEBUG, filemode='w',
        format='%(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
    )
    main()
