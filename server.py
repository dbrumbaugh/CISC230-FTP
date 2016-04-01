import socket
import os
import sys
import hashlib
import math
from Crypto.Cipher import AES

#high-level config options:

root_dir = os.getcwd() + "\\server-root"
port     = 21
host_add = socket.gethostname()
password_file = os.getcwd() + "\\shadow"
key_file      = os.getcwd() + "\\key"
buffer_size   = 1024 

AES_key =""
AES_iv  =""

def encrypt(plain_text, key, iv):
  aes_crypt  = AES.new(key, AES.MODE_CBC, iv)
  length     = 16 - (len(plain_text) % 16)
  for i in range(length):
    plain_text += chr(length)

  cipher_text = ""

  for i in range(int(math.ceil(len(plain_text)/16.0))):
    print(str(len(plain_text[16*i:16*i+16])))
    encoded = aes_crypt.encrypt(plain_text[16*i:16*i+16])
    cipher_text += encoded

  return cipher_text

def decrypt(cipher_text, key, iv):
  aes_crypt = AES.new(key, AES.MODE_CBC, iv)

  plain_text = ""
  for i in range(int(math.ceil(len(cipher_text)/16.0))):
    plain_part = aes_crypt.decrypt(cipher_text[16*i:16*i+16])
    plain_text += plain_part

  if ord(str(plain_text[-1])) < 16:
      text_list = list(plain_text)
      padding = plain_text[-1]
      while str(text_list[-1]) == str(padding):
        del text_list[-1]
      plain_text = "".join(text_list)
	  
  return plain_text

#Python server file for CISC230 Project
#Barebones version--I'll update for multithreading support once I get home tonight

def validate_credentials(username, password):
  username = decrypt(username, AES_key, AES_iv)
  password = decrypt(password, AES_key, AES_iv)

  print(username)
  print(password)

  try:
    f =  open("shadow", "r")
  except:
    print("[E] Unable to open password file.")
    return False

  f_username = "default"
  while f_username:
    f_username = f.readline().strip()
    f_password = f.readline().strip()
    print(f_username)

    if f_username == username:
      s = hashlib.sha1()
      s.update(password.strip())
      if(s.digest().strip() == f_password.strip()):
	print("[I] Credentials validated")
        return True
  print("[I] Credentials Rejected")        
  return False
  #temp for testing
#  if(username == "test" and password == "password"):
    #print("[I] Connection validated")
#    return True
#  else:
#    print("[I] Credentials rejected")
#    return False

def get_and_process_function(session, working_dir):
  function = session.recv(buffer_size)
  print("[I] Function request recieved from client: " + function)

  args = function.split(" ", 1)
  func = args[0]
  try:
    arg  = args[1]
  except:
    print("[I] Single argument function request")

  if (func == "dir"):
    stat = dirl(session, working_dir)
    return stat, working_dir
  elif (func == "cd"):
    stat, working_dir = cd(session, arg, working_dir)
    return stat, working_dir
  elif (func == "get"):
    stat = get(session, arg, working_dir)
    return stat, working_dir
  elif (func == "put"):
    stat = put(session, arg, working_dir)
    return stat, working_dir
  elif (func == "exit"):
    stat = exit(session)
    return stat, working_dir
  else:
    print("[E] Invalid function request recieved.")
    stat = -1
    return stat, working_dir

def exit(session):
  session.close()
  print("[I] Session Terminated at client's request.")
  return 1

def dirl(session, working_dir):
  try:
    dir_lst = os.listdir(str(working_dir))
    
    count = len(dir_lst)
    trans_string = ""
    if count > 0:
      for i in xrange(count):
        trans_string = trans_string + str(dir_lst[i]) + "*"
    else:
      trans_string = "*"

    print("[I] Sending string over connection.")
    print("[I] " + trans_string)
    session.send(trans_string)

    return 0
  except:
    print("[E] Exceptional condition in execution of dir instruction")
    typ, val, traceback = sys.exc_info()
    print("[E] " + str(typ) + " " + str(val) + " " + str(traceback))
    return -1

def cd(session, arg, working_dir):
  backup = working_dir
  try:
    if (arg == ".."):
      dir_lst = working_dir.split("\\")
      dir_lst = filter(None, dir_lst)
      length = len(dir_lst)
      working_dir = ""
      print("[D]: " + str(dir_lst))

      for i in range(length - 1):
	if(i == length - 1):
	  working_dir = working_dir + str(dir_lst[i])
	else:
          working_dir = working_dir + str(dir_lst[i]) + "\\"
	print("[I] New directory is: " + working_dir)

      if (os.path.isdir(working_dir)):
	if (len(working_dir) < len(root_dir)):
	    session.send("A")
	    return -2, backup
	else:
          session.send("Y")
          return 0, working_dir
      else:
        session.send("N")
	return -1, backup

    else:
      working_dir = working_dir + "\\" + arg
      
      if (os.path.isdir(working_dir)):
        session.send("Y")
        return 0, working_dir
      else:
	session.send("N")
	return -1, backup

  except:
    session.send("N")
    return -1, backup

def put(session, arg, working_dir):
    try:
      f = open(working_dir + "\\" + arg, "wb")
      print("[I] File at " + working_dir + "\\" + arg +" opened.")
      session.send('Y')
    except:
      print("[E] Unable to open file " + working_dir + "\\" + art)
      session.send("N")
      return 0

    length = str(session.recv(buffer_size)).strip()
    data_length = 0

    try:
      data_length = int(float(length))
      print("[I] Incoming file of length: " + str(data_length) +" kb")
      session.send("Y")
    except:
      e = sys.exc_info()
      print(str(e))
      print("[E] Invalid file length recieved: " + str(length))
      session.send("N")

    for i in range(int(data_length)):
      data_segment = session.recv(buffer_size)
      print("[I] Recieved segment: " + str(i))
      #print("[I]" + str(data_segment))
      f.write(data_segment)
      print("[I] Writing segment" + str(i) +" to file")

    f.close()
    return 0

def get(session, filename, working_dir):
#send specified file to server

  get_path = str(working_dir + "\\" + filename)

  try:
    f = open(get_path, "rb")
    session.send("Y")

  except:
    print("[E] Cannot open local file: " + get_path)
    session.send("N")
    return 0

  #all is good, begin sending file
  print("[I] Begin processesing GET request.")
  length = 0
  try:
    length = math.ceil(float(os.path.getsize(get_path))/1024)
    print("[I] File of length: " + str(length) + " kb")
    session.send(str(length))

  except:
    e = sys.exc_info()
    print(str(e))

  cstat = session.recv(1)

  if(cstat == 'Y'):
    print("[I] File length accepted by client.")

  else:
    print("[E] File length rejected by client.")
    f.close()
    return 0

  data_segment = f.read(1024)

  while data_segment:
     session.send(data_segment)
     data_segment = f.read(1024)

     print("[I]" + str(data_segment))

  f.close()
 

def main():
  global AES_key
  global AES_iv

  try:
    f = open(key_file)
    AES_key = f.read(32)
    AES_iv  = f.read(16)
  except:
    print("[E] Unable to access key file: " + key_file)

  host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host_socket.bind((host_add, port))

  print("[I] Server socket opened and awaiting connection.")

  while True:
    host_socket.listen(1)

    session, ip_address = host_socket.accept()
    print("[I] Connection recieved from " + str(ip_address))
    working_dir = root_dir

    while True:
      username = session.recv(1024)
      password = session.recv(1024)

      valid = validate_credentials(username, password)
      if (valid):
	session.send("Y")
	break
      else:
	session.send("N")
	continue
    stat = 0
    while not stat == 1:
      stat, working_dir = get_and_process_function(session, working_dir)










main()
