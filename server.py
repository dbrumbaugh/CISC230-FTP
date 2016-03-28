import socket
import os
import sys

#high-level config options:

root_dir = os.getcwd()
port     = 21
host_add = socket.gethostname()

#Python server file for CISC230 Project
#Barebones version--I'll update for multithreading support once I get home tonight

def validate_credentials(username, password):
  #Stephen's assignment. Search a password file for the submitted username, then validate that
  #passwords match (hash them). Return True for valid creds and false for invalid

  #temp for testing
  if(username == "test" and password == "password"):
    print("[I] Connection validated")
    return True
  else:
    print("[I] Credentials rejected")
    return False

def get_and_process_function(session, working_dir):
  function = session.recv(1024)
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
    stat = get(session)
    return stat, working_dir
  elif (func == "put"):
    stat = put(session)
    return stat, working_dir
  elif (func == "exit"):
    stat = ext(session)
    return stat, working_dir
  else:
    print("[E] Invalid function request recieved.")
    stat = -1
    return stat, working_dir


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
 

def main():
  host_socket = socket.socket()
  host_socket.bind((host_add, port))

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
