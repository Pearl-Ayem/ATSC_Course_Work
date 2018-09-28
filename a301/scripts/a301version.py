"""
prints the version of the the a301 library
and the path to the data_dir folder
"""

import os, sys
import argparse

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def make_parser():
    """
    set up the command line arguments needed to call the program
    """
    linebreaks = argparse.RawTextHelpFormatter
    # parser = MyParser(
    #     formatter_class=linebreaks, description=__doc__.lstrip())
    parser = argparse.ArgumentParser(
        formatter_class=linebreaks, description=__doc__.lstrip())
    return parser

def main(args=None):
    """
    args: no arguments
    """
    parser = make_parser()
    args = parser.parse_args(args)
    import a301
    print(f'a301 version - {a301.__version__}\n')
    print(f'data_dir is {a301.data_dir}\n')

if __name__ == "__main__":
    #
    # will exit with non-zero return value if exceptions occur
    #
    sys.exit(main())
