import sys
from pathlib import Path
import site
#
# put the folder above this one in sys.path
# so python can find libraries
#
path=Path(__file__).resolve()
sys.path.insert(0,path.parent.parent)
sep='*'*30
print(sys.path)
print(f'{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n{sep}\n')
data_dir = path.parent.parent / Path('data')
if data_dir.is_dir():
    print(f'\ndata directory a301.data_dir = {data_dir}\n')
site.removeduppaths()
