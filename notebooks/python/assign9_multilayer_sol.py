
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Using-Stull-eqn.-8.4-to-find-the-outgoing-radiance" data-toc-modified-id="Using-Stull-eqn.-8.4-to-find-the-outgoing-radiance-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Using Stull eqn. 8.4 to find the outgoing radiance</a></span></li><li><span><a href="#Autograded-answer" data-toc-modified-id="Autograded-answer-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Autograded answer</a></span></li></ul></div>

# # Using Stull eqn. 8.4 to find the outgoing radiance
# 
# 
# Complete the function below that calculates the radiance through the top
# of a stack of layers given the optical thickness, layer temperature and
# surface temperature.  I borrowed code from the weighting_functions notebook, my
# answer is 9 lines of code including the return statement

# In[8]:


from a301.radiation import calc_radiance
import numpy as np
import pdb

def multi_layer_radiance(Tsfc,Temps,tau,the_wavel):
    """
    Find the radiance $L_λ$ reaching a satllite from an N-level atmosphere
    using Stull equation 8.4
    
    Given N levels (counting surface), and N-1 layers with the following layout:
    
    ============= tau[-1]
    
      Temps[-1]
      
    ============= tau[N-2]
      
      .....
      
    ============= tau[2]
    
      Temps[1]
      
    ============= tau[1]
     
      Temps[0]
      
    ============= Tsfc, tau[0]=0
    
    this function calculates the vertical, upward, monochromatic radiance
    at a given wavelength, passing through the top level N of layer N-1.  It includes
    both surface emission (assuming a black surface at temperature Tsfc)
    
    Parameters
    ----------
    
    Tsfc:  float (Kelvin)
       temperature of the black surface
    
    Temps: numpy vector (Kelvin)
       Layer temperatures with Temps[0] being closest to the surface
       Length is N-1, where N is the number of levels
       
    tau: numpy vector (unitless)
       Level values of the absorption optical thicknesses at this wavelength
       taus[0]=0 is the surface, tau[-1]=tau_tot is the total optical thickness
       lenght is N, the number of levels
       
    the_wavel: float (m)
       wavelength for calc_radiance
       
    Returns
    -------
    
    Radiance: float (W/m^2/m/sr) 
       Radiance from the surface and layers passing through the top level
    
    
    """
    ### BEGIN SOLUTION
    Batm = np.array([calc_radiance(the_wavel,the_temp) for the_temp in Temps])
    Bsfc = calc_radiance(the_wavel,Tsfc)
    tau_tot = tau[-1]
    trans = np.exp(-(tau_tot - tau))
    weights=np.diff(trans)
    sfc_flux=Bsfc*np.exp(-tau_tot)
    atm_flux = np.sum(Batm*weights)
    print(f'{type(Batm)}, {type(weights)}')
    the_flux=sfc_flux + atm_flux
    return the_flux
    ### END SOLUTION


# # Autograded answer
# 
# Here is a test set of layers that should produce a radiance of 9.045 W/m^2/micron/sr

# In[9]:


from numpy.testing import assert_almost_equal
Temps=np.asarray([300.,280.,270.,260.])
taus=np.asarray([0.,0.2, 0.35, 0.5, 0.6])
Tsfc=305.
the_wavel=10.e-6
out=multi_layer_radiance(Tsfc,Temps,taus,the_wavel)
assert_almost_equal(out*1.e-6,9.045,decimal=3)


# In[3]:


### BEGIN HIDDEN TESTS
Temps=np.asarray([300.,280.,270.,260.,240.,230.])
taus=np.asarray([0.,0.2, 0.35, 0.5, 0.6, 0.65, 0.75])
Tsfc=305.
the_wavel=10.e-6
out=multi_layer_radiance(Tsfc,Temps,taus,the_wavel)
assert_almost_equal(out*1.e-6,8.134,decimal=3)
### END HIDDEN TESTS

