from __future__ import annotations;

from ..Storage import DbData;
from ..User import User;

class Element:
	element_types: dict[int, type[Element]] = {};
	element_type: int;
	db_data: DbData;
	key: str;
	
	def __init_subclass__(cls):
		assert hasattr(cls, "element_type");
		assert cls.element_type not in cls.element_types.keys();
		cls.element_types[cls.element_type] = cls;
		assert cls.create is not Element.create, f"Class {cls} didn't implement create";
	pass

	def save(self, force = False): ...
	@staticmethod
	def load(db_data: DbData) -> Element:
		element_type = db_data.kind;
		cls = Element.element_types[element_type];
		self = cls();
		self.db_data = db_data;
		self.key = self.db_data.key;
		self.onLoad();
		return self;
	pass
	def onLoad(self): ...
	def unlock(self): ...
	
	@classmethod
	def create(cls, user: User) -> Element: ...
	def delete(self): ...
pass
