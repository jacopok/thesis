import matplotlib.pyplot as plt
from pathlib import Path
import os
from . import dummy_module
plt.rc('text', usetex=True)
plt.rc('font',**{'family':'serif'})

data_path = Path(os.path.abspath(dummy_module.__file__)).resolve().parent.parent.parent.parent / 'data'

if not (data_path / 'cache').exists():
	os.makedirs((data_path / 'cache').as_posix())
