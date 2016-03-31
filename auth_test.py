import hashlib

def authenticate(username, password):
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
        return True
        
  return False





