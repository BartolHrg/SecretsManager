from typing import *;

import tkinter as tk;
from tkinter import ttk;
from tkinter import messagebox;

from ..Storage import Database;
from ..Algorithms.Algorithm import LoginAlgorithm;
from ..User import User;
from .Window import *;

MSG_TITLE = "SecretsManager - Login"

class LoginType:
	REGISTER = 0;
	LOGIN = 1;
pass

class LoginView:
	def __init__(self, master: Window | None, db: Database, login_type: LoginType, onSubmit: Callable[[User, LoginType], None], onCancel: Callable[[], None], username: str | None = None):
		self.destroyed = False;
		self.window = makeWindow(master);
		
		self.db = db;
		self.onSubmit = onSubmit;
		self.onCancel = onCancel;
		
		self.username_var = tk.StringVar(self.window, username or "");
		self.   mpass_var = tk.StringVar(self.window, "");
		self.  repeat_var = tk.StringVar(self.window, "");
		
		frame = tk.Frame(self.window);
		frame.pack(expand = True, fill = tk.BOTH);
		
		self.username_label = ttk.Label(frame, text = "Username"       );
		self.   mpass_label = ttk.Label(frame, text = "Password"       );
		self.  repeat_label = ttk.Label(frame, text = "Repeat");
		self.username_label.grid(row = 1, column = 0, sticky = tk.E);
		self.   mpass_label.grid(row = 2, column = 0, sticky = tk.E);
		self.  repeat_label.grid(row = 3, column = 0, sticky = tk.E);
		
		self.username_entry = tk.Entry(frame, textvariable = self.username_var, state = tk.NORMAL if username is None else tk.DISABLED);
		self.   mpass_entry = tk.Entry(frame, textvariable = self.   mpass_var, show = "*");
		self.  repeat_entry = tk.Entry(frame, textvariable = self.  repeat_var, show = "*");
		self.username_entry.grid(row = 1, column = 1, sticky = tk.NSEW);
		self.   mpass_entry.grid(row = 2, column = 1, sticky = tk.NSEW);
		self.  repeat_entry.grid(row = 3, column = 1, sticky = tk.NSEW);
		
		self. mpass_show_toggle = tk.Button(frame, text = "👁", width = 2, command = lambda: self.toggleShow(0));
		self.repeat_show_toggle = tk.Button(frame, text = "👁", width = 2, command = lambda: self.toggleShow(1));
		self. mpass_show_toggle.grid(row = 2, column = 2);
		self.repeat_show_toggle.grid(row = 3, column = 2);
		
		frame.columnconfigure(1, weight = 1);
		
		buttons = tk.Frame(self.window);
		buttons.pack(fill = tk.Y, side = tk.BOTTOM);
		
		self.submit_button = ttk.Button(buttons, text = "Login", command = self.login);
		self.submit_button.pack(side = tk.LEFT);
		self.switch_button = ttk.Button(buttons, text = "Register instead", command = self.switch);
		if username is None:
			self.switch_button.pack(side = tk.LEFT);
		pass
		
		self.login_type = login_type;
		
		self.window.bind("<Destroy>", self.onDestroyEvent);
		self.window.update();
		self.window.update_idletasks();
		self.window.geometry("350x100");
	pass
	def switch(self, *_):
		self.login_type = not self.login_type;
	pass
	def toggleShow(self, what: int):
		entry = self.mpass_entry if what == 0 else self.repeat_entry;
		if entry["show"]: entry["show"] = "";
		else:             entry["show"] = "*";
	pass
	@property
	def login_type(self): return self._login_type;
	@login_type.setter
	def login_type(self, value: LoginType): 
		self._login_type = value;
		if value == LoginType.LOGIN:
			self.window.title("Login - SecretsManager");
			self.repeat_label      .grid_remove();
			self.repeat_entry      .grid_remove();
			self.repeat_show_toggle.grid_remove();
			self.submit_button.config(text = "Login", command = self.login);
			self.switch_button.config(text = "Register Instead");
		else:
			self.window.title("Register - SecretsManager");
			self.repeat_label      .grid();
			self.repeat_entry      .grid();
			self.repeat_show_toggle.grid();
			self.submit_button.config(text = "Register", command = self.register);
			self.switch_button.config(text = "Login Instead");
		pass
	pass
	
	def login(self, *_):
		username = self.username_var.get();
		mpass    = self.   mpass_var.get();
		with self.db:
			if not self.db.userExists(username):
				messagebox.showerror(MSG_TITLE, f"User <{username}> does not exist");
				return;
			pass
			user = self.db.userGet(username);
		pass
		if not LoginAlgorithm.login(user, mpass):
			messagebox.showerror(MSG_TITLE, "Wrong username or password");
			return;
		pass
		self.destroyed = True;
		self.window.destroy();
		self.onSubmit(user, LoginType.LOGIN);
	pass
	
	def register(self, *_):
		if not messagebox.askokcancel(MSG_TITLE, "Do you want to create a new user?"): return;
		username = self.username_var.get();
		mpass    = self.   mpass_var.get();
		repeat   = self.  repeat_var.get();
		if mpass != repeat:
			messagebox.showerror(MSG_TITLE, "Password does not match repeated password");
			return;
		pass
		with self.db:
			if self.db.userExists(username):
				messagebox.showerror(MSG_TITLE, f"User <{username}> already exists");
				return;
			pass
			user = User(None, username, None, None, None, "", None);
			LoginAlgorithm.register(user, mpass);
			self.db.userSave(user, True);
		pass
		self.destroyed = True;
		self.window.destroy();
		self.onSubmit(user, LoginType.REGISTER);
	pass
	
	def onDestroyEvent(self, *_):
		if self.destroyed: return;
		self.destroyed = True;
		self.onCancel();
	pass
pass


