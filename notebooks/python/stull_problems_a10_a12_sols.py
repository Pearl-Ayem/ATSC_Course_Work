
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Stull-problem-8-A.10" data-toc-modified-id="Stull-problem-8-A.10-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Stull problem 8-A.10</a></span><ul class="toc-item"><li><span><a href="#my-test-for-a10" data-toc-modified-id="my-test-for-a10-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>my test for a10</a></span></li></ul></li><li><span><a href="#Stull-problem-8-A.12" data-toc-modified-id="Stull-problem-8-A.12-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Stull problem 8-A.12</a></span><ul class="toc-item"><li><span><a href="#my-test-for-a12" data-toc-modified-id="my-test-for-a12-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>my test for a12</a></span></li></ul></li></ul></div>

# # Stull problem 8-A.10

# Chapter 8-A10. Write a python function to find the beamwidth angle in degrees for a radar pulse
# for the following sets of 
# [wavelength (cm) , antenna
# dish diameter (m)]:
#         
# a. [ 20, 8] b. [20, 10] c. [10, 10] d. [10, 5] e. [10, 3]
# f. [5, 7] g. [5, 5] h. [5, 2] i. [5, 3] j. [3, 1]

# In[1]:


import numpy as np
import pytest
import json
from pathlib import Path
import a301

def find_beamwidth(the_wavel,dish_size):
    """
    find the beamwidth using Stulll eq. 8.13
    
    Parameters
    ----------
    
    the_wavel : wavelength (float)
       units (cm)
            
    dish_size : antenna dish diameter (float)
       units (m)
       
    Returns
    -------
    
    beamwidth : beamwidth angle  
       units (degrees)
    """
    #
    # Stull eq. 8.13
    #
    ### BEGIN SOLUTION
    a = 71.6 #constant (degrees)
    the_wavel = the_wavel/100. #convert cm to m
    beamwidth = a*the_wavel/dish_size #beamwitdh in degrees
    return beamwidth
    ### END SOLUTION


# ## my test for a10

# In[2]:


the_wavel=[20,20,10,10,10,5,5,5,5,3]  #wavelength (cm)
dish_size=[8,10,10,5,3,7,5,2,3,1]   #dishsize (meters)
input_vals=list(zip(the_wavel,dish_size))
assert(len(input_vals)==10)
beamwidth=[find_beamwidth(wavel,dish_size) for wavel,dish_size in input_vals]
#
# test the beamwidth values
#
answer_file='ch8_a10_answer.json'
if Path(answer_file).is_file():
    with open(answer_file,'r') as f:
        answer=json.load(f)
    np.testing.assert_array_almost_equal(beamwidth,answer,decimal=3)


# # Stull problem 8-A.12
# 
# Write a python function to find the range to a radar target, given the
# round-trip (return) travel times (µs) of:
# 
# a. 2 b. 5 c. 10 d. 25 e. 50
# f. 75 g. 100 h. 150 i. 200 j. 300

# In[3]:


def find_range(delT):
    """
    tind the range to radar using Stull eq. 8.16
    
    Parameters
    ----------
    
    delT: float
       the round-trip travel times (units: micro sec)
       
    Returns
    -------
    
    radar_range: float
       range from target to radar (units: km)
    """
    
    ### BEGIN SOLUTION
    c = 3e8 #speed of light (m/s)
    delT = delT*(1.e-6) #convert microseconds to s
    radar_range = c*delT/2
    return radar_range*1.e-3  #kilometers
    ### END SOLUTION


# ## my test for a12

# In[4]:


import json
times=[2,5,10,25,50,75,100,150,200,300]  #microseconds
the_range=[find_range(delT) for delT in times]
assert(len(times) == 10)
answer_file= a301.test_dir / 'ch8_a12_answer.json'
if Path(answer_file).is_file():
    with open(answer_file,'r') as f:
        answer=json.load(f)
    np.testing.assert_array_almost_equal(the_range,answer,decimal=1)

