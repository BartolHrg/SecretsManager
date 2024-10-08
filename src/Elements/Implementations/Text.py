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



from ..Element import *;
from ...Algorithms.Algorithm import SealAlgorithm, Secret;
from ...ByteChunks import SimpleByteChunks;
from ...Storage import argsToBytes, bytesToArgs;

class Text(Element):
	element_type = 2;
	text: str;
	original: str | None = None;
	@property
	def header(self) -> bytes: return self.db_data.name.encode("UTF-8");
	def save(self, force = False):
		db_data = self.db_data;
		db_data.name = self.name;
		if not force and db_data.id is not None: # not forced and not new
			if self.original is None: return; # not loaded
			if self.text == self.original: return;
		pass
		data = SimpleByteChunks(self.text.encode("UTF-8"));
		sealed = SealAlgorithm.seal(data, self.db_data.user.mkey, self.header);
		db_data.algorithm = sealed.algorithm_id;
		db_data.data = argsToBytes(sealed.data.get, sealed.salt, sealed.hash);
		self.original = self.text;
		db_data.db.dataSave(db_data);
	pass
	def unlock(self):
		(data, salt, hash) = bytesToArgs(self.db_data.data);
		secret = Secret(SimpleByteChunks(data), salt, hash, self.db_data.algorithm);
		unsealed = SealAlgorithm.unseal(secret, self.db_data.user.mkey, self.header).get;
		text = unsealed.decode("UTF-8");
		self.text = self.original = text;
	pass
	@classmethod
	def create(cls, vault: Vault) -> Text:
		self = cls();
		self.name = "";
		self.vault = vault;
		self.original = self.text = "";
		self.db_data = DbData(None, "", 0, self.element_type, b"", vault);
	pass
	def delete(self):
		self.db_data.db.dataDelete(self.db_data.id);
	pass
pass
