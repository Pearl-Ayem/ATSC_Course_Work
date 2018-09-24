
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Using-ipython-magic-commands" data-toc-modified-id="Using-ipython-magic-commands-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Using ipython magic commands</a></span></li><li><span><a href="#Write-a-module-to-compute-Stull-2.13" data-toc-modified-id="Write-a-module-to-compute-Stull-2.13-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Write a module to compute Stull 2.13</a></span></li></ul></div>

# # Using ipython magic commands
# 
# When you start a jupyter notebook with python (instead of R, Julia, Rust etc.) you
# get access to the ipython interactive environment, which can also be run outside
# Jupyter (and was developed before Jupyter existed).  One feature of ipython is
# "magic" commands:
# 
# [IPython magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
# 
# You can use these to start the debugger, output cells to files, etc.  We've already
# seen
# 
#     %debug
#     
# Below I'll use %%file output a cell to a file for later use as a module

# In[11]:


get_ipython().run_line_magic('magic', '--brief')


# In[19]:


from matplotlib import pyplot as plt
import numpy as np


# # Write a module to compute Stull 2.13
# 
# Save this to a file called "radiation.py" in this folder

# In[34]:


get_ipython().run_cell_magic('file', 'radiation.py', 'import numpy as np\n#\n# get Stull\'s c_1 and c_2 from fundamental constants\n#\n# c=2.99792458e+08  #m/s -- speed of light in vacuum\n# h=6.62606876e-34  #J s  -- Planck\'s constant\n# k=1.3806503e-23  # J/K  -- Boltzman\'s constant\n\nc, h, k = 299792458.0, 6.62607004e-34, 1.38064852e-23\nc1 = 2. * h * c**2.\nc2 = h * c / k\nsigma = 2. * np.pi**5. * k**4. / (15 * h**3. * c**2.)\nprint(sigma)\n\n\ndef Elambda(wavel, Temp):\n    """\n    Calculate the blackbody radiant exitence (Stull 2.13)\n\n    Parameters\n    ----------\n\n      wavel: float or array\n           wavelength (meters)\n\n      Temp: float\n           temperature (K)\n\n    Returns\n    -------\n\n    Elambda:  float or arr\n           monochromatic radiant exitence (W/m^2/m)\n    """\n    Elambda_val = c1 * np.pi / (wavel**5. * (np.exp(c2 / (wavel * Temp)) - 1))\n    return Elambda_val')


# # import the function from that file and use it

# In[33]:


import radiation
from radiation import Elambda
print(f'reading function from {radiation.__file__}')

npoints = 10000
Temp=255  #K
wavelengths=np.linspace(0.1,500.,npoints)*1.e-6  #meters
Estar=Elambda(wavelengths,Temp)
fig, ax = plt.subplots(1,1, figsize=(10,10))
ax.plot(wavelengths*1.e6,Estar*1.e-6)
ax.set(xlim=[0,50])
ax.grid(True)
ax.set(xlabel='wavelength (m)', 
       ylabel='$E_\lambda^*\ (W\,m^{-2}\,\mu^{-1}$)',
       title=f"Monochromatic blackbody flux at Temp={Temp} K");


# In[35]:


Lstar = Estar/np.pi
fig, ax = plt.subplots(1,1, figsize=(10,10))
ax.plot(wavelengths*1.e6,Lstar*1.e-6)
ax.set(xlim=[0,50])
ax.grid(True)
ax.set(xlabel='wavelength (m)', 
       ylabel='$L_\lambda^*\ (W\,m^{-2}\,sr^{-1}\,\mu^{-1}$)',
       title=f"Monochromatic blackbody radiance at Temp={Temp} K");

