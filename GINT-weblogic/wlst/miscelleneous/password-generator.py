import random
import string
import re

def generateRandomPassword(length):
  password = ''
  #print "Generating random password"

  for i in range(length):
    password = password + str(random.choice(string.ascii_letters + string.digits))

  return password

def validatePassword(password):
  #print "Validating if password is alpha-numeric"
  #return password.isalnum()
  return bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', password))

flag = False

while True :
  password = generateRandomPassword(15)
  flag = validatePassword(password)
  #print flag
  if flag:
    break

print password

