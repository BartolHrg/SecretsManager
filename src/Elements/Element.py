from __future__ import annotations;
from typing import TYPE_CHECKING;

from ..Storage import DbData;

if TYPE_CHECKING:
	from ..Vault import Vault;
pass

class Element:
	element_types: dict[int, type[Element]] = {};
	element_type: int;
	db_data: DbData;
	name: str;
	vault: Vault;
	
	def __init_subclass__(cls):
		assert hasattr(cls, "element_type");
		assert cls.element_type not in cls.element_types.keys();
		cls.element_types[cls.element_type] = cls;
		assert cls.create is not Element.create, f"Class {cls} didn't implement create";
	pass

	def save(self, force = False): ...
	@staticmethod
	def load(db_data: DbData, vault: Vault) -> Element:
		element_type = db_data.kind;
		cls = Element.element_types[element_type];
		self = cls();
		self.name = db_data.name;
		self.db_data = db_data;
		self.vault = vault;
		self.onLoad();
		return self;
	pass
	def onLoad(self): ...
	def unlock(self): ...
	
	@classmethod
	def create(cls, vault: Vault) -> Element: ...
	def delete(self): ...
pass
