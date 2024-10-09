from __future__ import annotations;
from typing import TYPE_CHECKING;

if TYPE_CHECKING:
	from .Vault import Vault;
pass

class Globals:
	ROOT: str;
	vault: Vault;
pass

def singleton[T](cls: type[T]) -> T: return cls();

class InstanceClassMethod:
	def __init__(self, func):
		self.func = func;
	pass
	def __get__(self, obj, cls):
		first_arg = obj if obj is not None else cls;
		return lambda *args, **kwargs: self.func(first_arg, *args, **kwargs);
	pass
pass

class memberclass[T]:
	def __init__(self, cls: type[T]):
		self.cls = cls;
	pass
	def __get__(self, obj, cls) -> T:
		if obj is None: return self.cls;
		fullname = "_memberclass__" + self.cls.__name__;
		if hasattr(obj, fullname): return getattr(obj, fullname);
		member = self.cls();
		member.self = obj;
		setattr(obj, fullname, member);
		return member;
	pass
pass

import os, pathlib;
import importlib.util;

def _pathToPackage(path: str) -> str:
	original = path;
	path: str = str(pathlib.Path(path).resolve()).replace("\\", "/");
	if not path.startswith(Globals.ROOT): raise ValueError(f"Path not under ROOT <${original}>");
	if not path.endswith(".py"): raise ValueError("File not Python <${original}>");
	x = path[len(Globals.ROOT) : -3];
	if x.startswith("/"): x = x[1 : ];
	return x.replace("/", ".");
pass
def importFromPath(path: str):
	original = path;
	path: str = str(pathlib.Path(path).resolve()).replace("\\", "/");
	if not path.startswith(Globals.ROOT): raise ValueError(f"Path not under ROOT <${original}>");
	if not path.endswith(".py"): raise ValueError("File not Python <${original}>");
	x = path[len(Globals.ROOT) : -3];
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
