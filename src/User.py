

from dataclasses import dataclass;

@dataclass
class DbUser:
	id: int;
	username: str;
	algorithm: int;
	msalt: bytes;
	mhash: bytes;
pass

@dataclass
class User(DbUser):
	mkey: bytes;
pass
