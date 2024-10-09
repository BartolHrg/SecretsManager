from __future__ import annotations;
from typing import TYPE_CHECKING;

from dataclasses import dataclass;

if TYPE_CHECKING:
	from .Storage import Database;
pass

@dataclass
class DbUser:
	id: int;
	username: str;
	algorithm: int;
	msalt: bytes;
	mhash: bytes;
	sub_db_path: str;
pass

@dataclass
class User(DbUser):
	mkey: bytes;
pass
