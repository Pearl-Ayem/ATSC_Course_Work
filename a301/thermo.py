import numpy as np
import pdb

g=9.8  #m/s/s don't worry about g(z) for this exercise
Rd=287.  #kg/m^3


def calcDensHeight(T,z):
    """
    Calculate the density scale height H_rho

    Introduced in the hydrostatic_balance notebook
    
    Parameters
    ----------
    
    T: vector (float)
      temperature (K)
      
    z: vector (float) of len(T
      height (m)
      
    Returns
    -------
    
    Hbar: vector (float) of len(T)
      density scale height (m)
    """
    dz=np.diff(z)
    TLayer=(T[1:] + T[0:-1])/2.
    dTdz=np.diff(T)/np.diff(z)
    oneOverH=g/(Rd*TLayer) + (1/TLayer*dTdz)
    Zthick=z[-1] - z[0]
    oneOverHbar=np.sum(oneOverH*dz)/Zthick
    Hbar = 1/oneOverHbar
    return Hbar
