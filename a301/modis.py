def get_index(band_nums,chan_num):
    """
    given the longwave_bands vector from the level1b file, 
    find the index of the channel chan_num in the dataset
    
    Parameters
    ----------
    
    band_nums: numpy float vector
       list of channel numbers
       
    chan_num: float or int
       channel number to get index for
       
    Returns
    -------
    
    the_index: int
        index of channel in modis image

    """
    ch_index=np.searchsorted(band_nums,chan_num)
    return int(ch_index)

from pyhdf.SD import SD, SDC
from a301.radiation import planck_invert
modis_file = a301.data_dir / Path("myd02_2018_10_10.hdf")

def get_modis_lw_radiance(m2_file,chan_num):
    """
    given a modis MYD02 file path and and a band number 
    from https://modis.gsfc.nasa.gov/about/specifications.php
    get the scaled radiance
    
    Parameters:
    
    m2_file: Path or str 
       path to MYD02 file
    
    chan_num: int
       channel/band number to extract
    """
    the_file = SD(str(m2_file), SDC.READ)    
    longwave_data = the_file.select('EV_1KM_Emissive') # 
    longwave_bands = the_file.select('Band_1KM_Emissive')
    band_nums=longwave_bands.get()
    band_index=get_index(band_nums,chan_num)
    band_data = longwave_data[band_index,:,:]
    scales=longwave_data.attributes()['radiance_scales']
    offsets=longwave_data.attributes()['radiance_offsets']
    band_scale=scales[band_index]
    band_offset=offsets[band_index]
    band_calibrated =(band_data - band_offset)*band_scale
    return band_calibrated
