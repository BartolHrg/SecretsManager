from collections.abc import Iterable;
from functools import wraps;

class Constants:
	ROOT: str;
pass

def singleton[T](cls: type[T]) -> T: return cls();

class InstanceClassMethod:
	def __init__(self, func):
		self.func = func;
	pass
	def __get__(self, obj, cls=None):
		first_arg = obj if obj is not None else cls;
		return lambda *args, **kwargs: self.func(first_arg, *args, **kwargs);
	pass
pass

import os, pathlib;
import importlib.util;

def _pathToPackage(path: str) -> str:
	original = path;
	path: str = str(pathlib.Path(path).resolve()).replace("\\", "/");
	if not path.startswith(Constants.ROOT): raise ValueError(f"Path not under ROOT <${original}>");
	if not path.endswith(".py"): raise ValueError("File not Python <${original}>");
	x = path[len(Constants.ROOT) : -3];
	if x.startswith("/"): x = x[1 : ];
	return x.replace("/", ".");
pass
def importFromPath(path: str):
	original = path;
	path: str = str(pathlib.Path(path).resolve()).replace("\\", "/");
	if not path.startswith(Constants.ROOT): raise ValueError(f"Path not under ROOT <${original}>");
	if not path.endswith(".py"): raise ValueError("File not Python <${original}>");
	x = path[len(Constants.ROOT) : -3];
	if x.startswith("/"): x = x[1 : ];
	package = x.replace("/", ".");
	importlib.import_module(package);
pass

def importAll(directory):
	for filename in os.listdir(directory):
		module_path = os.path.join(directory, filename);
		if not os.path.isfile(module_path): continue;
		if not filename.endswith('.py'): continue;
		importFromPath(module_path);
	pass
pass
