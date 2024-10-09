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



import json, subprocess;
from urllib import request;
from tkinter import messagebox;

from .Misc import Globals;
# pip install <package_name>==<version>

TITLE = "SecretsManager - Update System";

class VersionInfo(TypedDict):
	app: str;
	algorithms: str;
	crypto: str;
pass

def runUpdates():
	with open(__actual_dir__ + "/" + "../config/version.json") as f: version_here: VersionInfo = json.load(f);
	version_online = loadOnlineVersion() or version_here;
	
	if (False
		or version_here["app"       ] != version_online["app"       ] and messagebox.askyesno(TITLE, f"A new version of the app is available {            version_here['app'       ]} -> {version_online['app'       ]}")
		or version_here["algorithms"] != version_online["algorithms"] and messagebox.askyesno(TITLE, f"A new version of the CORE ALGORITHMS is available {version_here['algorithms']} -> {version_online['algorithms']}\nThis will also update the app")
	):
		if updateApp() is Exception:
			messagebox.showerror(TITLE, "Could not update app to the latest version\nMaybe you don't have git installed\nYou can update to the latest version manually");
		pass
	pass

	if version_here["crypto"] != version_online["crypto"] or not tryImportCrypto():
		match updateCrypto(version_online["crypto"]):
			case True: version_here["crypto"] = version_online["crypto"];
			case Exception: messagebox.showwarning(TITLE, "Could not update Cryptographic dependancy to the latest version");
		pass
	pass

	with open(__actual_dir__ + "/" + "../config/version.json", "w") as f: json.dump(version_here, f);
pass

def loadOnlineVersion() -> Optional[VersionInfo]:
	url = "https://raw.github.com/BartolHrg/SecretsManager/main/config/version.json"
	try:
		with request.urlopen(url) as response:
			if response.status == 200:
				content = response.read().decode('utf-8')
				return json.loads(content);
			else:
				messagebox.showwarning(TITLE, ""
					+  "Could not check for updates\n" 
					+ f"Request failed with status code: {response.status}\n"
					+  "Continuing with current version"
				);
			pass
		pass
	except Exception as e:
		messagebox.showwarning(TITLE, ""
			+  "Could not check for updates\n" 
			+ f"Something happened\n"
			+  "Continuing with current version"
		);
	pass
pass

def updateApp():
	try:
		if subprocess.run(["git", "pull", "origin", "main"], cwd = Globals.ROOT).returncode == 0:
			sys.exit(subprocess.run([sys.executable, Globals.ROOT + "/SecretsManager.pyw"]));
		else: 
			return Exception;
		pass
	except:
		return Exception;
	pass
pass

def tryImportCrypto() -> bool:
	try: import dependencies.Crypto;
	except ImportError: return False;
	else: return True;
pass
def updateCrypto(new_version):
	try:
		if subprocess.run(["pip", "install", f"pycryptodome=={new_version}", "--target", f"{Globals.ROOT}/dependencies/"], cwd = Globals.ROOT, stderr=subprocess.PIPE, stdout=subprocess.PIPE).returncode == 0:
			return True;
		else:
			return Exception;
		pass
	except:
		return Exception;
	pass
pass

runUpdates();
