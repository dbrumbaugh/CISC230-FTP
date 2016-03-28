import socket

#Python client file for CISC230 Project

def establish_connection() :
  connection = socket.socket()

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
  inp = raw_input("Please enter a function to perform [? for help]: ")

  args = inp.split(" ", 1)
  func = args[0]

  if(func == "dir"):
    dirl(connection)
    return 0

  elif(func == "cd"):
    cd(connection, args[1])
    return 0

  elif(func == "get", args[1]):
    get(connection, args[1])
    return 0

  elif(func == "put", args[1]):
    put(connection, args[1])
    return 0

  elif (func == "?"):
    print_help()
    return 0

  elif (func == "exit"):
    return -1

  else:
    print("Invalid function or function syntax")
    print_help()

def print_help():
  #print help dialogue
  print("function not yet implemented")

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
  connection.send("cd " + str(arg))
  stat = str(connection.recv(1))

  if (stat == "Y"):
    print("[I] CD Command executed successfully")
  elif (stat == "A"):
    print("[A] Access violation on CD command. Access to requested directory is restricted.")
  else:
    print("[E] Exceptional condition in CD command. Ensure that desired directory exists and is properly spelled")

def get():
  #recieve specified file from server
  print("function not yet implemented")

def put():
  #send specified file to server
  print("function not yet implemented")


def main() :

  connection = establish_connection()
  authenticate(connection)

  cont = 0
  while(cont == 0):
    cont = get_function(connection)









main()
