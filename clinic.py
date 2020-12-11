from import_helper import dynamic_import
import os
import sys
configure = dynamic_import('config.configure')


def main():
    """
    Function takes information from the commandline.
    """
    args = configure.set_parser()
    t = args.t
    r = args.r
    d = args.d
    n = args.n
    m = args.m
    os.system(f'python3 config/configure.py -n {n} -r {r} -m {m} -d {d} -t {t}')

if __name__ == '__main__':
    main()
