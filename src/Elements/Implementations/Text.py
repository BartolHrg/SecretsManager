

from ..Element import *;
from ...Algorithms.Algorithm import SealAlgorithm, Secret;
from ...ByteChunks import SimpleByteChunks;
from ...Storage import argsToBytes, bytesToArgs;

class Text(Element):
	element_type = 1;
	text: str;
	original: str | None = None;
	def save(self, force = False):
		if not force and self.db_data.id is not None:
			if self.original is None: return; # not loaded
			if self.text == self.original: return;
		pass
		data = SimpleByteChunks(self.text.encode("utf-8"));
		sealed = SealAlgorithm.seal(data, b"TODO", SealAlgorithm.default);
		db_data = self.db_data;
		db_data.algorithm = sealed.algorithm_id;
		db_data.key = self.key;
		db_data.data = argsToBytes(sealed.data.get, sealed.salt, sealed.hash);
		self.original = self.text;
		db_data.db.dataSave(db_data);
	pass
	def unlock(self):
		(data, salt, hash) = bytesToArgs(self.db_data.data);
		secret = Secret(SimpleByteChunks(data), salt, hash, self.db_data.algorithm);
		unsealed = SealAlgorithm.unseal(secret, b"TODO").get;
		text = unsealed.decode("utf-8");
		self.text = self.original = text;
	pass
	@classmethod
	def create(cls, user: User) -> Text:
		self = cls();
		self.key = "";
		self.original = self.text = "";
		self.db_data = DbData(None, "", 0, self.element_type, b"", user);
	pass
	def delete(self):
		self.db_data.db.dataDelete(self.db_data.id);
	pass
pass
