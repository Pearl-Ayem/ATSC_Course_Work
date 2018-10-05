"""
This test tries to confirm that::

    m3_file_2018_10_1.hdf

and:: 

    rad_file_2018_10_1.hdf

are in your a301.data_dir folder and that::

    pyresample.SwathDefinition.compute_optimal_bb_area

can compute an area_def and kdresample can resample
your lats and lons.

Usage::

    python -m a301.scripts.week5_test

which should print out shapes and diagnostics, or an error message
if you have the wrong files

"""

from pyhdf.SD import SD, SDC
from a301.scripts.modismeta_read import parseMeta
from a301.geometry import get_proj_params
from pyresample import kd_tree
import a301
from pathlib import Path

def main():
    """
    run the test
    """
    generic_m3= a301.data_dir / Path("m3_file_2018_10_1.hdf")
    if not generic_m3.exists():
        raise ValueError(f"couldn't find {generic_m3}")
    modis_meta=parseMeta(generic_m3)
    print(f"working on {generic_m3}, originally was { modis_meta['filename']}")
    m3_file = SD(str(generic_m3), SDC.READ)
    lats = m3_file.select('Latitude').get()
    lons = m3_file.select('Longitude').get()
    stars='*'*40
    print(f"{stars}\nlats.shape, lons.shape: {lats.shape},{lons.shape}\n{stars}")
    m3_file.end()


    generic_rad= a301.data_dir / Path("rad_file_2018_10_1.hdf")
    if not generic_rad.exists():
        raise ValueError(f"couldn't find {generic_rad}")

    rad_file = SD(str(generic_rad), SDC.READ)
    ch30=rad_file.select('ch30').get()
    print(f"working on {generic_rad}, originally was {rad_file.filename}")
    print(f"{stars}\narray shape is: {ch30.shape}\n{stars}")
    rad_file.end()

    print(f'reading {generic_m3}')


    from pyresample import SwathDefinition
    proj_params = get_proj_params(generic_m3)
    swath_def = SwathDefinition(lons, lats)
    area_def=swath_def.compute_optimal_bb_area(proj_dict=proj_params)

    fill_value=-9999.
    area_name = 'modis swath 5min granule'
    image_30 = kd_tree.resample_nearest(swath_def, ch30.ravel(),
                                      area_def, radius_of_influence=5000, 
                                          nprocs=2,fill_value=fill_value)
    print(f'\ndump area definition:\n{area_def}\n')
    print((f'\nx and y pixel dimensions in meters:'
           f'\n{area_def.pixel_size_x}\n{area_def.pixel_size_y}\n'))


if __name__ == "__main__":
    main()
