import random
import os
import hashlib

class Connector():
    def __init__(self, file_name, rep = os.getcwd()):
        self.file_path = os.path.join(rep, file_name)
        if file_name.split(".")[-1] != "txt":
            raise Exception("Error: Connector just support txt files")
            return 0
        self.content = self.connect(self.file_path)
    
    def get_usernames(self):
        if not ";" in self.content[0]:
            raise Exception(self.file_path+"doesn't content usernames")
            return 0
        all_val = list(map(lambda val: val.replace("\n", "").split(";"), self.content))
        return [all_val[i][0] for i in range(len(all_val))]
    
    def get_passwords(self):
        if not ";" in self.content[0]:
            raise Exception(self.file_path+"doesn't content passwords")
            return 0
        all_val = list(map(lambda val: val.replace("\n", "").split(";"), self.content))
        return [all_val[i][1] for i in range(len(all_val))]
    
    def get_username(self):
        if not ";" in self.content[0]:
            raise Exception(self.file_path+"doesn't content username")
            return 0
        all_val = list(map(lambda val: val.replace("\n", "").split(";"), self.content))
        return [all_val[i][0] for i in range(len(all_val))]
    
    def get_score(self):
        if not ";" in self.content[0]:
            raise Exception(self.file_path+"doesn't content score")
            return 0
        all_val = list(map(lambda val: val.replace("\n", "").split(";"), self.content))
        return [all_val[i][1] for i in range(len(all_val))]
    
    def get_time(self):
        if not ";" in self.content[0]:
            raise Exception(self.file_path+"doesn't content time")
            return 0
        all_val = list(map(lambda val: val.replace("\n", "").split(";"), self.content))
        return [all_val[i][2] for i in range(len(all_val))]
    
    def connect(self, file_path):
        with open(file_path) as self.f:
            return [line for line in self.f.readlines()]
    
    def check_username_password(self, username, password):
        if ((not username in self.get_usernames()) or (not password in self.get_passwords())):
            self.error_msg = "the Username or password is incorrect"
            return False
        else:
            return True
    
    def add(self, value):
        self.f.close()
        with open(self.file_path, 'a') as f:
            f.write(value)
            self.f.close()
            return True
        return False
    
    def set_username_password(self, username, password):
        return self.add(username+";"+password+"\n")
    
    def set_leaderbord(self, username, score, best_time):
        return self.add(username+";"+score+";"+best_time+"\n")
    
    def get_line(self, number):
        return self.content[number-1]
    
    def get_random_line(self):
        return self.get_line(random.randint(1,len(self.content)))
    
    def save_word(self, word):
        return self.add(word+"\n")

class SignUp_db():
	def __init__(self, username, password, min_size_username = 8, min_size_password = 4, max_size_username = 10, max_size_password = 10):
		self.username = str(username)
		self.password = str(password)
		self.min_size_username = min_size_username
		self.min_size_password = min_size_password
		self.max_size_username = max_size_username
		self.max_size_password = max_size_password
		self.error_msg = ''
		self.connector = Connector("db.txt")
		self.signup_state =self.error_msg 

		#check the username and the password
		if not self.check_username() or not self.check_password() or not self.is_username_available():
			self.signup_state =self.error_msg
		elif not self.save_user_info():
			self.signup_state =self.error_msg
		else:
			self.signup_state = 'OK'

	def get_signup_state(self):
		return self.signup_state

	def check_username(self):
		if len(self.username) < self.min_size_username :
			self.error_msg = "the Min size of the username is " + str(self.min_size_username)
			return False
		if len(self.username) > self.max_size_username :
			self.error_msg = "the Max size of the username is " + str(self.max_size_username)
			return False
		if " " in self.username.split() or " " in self.password.split():
			self.error_msg = "the Username or password can't contain space"
			return False
		return True

	def check_password(self):
		if len(self.password) < self.min_size_password :
			self.error_msg = "the Min size of the password is " + str(self.min_size_password)
			return False
		if len(self.password) > self.max_size_password :
			self.error_msg = "the Max size of the password is " + str(self.max_size_password)
			return False
		return True

	def is_username_available(self):
		if self.username in self.connector.get_usernames():
			self.error_msg = "Username exist"
			return False
		else:
			return True
		#get all the username from the db and compare

	def save_user_info(self):
		return self.connector.set_username_password(self.username, self.hash_password(self.password))
		#save the user in the db and return True if successful

	def hash_password(self, password):
		password = str(password) + "5gz"
		hashed = hashlib.md5(password.encode())
		return hashed.hexdigest()


class Login_db():
    def __init__(self, username, password):
        self.username = str(username)
        self.password = password
        self.error_msg = ''
        self.connector = Connector("db.txt")
        self.login_state = self.error_msg
        if self.is_correct_login():
            self.login_state = 'OK'
        else:
            self.login_state = self.error_msg

    def get_login_state(self):
        return self.login_state

    def is_correct_login(self):
        return self.check_username_password(self.username, self.hash_password(self.password))

    def hash_password(self, password):
        password = str(password) + "5gz"
        hashed = hashlib.md5(password.encode())
        return hashed.hexdigest()
    
    def check_username_password(self, username, password):
        if ((not username in self.connector.get_usernames()) or (not password in self.connector.get_passwords())):
            self.error_msg = "the Username or password is incorrect"
            return False
        else:
            return True