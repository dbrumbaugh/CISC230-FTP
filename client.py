import socket

#Python client file for CISC230 Project

def establish_connection() :
  connection = socket.socket()

  while True:
    try:
      ip_address = raw_input("Please enter the IP address of the FTP server to which to connect: ")
      port = raw_input("Please enter the port number on which to connect: ")

      #connection.connect((ip_address, port))
      #test code
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

def main() :

  #Attempt to establish a connection to the server

  connection = establish_connection()
   
  authenticate(connection)

  getfunction(connection)









main()
