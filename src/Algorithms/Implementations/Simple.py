

# print(__name__, __package__, __file__, "======================", sep = "\n");
from ..Algorithm import *;

class SimpleLogin(LoginAlgorithm):
	id = 0;
	description = "Unsecure - Plain Text"
	# deprecated_replacement = ...
	@staticmethod
	def register(user: User, mpass: str): 
		user.mkey  = b"key";
		user.msalt = b"salt";
		user.mhash = b"hash";
	pass
	@staticmethod
	def login(user: User, mpass: str) -> bool: 
		user.mkey  = b"key";
		return True;
	pass
pass
class SimpleSeal(SealAlgorithm):
	id = 0;
	description = "Unsecure - Plain Text"
	# deprecated_replacement = ...
	@staticmethod
	def seal(data: ByteChunks, key: bytes, header: bytes = None) -> Secret    : return Secret(data, b"", b"");
	@staticmethod
	def unseal(secret: Secret, key: bytes, header: bytes = None) -> ByteChunks: return secret.data;
	@staticmethod
	def getRandomBytes(n_bytes: int) -> bytes: return b"7" * n_bytes;
pass
