import cartopy.crs as ccrs
from .scripts.modismeta_read import parseMeta

def get_proj_params(modis_file):
    """
    given a path to a Modis level1b file with a standard
    'CoreMetadata.0' atrribute, return proj4 parameters
    for use by cartopy or pyresample, assuming a laea projection
    and WGS84 datum
    
    Parameters
    ----------
    
    modis_file:  Path or str with path to hdf file
    
    Returns
    -------
    
    proj_params: dict
        dict with parameters for proj4
        
    """
    modis_dict=parseMeta(modis_file)
    import cartopy.crs as ccrs
    globe_w = ccrs.Globe(datum="WGS84",ellipse="WGS84")
    projection_w=ccrs.LambertAzimuthalEqualArea(central_latitude=modis_dict['lat_0'],
                    central_longitude= modis_dict['lon_0'],globe=globe_w)
    proj_params=projection_w.proj4_params
    return proj_params

def make_projection(proj_params):
    """
    turn a set of proj4 parameters into a cartopy laea projection
    
    Parameters
    ----------
    
    proj_params: dict
       dictionary with parameters lat_0, lon_0 datum and ellps
       
    Returns
    -------
    
    cartopy projection object
    
    """
    import cartopy.crs as ccrs
    globe_w = ccrs.Globe(datum=proj_params["datum"],ellipse=proj_params['ellps'])
    projection_w=ccrs.LambertAzimuthalEqualArea(central_latitude=float(proj_params['lat_0']),
                    central_longitude= float(proj_params['lon_0']),globe=globe_w)
    return projection_w
