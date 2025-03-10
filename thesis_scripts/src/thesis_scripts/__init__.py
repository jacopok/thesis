import matplotlib.pyplot as plt
from pathlib import Path
import os
from . import dummy_module
plt.rc('text', usetex=True)

data_path = Path(os.path.abspath(dummy_module.__file__)).resolve().parent.parent.parent.parent / 'data'


