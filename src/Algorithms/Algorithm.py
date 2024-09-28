from __future__ import annotations;

from dataclasses import dataclass;

from ..Misc import BytesChunk;
from ..User import User;

__all__ = ("LoginAlgorithm", "SealAlgorithm", "Secret", "User", "BytesChunk");

@dataclass
class Secret:
	data: BytesChunk;
	salt: bytes;
	hash: bytes;
	algorithm_id: int;
pass

class _Algorithm:
	algorithms: dict[int, Algorithm];
	deprecated: dict[int, int];
	id: int;
	deprecated_replacement: int | None = None;
	description: str;
	
	def __init_subclass__(cls):
		if not hasattr(cls, "id"): 
			assert False, f"You forgot id in {cls}";
		elif cls.id is None: return;
		pass
		cls.algorithms[cls.id] = cls();
		if cls.deprecated_replacement is not None: 
			cls.deprecated[cls.id] = cls.deprecated_replacement;
		pass
	pass
pass

class LoginAlgorithm(_Algorithm):
	id = None;
	algorithms: dict[int, LoginAlgorithm] = {};
	deprecated: dict[int, int] = {};
	current: int = 0;
	
	@staticmethod
	def register(user: User, mpass: str): 
		algorithm_id = user.algorithm if user.algorithm is not None else self.current;
		algorithm = self.algorithms[algorithm_id];
		algorithm.register(user, mpass);
		assert user.mkey is not None;
	pass
	@staticmethod
	def login   (user: User, mpass: str) -> bool:
		algorithm_id = user.algorithm;
		algorithm = self.algorithms[algorithm_id];
		if not algorithm.login(user, mpass): return False;
		assert user.mkey is not None;
		return True;
	pass
pass


class SealAlgorithm(_Algorithm):
	id = None;
	algorithms: dict[int, SealAlgorithm] = {};
	deprecated: dict[int, int] = {};
	default: int = 0;
	
	@staticmethod
	def   seal(data  : BytesChunk, key: bytes, algorithm_id: int = None) -> Secret    : 
		if algorithm_id is None: algorithm_id = self.default;
		algorithm = self.algorithms[algorithm_id];
		secret: Secret = algorithm.seal(data, key);
		secret.algorithm_id = algorithm_id;
		return secret;
	pass
	@staticmethod
	def unseal(secret: Secret    , key: bytes) -> BytesChunk:
		algorithm = self.algorithms[secret.algorithm_id];
		return algorithm.unseal(secret, key);
	pass
pass

