from __future__ import annotations;
from typing import *;
import inspect as ins;
import sys, os, pathlib;
__actual_file__   = pathlib.Path(ins.getabsfile(ins.currentframe())).resolve();
__actual_dir__    = os.path.dirname(__actual_file__);
if __name__ == '__main__' and not __package__:
	__actual_parent__ = os.path.dirname(__actual_dir__ );
	sys.path.insert(0, __actual_parent__);
	__package__ = os.path.split(__actual_dir__)[1];
pass



from src.Misc import Constants;
Constants.ROOT = __actual_dir__.replace("\\", "/");
import src.Updater;
print("Updater");

import src.Storage;
print("Storage");
import src.Algorithms.Init;
print("Algorithms");
import src.Elements  .Init;
print("Elements");

