"""
This test tries to confirm that::

    myd05_l2_10_7.hdf

and 

    m3_file_2018_10_1.hdf


are in your a301.data_dir folder and that::

    pyresample.SwathDefinition.compute_optimal_bb_area

can compute an area_def and kdresample can resample
your lats and lons.

Usage::

    python -m a301.install_tests.assign8_test

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
    stars='*'*50
    print(f'\n{stars}\nrunning test: {__file__}\n{stars}\n')
    generic_m3= a301.data_dir / Path("m3_file_2018_10_1.hdf")
    if not generic_m3.exists():
        raise ValueError(f"couldn't find {generic_m3}")
    modis_meta=parseMeta(generic_m3)
    print(f"working on {generic_m3}, originally was { modis_meta['filename']}")
    m3_file = SD(str(generic_m3), SDC.READ)
    lats_1km = m3_file.select('Latitude').get()
    lons_1km = m3_file.select('Longitude').get()
    stars='*'*40
    print(f"{stars}\nlats_1km.shape, lons_1km.shape: {lats_1km.shape},{lons_1km.shape}\n{stars}")
    m3_file.end()


    generic_m5 = a301.data_dir / Path("myd05_l2_10_7.hdf")
    if not generic_m5.exists():
        raise ValueError(f"couldn't find {generic_m5}")

    m5_file = SD(str(generic_m5), SDC.READ)
    vapor_ir=m5_file.select('Water_Vapor_Infrared').get()
    vapor_near_ir = m5_file.select('Water_Vapor_Near_Infrared').get()
    lats_5km = m5_file.select('Latitude').get()
    lons_5km = m5_file.select('Longitude').get()
    m5_file.end()
    print('through')
    m5_meta=parseMeta(generic_m5)
    print(f"working on {generic_m5}, originally was {m5_meta['filename']}")
    print(f"{stars}\nnearir vapor array shape is: {vapor_near_ir.shape}\n{stars}")
    print(f"{stars}\nir vapor array shape is: {vapor_ir.shape}\n{stars}")
    print(f"{stars}\nlats_5km arrayshape is: {lats_5km.shape}\n{stars}")
    print(f"{stars}\nlons_5km arrayshape is: {lons_5km.shape}\n{stars}")
    # print(f'reading {generic_m3}')

    from pyresample import SwathDefinition
    proj_params = get_proj_params(generic_m3)
    swath_def = SwathDefinition(lons_1km, lats_1km)
    area_def=swath_def.compute_optimal_bb_area(proj_dict=proj_params)

    fill_value=-9999.
    area_name = 'modis swath 5min granule'
    image_nearir = kd_tree.resample_nearest(swath_def, vapor_near_ir.ravel(),
                                      area_def, radius_of_influence=5000, 
                                          nprocs=2,fill_value=fill_value)
    print(f'was able to regrid the nearir image, xy shape is {image_nearir.shape}')

    proj_params = get_proj_params(generic_m5)
    swath_def = SwathDefinition(lons_5km, lats_5km)
    area_def=swath_def.compute_optimal_bb_area(proj_dict=proj_params)

    fill_value=-9999.
    area_name = 'modis swath 5min granule'
    image_ir = kd_tree.resample_nearest(swath_def, vapor_ir.ravel(),
                                      area_def, radius_of_influence=5000, 
                                          nprocs=2,fill_value=fill_value)
    print(f'was able to regrid the ir image, xy shape is {image_ir.shape}')

    print('data looks good, ready to go')


if __name__ == "__main__":
    main()
