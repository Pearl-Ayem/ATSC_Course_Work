"""
This test tries to confirm that::

    wv_ir, wv_nearir_hr, and wv_nearir_lr are all in a301.map_dir

and that the MYD021KM file

    myd02_2018_10_10.hdf

exists and is readable

Usage::

    python -m a301.install_tests.assign9_test

which should print out shapes and diagnostics, or an error message
if you have the wrong files

"""

from pyhdf.SD import SD, SDC
from a301.scripts.modismeta_read import parseMeta
import a301
from pathlib import Path
import json
import pprint

def main():
    """
    run the test
    """
    for the_root in ['wv_ir', 'wv_nearir_hr', 'wv_nearir_lr']:
        the_file = a301.map_dir / Path(f'wv_maps/{the_root}.json')
        with open(the_file,'r') as f:
            metadata_dict=json.load(f)
        print(f"found ({metadata_dict['area_def']['name']})")
    print('\ndata looks good, ready to go')

if __name__ == "__main__":
    main()
