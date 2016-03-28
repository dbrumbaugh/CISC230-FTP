import socket

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
    

def main():
  host_socket = socket.socket()
  host_socket.bind((socket.gethostname(), 21))

  while True:
    host_socket.listen(1)

    session, ip_address = host_socket.accept()
    print("[I] Connection recieved from " + str(ip_address))

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










main()
