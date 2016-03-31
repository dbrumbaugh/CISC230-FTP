import socket
import math
import os
import sys

#Python client file for CISC230 Project

def establish_connection() :
  connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  while True:
    try:
      ip_address = raw_input("Please enter the IP address of the FTP server to which to connect: ")
      port = raw_input("Please enter the port number on which to connect: ")

      #test code
      #connection.connect((ip_address, port))
      connection.connect((socket.gethostname(),21))

      print("[I] Connection to " + ip_address + "successfully established.")
      break
    except:
      print("[E] Connection to server refused. Please ensure that the IP address and port number are correct, and that the server script is running on the host machine")

  return connection

def authenticate(connection):
  while True:
    name = raw_input("Please enter username: ")
    passwd = raw_input("Please enter password: ")

    connection.send(name)
    connection.send(passwd)

    authenticated = connection.recv(1)

    if (authenticated == 'Y'):
      print("[I] Authentication successful")
      break
    else:
      print("[E] Credentials rejected by server. Please try again.")
      continue

def get_function(connection):
  try:
    inp = raw_input("Please enter a function to perform [? for help]: ")

    args = inp.split(" ")
    func = args[0]

    if len(args) >= 2:
      arg1 = args[1]
    else:
      arg1 = ""

    if len(args) >=3:
      arg2 = args[2]
    else:
      arg2 = ""



    if(func == "dir"):
      dirl(connection)
      return 0

    elif(func == "cd"):
      cd(connection, arg1)
      return 0

    elif(func == "get"):
      get(connection, arg1, arg2)
      return 0

    elif(func == "put"):
      put(connection, arg1, arg2)
      return 0

    elif (func == "?"):
      print_help()
      return 0

    elif (func == "exit"):
      exit(connection)
      return -1

    else:
      print("Invalid function or function syntax")
      print_help()
      return 0

  except:
    exit(connection)
    print("[E] An exceptional condition has occured in the FTP client which is irrecoverable. The session has been terminated. Please restart the client and reconnect to the server.")

    return -1

def exit(connection):
  connection.send("exit")

def print_help():
  #print help dialogue
  print("Supported operations are:")
  print("Change Directory:\tcd <target directory>")
  print("List Directory contents:\tdir")
  print("Get file from server: \tget <source filename> <target filename>")
  print("Put file to server: \tput <source filename> <target filename>")
  print("End session: \t\texit")
  print("Show this message: \t?")

def dirl(connection):
  #list directory contents on server
  connection.send("dir")
  trans_string = connection.recv(5120)

  if trans_string[0] == "*":
    print("Directory Empty")
  else:  
    dir_lst = trans_string.split("*")
    count = len(dir_lst)
    for i in xrange(int(count)):
      print(str(dir_lst[i]))

def cd(connection, arg):
  print("[I] Function: CD, ARGS: " + str(arg))
  if arg == "":
    print("[E] No argument provided to CD function.")
    return
    
  connection.send("cd " + str(arg))
  sstat = str(connection.recv(1))

  if (sstat == "Y"):
    print("[I] CD Command executed successfully")
  elif (sstat == "A"):
    print("[A] Access violation on CD command. Access to requested directory is restricted.")
  else:
    print("[E] Exceptional condition in CD command. Ensure that desired directory exists and is properly spelled")

#def get(connection, arg1, arg2):
#  #receive specified file from server
#
#  if arg2 == "":
#    arg2 = arg1
#
#  try:
#    f = open(arg2, "wb")
#    connection.send("get " + str(arg1))
#    sstat = connection.recv(1)
#
#    if sstat == "Y":
#      #all is good, begin recieving file
#      print("[I] Get request accepted by server")
#
#    elif sstat == "E":
#      print("[E] Requested filename does not exist on server in current working directory")
#
#    else:
#      print("[E] Get request rejected by server.")
#
#    f.close()
#
#
#  except:
#    print("[E] Cannot open local file: " + arg2)
#
#  print("function not yet implemented")

def get(connection, arg1, arg2):
  #receive specified file from server
  if arg2 == "":
    arg2 = arg1

  try:
    f = open(arg2, "wb")
    print("[I] File at " + arg2 +" opened.")

  except:
    print("[E] Unable to open file " + arg2)
    return 0

  connection.send("get " + arg1)

  sstat = connection.recv(1)

  if sstat == "Y":
    length = str(connection.recv(1024)).strip()
    data_length = 0

    try:
      data_length = int(float(length))
      print("[I] Incoming file of length: " + str(data_length) +" kb")
      connection.send("Y")

    except:
      print("[E] Invalid file length recieved: " + str(length))
      connection.send("N")
      return 0

    for i in range(int(data_length)):
      data_segment = connection.recv(1024)
      print("[I] Recieved segment: " + str(i))
      print("[I]" + str(data_segment))

      f.write(data_segment)
      print("[I] Writing segment" + str(i) +" to file")

    f.close()
    return 0

  else:
    print("[E] Get request rejected by server.")
    f.close()
    return 0

def put(connection, arg1, arg2):
  #send specified file to server

  if arg2 == "":
    arg2 = arg1

  try:
    f = open(arg1, "rb")

  except:
    print("[E] Cannot open local file: " + arg1)
    return 0

  connection.send("put " + str(arg2))

  sstat = connection.recv(1)

  if sstat == "Y":
    #all is good, begin sending file
    print("[I] Put request accepted by server.")
    length = 0

    try:
      length = math.ceil(float(os.path.getsize(arg1))/1024)
      print("[I] File of length: " + str(length) + " kb")
      connection.send(str(length))
    except:
      e = sys.exc_info()[0]
      print(str(e))
   
    sstat = connection.recv(1)

    if(sstat == 'Y'):
      print("[I] File length accepted by server.")
    else:
      print("[E] File length rejected by server.")
      return 0
      
    data_segment = f.read(1024)
    while data_segment:
       connection.send(data_segment)
       data_segment = f.read(1024)

  elif sstat == "E":
    print("[E] Requested filename does not exist on server in current working directory")

  else:
    print("[E] Put request rejected by server.")

  f.close()

def main() :

  
  connection = establish_connection()
  authenticate(connection)

  stat = 0
  while(stat == 0):
    stat = get_function(connection)

      








main()
