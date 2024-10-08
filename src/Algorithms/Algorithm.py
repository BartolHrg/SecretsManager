from __future__ import annotations;

from dataclasses import dataclass;

from ..ByteChunks import ByteChunks;
from ..User import User;

__all__ = ("LoginAlgorithm", "SealAlgorithm", "Secret", "User", "ByteChunks");

@dataclass
class Secret:
	data: ByteChunks;
	salt: bytes;
	hash: bytes;
	algorithm_id: int;
pass

class _Algorithm:
	algorithms: dict[int, _Algorithm];
	deprecated: dict[int, int];
	id: int;
	deprecated_replacement: int | None = None;
	description: str;
	
	def __init_subclass__(cls):
		if not hasattr(cls, "id"): 
			assert False, f"You forgot id in {cls}";
		elif cls.id is None: 
			cls.algorithms = {};
			cls.deprecated = {};
			return;
		pass
		assert cls.id not in cls.algorithms.keys(), "Duplicate id for {cls}";
		cls.algorithms[cls.id] = cls();
		if cls.deprecated_replacement is not None: 
			cls.deprecated[cls.id] = cls.deprecated_replacement;
		pass
	pass
pass

class LoginAlgorithm(_Algorithm):
	id = None;
	current: int = 0;
	
	@staticmethod
	def register(user: User, mpass: str): 
		if user.algorithm is None: user.algorithm = LoginAlgorithm.current;
		algorithm = LoginAlgorithm.algorithms[user.algorithm];
		algorithm.register(user, mpass);
		assert user.mkey is not None;
	pass
	@staticmethod
	def login   (user: User, mpass: str) -> bool:
		algorithm = LoginAlgorithm.algorithms[user.algorithm];
		if not algorithm.login(user, mpass): return False;
		assert user.mkey is not None;
		return True;
	pass
pass


class SealAlgorithm(_Algorithm):
	id = None;
	default: int = 0;
	
	@staticmethod
	def   seal(data  : ByteChunks, key: bytes, header: bytes = None, algorithm_id: int = None) -> Secret    : 
		if algorithm_id is None: algorithm_id = SealAlgorithm.default;
		algorithm = SealAlgorithm.algorithms[algorithm_id];
		secret: Secret = algorithm.seal(data, key);
		secret.algorithm_id = algorithm_id;
		return secret;
	pass
	@staticmethod
	def unseal(secret: Secret    , key: bytes, header: bytes = None) -> ByteChunks:
		algorithm = SealAlgorithm.algorithms[secret.algorithm_id];
		return algorithm.unseal(secret, key);
	pass
	
	@staticmethod
	def getRandomBytes(n_bytes: int) -> bytes:
		algorithm = SealAlgorithm.algorithms[SealAlgorithm.default];
		return algorithm.getRandomBytes(n_bytes);
	pass
pass

