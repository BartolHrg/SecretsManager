from __future__ import annotations;
from typing import TYPE_CHECKING;

from ..Element import *;
from ...Algorithms.Algorithm import SealAlgorithm, Secret;
from ...ByteChunks import SimpleByteChunks;
from ...Storage import argsToBytes, bytesToArgs, Database;
from ...Vault import Vault;


class VaultElement(Element):
	element_type = 1;
	mpass_part: bytes | None = None;
	sub_vault: Vault | None = None;
	@property
	def header(self) -> bytes: return self.db_data.name.encode("UTF-8");
	def save(self, force = False):
		db_data = self.db_data;
		db_data.name = self.name;
		if not force and db_data.id is not None: # not forced and not new
			if self.mpass_part is None: return; # not loaded
		pass
		# TODO mpass_part might be none
		data = SimpleByteChunks(self.mpass_part);
		sealed = SealAlgorithm.seal(data, self.db_data.user.mkey, self.header);
		db_data.algorithm = sealed.algorithm_id;
		db_data.data = argsToBytes(sealed.data.get, sealed.salt, sealed.hash);
		db_data.db.dataSave(db_data);
	pass
	def unlock(self):
		(data, salt, hash) = bytesToArgs(self.db_data.data);
		secret = Secret(SimpleByteChunks(data), salt, hash, self.db_data.algorithm);
		unsealed = SealAlgorithm.unseal(secret, self.db_data.user.mkey, self.header).get;
		self.mpass_part = unsealed;
	pass
	@classmethod
	def create(cls, vault: Vault) -> VaultElement:
		self = cls();
		self.name = "";
		self.mpass_part = SealAlgorithm.getRandomBytes(32);
		self.db_data = DbData(None, "", 0, self.element_type, b"", vault);
	pass
	def delete(self):
		self.db_data.db.dataDelete(self.db_data.id);
	pass
pass
