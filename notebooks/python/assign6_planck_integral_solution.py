
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Assignment-5-Planck-integral-problem" data-toc-modified-id="Assignment-5-Planck-integral-problem-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Assignment 5 Planck integral problem</a></span></li><li><span><a href="#Answer----write-your-function-in-the-cell-below" data-toc-modified-id="Answer----write-your-function-in-the-cell-below-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Answer -- write your function in the cell below</a></span></li></ul></div>

# ### Assignment 5 Planck integral problem
# 
# Following the apprach of the [derivs_and_ints notebook]([https://clouds.eos.ubc.ca/~phil/courses/atsc301/coursebuild/html/derivs_and_ints.html)
# 
# Verify Stull equation 2.15:
# 
#  $$\int_0^\infty  E^*_\lambda(T)d\lambda   =\int_0^\infty \frac{\pi h c^2}{\lambda^5 \left [ \exp (h c/(\lambda k_B T )) -1 \right ] } d\lambda = \int_0^\infty \frac{c_1}{\lambda^5 \left [ \exp (c_2/(\lambda T )) -1 \right ] } d\lambda  = \sigma_{SB} T^4$$
#  
# For a temperature of 300 K.

# ### Answer -- write your function in the cell below
# 
# It can use [a301.radiation.Elambda](https://clouds.eos.ubc.ca/~phil/courses/atsc301/_modules/a301/radiation.html#Elambda)

# In[1]:


import numpy as np
from matplotlib import pyplot as plt
from a301.radiation import Elambda

def planckint(wavelen_start,wavelen_stop,Temp,npoints=10000):
    """
    Calculate the integrated blackbody radiant exitence (Stull 2.13)
    between two wavelengths
    
    Parameters
    ----------
    
      wavel_start: float
            lower limit of integral (meters)
            
      wavel_stop: float
            upper limit of integral (meters)
           
      Temp: float
           temperature (K)
           
    Returns
    -------
    
    Elambda:  float 
           integrated radiant fllux (W/m^2)
    """
    ### BEGIN SOLUTION
    wavelengths=np.linspace(wavelen_start,wavelen_stop,npoints)
    flux = Elambda(wavelengths,Temp)
    avg_flux = (flux[1:] + flux[:-1])/2.
    integral = np.sum(avg_flux*np.diff(wavelengths))
    return integral
    ## END SOLUTION


# Place your own tests in the cell below.  Remember that you can use
#     
#     numpy.testing.assert_almost_equal
# 
# to check to see if your integral matches the $\sigma T^4$ to x decimal places.  I will
# test for decimal=1, i.e. I will run:
# 
# assert_almost_equal(your_answer, my_answer,decimal=1)

# In[15]:


from numpy.testing import assert_almost_equal
from a301.radiation import sigma
Temp=300.
low = 0.01e-6
high=5000e-6
truth = sigma*Temp**4.
flux=planckint(low,high,Temp,npoints=80000)
test_result=assert_almost_equal(flux,truth,decimal=1)
print(f"numpy: {flux}, stefan-boltzman: {truth}\n"
      f"do the answers match? (None means yes): "
      f"{test_result}")


# In[ ]:


help(assert_)

