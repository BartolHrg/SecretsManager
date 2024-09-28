from __future__ import annotations;


class Element:
	element_types: dict[int, type[Element]] = {};
	element_type: int;
	
	def __init_subclass__(cls):
		cls.algorithms[cls.id] = cls;
	pass
pass
