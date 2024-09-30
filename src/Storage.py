from __future__ import annotations;

import sys, os;
import uuid;
import sqlite3;
from dataclasses import dataclass;

from .Misc import Constants;
from .User import User, DbUser;

if len(sys.argv) == 1:
	storage_root = Constants.ROOT + "/storage/";
elif len(sys.argv) == 2:
	storage_root = os.path.abspath(sys.argv[1]) + "/";
pass
if not os.path.exists(storage_root): os.mkdir(storage_root);
elif not os.path.isdir(storage_root): raise ValueError(f"The path provided as the first argument {sys.argv[1]} is not a valid path")

data_path = storage_root + "data/";
temp_path = storage_root + "temp/";
if not os.path.exists(data_path): os.mkdir(data_path);
if not os.path.exists(temp_path): os.mkdir(temp_path);

def generateAvailablePath(path = "", permanent = True):
	root = data_path if permanent else temp_path;
	path = root + path;
	if not os.path.isdir(path): raise ValueError(f"Provided path <{path}> is not under root <{root}>");
	while True:
		new_path = path + "/" + str(uuid.uuid4());
		if not os.path.exists(new_path): return new_path;
	pass
pass

@dataclass
class DbData:
	id: int;
	key: str;
	algorithm: int;
	kind: int;
	data: bytes;
	user: User;
	@property
	def db(self): return self.user.db;
pass

def argsToBytes(*args: bytes) -> bytes:
	serialized = b"";
	for arg in args:
		length = len(arg);
		serialized += str(length).encode("ascii") + b":" + arg;
	pass
	serialized += b":";
	return serialized;
pass
def bytesToArgs(serialized: bytes) -> list[bytes]:
	result = [];
	i = 0;
	while True:
		index = serialized.index(b":", i);
		if index == i: break;
		length = serialized[i : index];
		i = index + 1;
		length = int(length.decode("ascii"));
		index = i + length;
		result.append(serialized[i : index]);
		i = index;
	pass
	return result;
pass

class Database:
	def __init__(self, path = "main.db"):
		if not path.startswith(data_path): path = data_path + path;
		self.path = path;
		with self: self.cursor.executescript(Database.Statements.INIT);
	pass

	def open(self):
		self.connection = sqlite3.connect(self.path);
		self.cursor = self.connection.cursor();
	pass
	def close(self):
		self.cursor.close();
		self.connection.close();
	pass
	def __enter__(self, *_): self.open();
	def __exit__(self, *_): self.close();
	
	def userExists(self, username: str) -> bool:
		self.cursor.execute(self.Statements.User.EXISTS, (username, ));
		return bool(self.cursor.fetchone()[0]);
	pass
	def userSave(self, user: DbUser, is_new: bool = None):
		if is_new is None: is_new = user.id is None;
		if is_new:
			self.cursor.execute(self.Statements.User.SAVE_NEW, (user.username, user.algorithm, user.msalt, user.mhash, ));
			user.id = self.cursor.lastrowid;
		else:
			self.cursor.execute(self.Statements.User.SAVE_OLD, (user.username, user.algorithm, user.msalt, user.mhash, user.id, ));
		pass
		self.connection.commit();
	pass
	def userGet(self, username: str) -> User: 
		self.cursor.execute(self.Statements.User.GET, (username, ));
		(id, username, algorithm, msalt, mhash) = self.cursor.fetchone();
		return User(id, username, algorithm, msalt, mhash, self, None);
	pass
	def userGetUsernames(self) -> list[str]: 
		self.cursor.execute(self.Statements.User.GET_USERNAMES);
		rows = self.cursor.fetchall();
		return [username for (username, ) in rows];
	pass
	def userDelete(self, username: str): 
		self.cursor.execute(self.Statements.User.DELETE, (username, ));
		self.connection.commit();
	pass
	
	def dataExists(self, user: DbUser, key: str) -> bool:
		self.cursor.execute(self.Statements.Data.EXISTS, (user.id, key, ));
		return bool(self.cursor.fetchone()[0]);
	pass
	def dataSave(self, data: DbData, is_new: bool = None):
		user = data.user;
		if is_new is None: is_new = data.id is None;
		if is_new:
			self.cursor.execute(self.Statements.Data.SAVE_NEW, (user.id, data.key, data.algorithm, data.kind, data.data, ));
			data.id = self.cursor.lastrowid;
		else:
			self.cursor.execute(self.Statements.Data.SAVE_OLD, (data.key, data.algorithm, data.kind, data.data, data.id, user.id));
		pass
		self.connection.commit();
	pass
	def dataGetUserOwned(self, user: DbUser) -> list[DbData]: 
		self.cursor.execute(self.Statements.Data.GET_USER_DATAS, (user.id, ));
		rows = self.cursor.fetchall();
		return [DbData(id, key, algorithm, kind, data, user) for (id, user_id, key, algorithm, kind, data,) in rows];
	pass
	def dataDelete(self, id: int): 
		self.cursor.execute(self.Statements.Data.DELETE, (id, ));
		self.connection.commit();
	pass
	def dataDeleteUserOwned(self, user: DbUser): 
		self.cursor.execute(self.Statements.Data.DELETE_USER_DATAS, (user.id, ));
		self.connection.commit();
	pass

	class Statements:
		INIT = """
			PRAGMA foreign_keys = ON;
			CREATE TABLE IF NOT EXISTS User (
				my_id        INTEGER PRIMARY KEY ,
				my_username  TEXT    UNIQUE      ,
				my_algorithm INTEGER             ,
				my_msalt     BLOB                ,
				my_mhash     BLOB
			) STRICT;
			CREATE TABLE IF NOT EXISTS Data (
				my_id        INTEGER PRIMARY KEY ,
				user_id      TEXT    REFERENCES User(my_id) ON DELETE RESTRICT  ,
				my_key       TEXT                ,
				my_algorithm INTEGER             ,
				my_kind      INTEGER             ,
				my_data      BLOB                ,
				UNIQUE (user_id, my_key)
			) STRICT;
		""";
		class User:
			EXISTS = """ SELECT EXISTS(SELECT 1 FROM User WHERE my_username=?); """;
			SAVE_NEW = """ INSERT INTO User (my_username, my_algorithm, my_msalt, my_mhash) VALUES(?, ?, ?, ?); """; # use lastrowid
			SAVE_OLD = """
				UPDATE User
				SET my_username=?, my_algorithm=?, my_msalt=?, my_mhash=?
				WHERE my_id=?
			""";
			GET = """ SELECT * FROM User WHERE my_username=? """;
			GET_USERNAMES = """ SELECT my_username FROM User """;
			DELETE = """ DELETE FROM User WHERE my_username=? """;
		pass
		class Data:
			EXISTS = """ SELECT EXISTS(SELECT 1 FROM Data WHERE user_id=? AND my_key=?); """;
			SAVE_NEW = """ INSERT INTO Data (user_id, my_key, my_algorithm, my_kind, my_data) VALUES(?, ?, ?, ?, ?); """; # use lastrowid
			SAVE_OLD = """
				UPDATE Data
				SET my_key=?, my_algorithm=?, my_kind=?, my_data=?
				WHERE my_id=? AND user_id=?
			""";
			GET_USER_DATAS = """ SELECT * FROM Data WHERE user_id=? """;
			DELETE = """ DELETE FROM Data WHERE my_id=? """;
			DELETE_USER_DATAS = """ DELETE FROM Data WHERE user_id=? """;
		pass
	pass
pass