from pyhdf.SD import SD, SDC
from pathlib import Path
import numpy as np
import a301

m5_file = a301.data_dir / Path('myd05_l2_10_7.hdf')
the_file = SD(str(m5_file), SDC.READ)
wv_nearir_data = the_file.select('Water_Vapor_Near_Infrared').get()
the_file.end
positive = wv_nearir_data > 0.
print(f'found {np.sum(positive.flat)} positive pixels')


