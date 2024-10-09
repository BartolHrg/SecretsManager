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

if TYPE_CHECKING:
	from .User import User;
pass

from .Storage import Database, generateAvailablePath;
from .Elements.Element import Element;

class Vault:
	"""User's collection of elements  
		Different from User since it can manipulate elements (user just holds data and can manipulate self)  
		Different from VaultElement since idk, it is  
		
		This should hold a optional reference to db of subvaults, but name of db should be in vault element (main vault db is always main.db)  
			each user optionally has his own db  
	"""
	_sub_db: Database | None = None;
	def __init__(self, user: User, db: Database):
		self.user = user;
		self.db = db;
		with db: elements = db.dataGetUserOwned(user);
		self.elements = [Element.load(db_data) for db_data in elements];
	pass
	def getSudo(self): ...
	def getSubDb(self):
		if self._sub_db is None:
			if not self.user.sub_db_path:
				self.user.sub_db_path = generateAvailablePath(permanent = True);
				with self.db: self.db.userSave(self.user);
			pass
			self._sub_db = Database(self.user.sub_db_path);
		pass
		return self._sub_db;
	pass
	def addElement(self, element: Element): ...
	def deleteElement(self, element: Element): ...
	def delete(self): ...
pass