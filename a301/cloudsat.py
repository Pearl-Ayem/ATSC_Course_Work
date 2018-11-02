"""
Cloudsat utily code to describe a cloudsat
file's contents and retrieve the geographical time, distance data
fields
"""

import datetime
import numpy as np
from pathlib import Path
from pyhdf.HDF import HDF, HC, HDF4Error
from pyhdf.V   import V
from pyhdf.VS  import VS
from pyhdf.SD  import SD, SDC
import pdb
import pprint

import sys

#https://stackoverflow.com/questions/31003968/fields-not-found-when-using-pyhdf
def describevg(refnum,v,vs,sd):
    """
    read a vgroup with a given refnum

    Parameters
    ----------

    refnum: int
      hdf4 reference number for element

    v: hdf.vgstart object marks the beginning of the vgroup

    vs: hdf.vstart object marks the beginning of the vdata

    Returns
    -------

    prints information about the vgroup

    """
    print(f'Scientific Datasets: \n{pprint.pformat(sd.datasets())}\n')
    # Describe the vgroup with the given refnum.
    # Open vgroup in read mode.
    vg = v.attach(refnum)
    print("----------------")
    print("vg name is:", vg._name, "class:",vg._class, "tag,ref:", end=' ')
    print(vg._tag, vg._refnum)
    
    # Show the number of members of each main object type.
    print("num. members: ", vg._nmembers, end=' ')
    print("num. datasets:", vg.nrefs(HC.DFTAG_NDG), end=' ')
    print("num. vdatas:  ", vg.nrefs(HC.DFTAG_VH), end=' ')
    print("num. vgroups: ", vg.nrefs(HC.DFTAG_VG))

    # Read the contents of the vgroup.
    members = vg.tagrefs()

    # Display info about each member.
    index = -1
    for tag, ref in members:
        index += 1
        print("member index", index)
        # Vdata tag
        if tag == HC.DFTAG_VH:
            vd = vs.attach(ref)
            nrecs, intmode, fields, size, name = vd.inquire()
            print(f"reading {vg._name} and dataset {name}")
            print("  vdata:",name, "tag,ref:",tag, ref)
            print("    fields:",fields)
            print("    nrecs:",nrecs)
            vd.detach()

        # SDS tag
        elif tag == HC.DFTAG_NDG:
            sds = sd.select(sd.reftoindex(ref))
            name, rank, dims, type, nattrs = sds.info()
            print("  dataset:",name, "tag,ref:", tag, ref)
            print("    dims:",dims)
            print("    type:",type)
            sds.endaccess()

        # VS tag
        elif tag == HC.DFTAG_VG:
            vg0 = v.attach(ref)
            print("  vgroup:", vg0._name, "tag,ref:", tag, ref)
            vg0.detach()

        # Unhandled tag
        else:
            print("unhandled tag,ref",tag,ref)

    # Close vgroup
    vg.detach()

def dump_cloudsat(filename):
    """
    walk the hdf file and print out
    information about each vgroup and vdata
    object

    Parameters
    ----------

    filename: str or Path object
        name of hdf file

    Returns
    -------

    prints information to stdout
    """
    #
    
    filename=str(filename)
    hdf = HDF(filename)

    # Initialize the SD, V and VS interfaces on the file.
    sd = SD(filename)
    vs = hdf.vstart()
    v  = hdf.vgstart()

    # Scan all vgroups in the file.
    ref = -1
    while 1:
        try:
            ref = v.getid(ref)
            print('vgroup: ',ref)
        except HDF4Error as msg:    # no more vgroup
            break
        describevg(ref,v,vs,sd)
    return None

def HDFvd_read(filename, variable, vgroup=None):
    out=HDFread(filename, variable, vgroup = vgroup)
    return out

def HDFread(filename, variable, vgroup=None):
    """
    Extract the data for non-scientific data in V mode of hdf file
    """
    if vgroup is None:
        vgroup = 'Geolocation Fields'
        
    filename=str(filename)
    hdf = HDF(filename, HC.READ)

    # Initialize the SD, V and VS interfaces on the file.
    sd = SD(filename)
    vs = hdf.vstart()
    v  = hdf.vgstart()
    vg_dict={}
    ref = -1
    while 1:
        try:
            ref = v.getid(ref)
            #print('vgroup ref number: ',ref)
        except HDF4Error as msg:    # no more vgroup
            break
        vg = v.attach(ref)
        # print("----------------")
        # print("vg name is:", vg._name, "class:",vg._class, "tag,ref:", end=' ')
        # print(vg._tag, vg._refnum)
        vg_dict[vg._name]=(vg._tag, vg._refnum)
        vg.detach()
        
    tag, ref = vg_dict[vgroup]

    # Open all data of the class
    vg = v.attach(ref)
    # print("----------------")
    # print("vg name is:", vg._name, "class:",vg._class, "tag,ref:", end=' ')
    # print(vg._tag, vg._refnum)

    # All fields in the class
    members = vg.tagrefs()

    nrecs = []
    names = []
    for tag, ref in members:
        # Vdata tag
        if tag == HC.DFTAG_VH:
            vd = vs.attach(ref)
            nrec, intmode, fields, size, name = vd.inquire()
            nrecs.append(nrec)
            names.append(name)
            vd.detach()
    try:
        idx = names.index(variable)
    except ValueError:
        error=f'{variable} is not in {names} for vgroup {vgroup}'
        raise ValueError(error)
        
    var = vs.attach(members[idx][1])
    V   = var.read(nrecs[idx])
    var.detach()
    # Terminate V, VS and SD interfaces.
    v.end()
    vs.end()
    sd.end()
    # Close HDF file.
    hdf.close()
    return np.asarray(V)

def HDFsd_read(filename,sdname):
    the_file = SD(str(filename), SDC.READ)
    try:
        out=the_file.select(sdname)
        values=out.get()
        attributes=out.attributes()
    except HDF4Error as e:
        datasets_dict = the_file.datasets()
        print(f"couldn't find {sdname} in "
              f"\n{pprint.pformat(datasets_dict)}")
        values=None
        attributes=None
        print(e)
    the_file.end()
        
    return values, attributes


def get_geo(hdfname, monotonic_lons=True):
    """
    given the name of any hdf file from the Cloudsat data archive
    return lat,lon,time_vals,prof_times,dem_elevation
    for the cloudsat orbital swath
    
    usage:  lat,lon,date_times,prof_times,dem_elevation=get_geo(filename)
    
    Parameters
    ----------
    
    hdfname:  str or Path object
          string with name of hdf file from http://www.cloudsat.cira.colostate.edu/dataSpecs.php
    monotonic_id: bool
           wrap the longitude by addint 360 degrees if it flips form 180 to -180 

    Returns
    -------
    
    lat: vector float
       profile latitude in degrees north  (1-D vector)
    
    lon: vector float
      profile longitude in degrees north (1-D vector)
    
    time_vals: vector datetimes
       profile times in UTC  (1D vector)
    
    prof_times: vector int
       profile times in seconds since beginning of orbit (1D vector)
    
    dem_elevation: vector float
       surface elevation in meters
    """

    variable_names=['Longitude','Latitude','Profile_time','DEM_elevation']
    var_dict={}
    for var_name in variable_names:
        var_dict[var_name]=HDFread(hdfname,var_name)
    #
    # tai stands for "international atomic time
    # https://en.wikipedia.org/wiki/International_Atomic_Time
    # https://space.stackexchange.com/questions/22240/is-gps-time-at-least-really-close-to-tai-international-atomic-time
    # 
    #
    tai_start=HDFread(hdfname,'TAI_start')[0][0]
    #
    # the longitude can flip between +180 and -180 at the international dateline
    # detect if this happens, and shift it to make it in the range -360 to +720 degrees
    #
    # ===================================================================== #
    if monotonic_lons:
        lon=var_dict['Longitude'][:];
        for id in range(0, len(lon)-1):
            if lon[id+1] > lon[id]:
                lon[id+1] = lon[id+1]-360
        lonmin=np.amin(lon)
        #
        # basemap requires lons in the range -360 - 720 degrees
        #
        if lonmin < -360.:
            lon[:]=lon[:] + 360.
        var_dict['Longitude']=lon
    #
    #
    #tai_start is the number of seconds since Jan 1, 1993 for orbit start
    #
    #
    taiDelta=datetime.timedelta(seconds=tai_start)
    taiDayOne=datetime.datetime(1993,1,1,tzinfo=datetime.timezone.utc)
    #this is the start time of the orbit in seconds since Jan 1, 1993
    orbitStart=taiDayOne + taiDelta
    time_vals=[]
    #now loop throught he radar profile times and convert them to 
    #python datetime objects in utc
    for the_time in var_dict['Profile_time']:
        date_time=orbitStart + datetime.timedelta(seconds=float(the_time))
        time_vals.append(date_time)
    var_dict['date_day']=np.array(time_vals)
    neg_values=var_dict['DEM_elevation'] < 0
    var_dict['DEM_elevation'][neg_values]=0
    #
    # return a list with the five variables
    #
    variable_names=['Latitude','Longitude','date_day','Profile_time','DEM_elevation']
    out_list=[var_dict[varname] for varname in variable_names]  
    return out_list

if __name__ == "__main__":

    import a301
    filename= a301.test_data / \
            Path('2006303212128_02702_CS_2B-GEOPROF_GRANULE_P_R04_E02.hdf')
    lat,lon,date_times,prof_times,dem_elevation=get_geo(filename)
    minlat,maxlat = np.min(lat),np.max(lat)
    minlon,maxlon = np.min(lon),np.max(lon)
    maxheight = np.max(dem_elevation)
    print(f'\nlatitudes -- deg north: \nmin: {minlat},  max: {maxlat}\n')
    print(f'\nlongitudes -- deg east: \nmin: {minlon},max: {maxlon}\n')
    print(f'\nmax elev (m): {maxheight}\n')
    print(f'\norbit start/stop dates (UCT): \nstart: {date_times[0]}\nstop: {date_times[-1]}\n')
    
          
