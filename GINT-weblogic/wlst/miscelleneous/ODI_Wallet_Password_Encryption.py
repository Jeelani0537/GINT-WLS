# -*- coding: utf-8 -*-

#Created on Fri August 14th 12:38:55 2020

#@author: NEPAN2

from __future__ import with_statement
import re
import sys
import getopt
import os
import os.path
import subprocess
from subprocess import Popen, PIPE, STDOUT

"""
Function to create the keys based on the store number and password (if password is common/variable)
"""
def list():
    com="ls -lrth"
    command=subprocess.call(com, shell=True)
    return command

def prepareStoreList(Multi_entry):
    storeList ={}
    for item in Multi_entry.split(':'):
        key = item.split(',')[0]
        storeList[key] = item
    print "Keys to be Encrypted: ", storeList.keys()
    return storeList


def execution_key(random_key,Keyname,random_key_encryption,password,Keys,Directory,Public_Key_Encryption,key_removal):

#Creating Random Keys

    myargs = []
    myargs.append(random_key)
    print "="*130
    print 'Step 1.'+'\t'+'Generating Random Key with name: ' + Keyname
    print "="*130
    p = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    Output=p.stdout.read()
    print("Genrated Random Key. PFB: ")
    list()
    print("Step 1. Completed")


#Encrypting Password using Random Key


    myargs = []
    myargs.append(random_key_encryption)
    print "="*130
    print 'Step 2.'+'\t'+'Encrypting Password using Random Key :  ' +  Keyname
    print "="*130
    q = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    Encrypted_Password = q.stdout.read()
    myargs = []
    myargs.append("date")
    q = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    date = q.stdout.read()
    Encrypted=open(Keys+"Encrypted.txt", 'a+')
    Encrypted.write(str(date)+"Encrypted Password For: ##"+Keyname+"## stored at --- "+Directory+":"+"\n"+Keyname+" : ")
    Encrypted.write(str(Encrypted_Password))
    Encrypted.write("\n")
    Encrypted.write("*"*120)
    Encrypted.write("\n")
    Encrypted.close()
    print("Encrypted password stored into the file:"+Keys+"Encryptex.txt")
    list()
    print("Step 2. Completed")

#Encrypting random_key_encryption using Public Key


    myargs = []
    myargs.append(Public_Key_Encryption)
    print "="*130
    print 'Step 3.'+'\t'+"Encrypting the: "+Keyname+" using Public Key for ODI"
    print "="*130
    r = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    f=Directory+"/"+Keyname+".enc"
    while not os.path.isfile(f):
         r = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
         if os.path.isfile(f):
             list()
             print("Step 3. Completed")
# Removing the unencrypted keys
             myargs = []
             myargs.append(key_removal)
             print "="*130
             print 'Step 4.'+'\t'+'Removing un-encrypted Key i.e. : ----- ' +  Keyname+' -----'
             print "="*130
             s = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
             list()
             print("Step 4. Completed")
             break
    print('\n')


#Encryption of the keys by calling the execution function

def KeyEncrypt(Directory,storeList,Keys):
    os.chdir(Directory)
    print("we are currently in : ---- "+os.getcwd()+"----")
    print('\n')
    for store in storeList:
        fields = storeList[store].split(",")
        Store = fields[0]
        print("Proceeding with the Key : "+Store)
        Password = fields[1]
        Keyname=str(Store)+".bin"
        Name=str(Directory)+"/"+str(Keyname)+".enc"
        exists = os.path.isfile(Name)
        if exists: # If Encrypted keys with Keyname existing then listing them.
            os.chdir(Directory)
            print '-'*130
            print('Encrypted entry already there for  '+str(Keyname)+' | in --- '+Directory+' --- Please find below:')
            print '-'*130
            list()
            print('\n')
        else:   # If Encrypted keys with Keyname not existing then creating them and starting Encryption process.
            os.chdir(Directory)
            print("The Present Directory is: ", os.getcwd())
            print('\n')
            print("*"*130)
            print("\t"*2+'----------------'+"\t"+'Starting the Password Encryption Process'+"\t"+'----------------'+"\t")
            print("*"*130)
            Enc_Keyname=str(Keyname)+".enc"
            random_key="openssl rand -base64 32 > "+str(Keyname)
            random_key_encryption="echo "+str(Password)+" | openssl enc -aes256 -md sha512 -pass file:"+str(Keyname)+" -e -base64"
            Public_Key_Encryption="openssl rsautl -encrypt -inkey "+str(Keys)+"/public.pem -pubin -in "+str(Keyname)+" -out "+str(Enc_Keyname)
            key_removal="rm "+str(Keyname)
            print "~"*130
            print "~"*53+" STARTING for : "+Store
            print "~"*130
            execution_key(random_key,Keyname,random_key_encryption,Password,Keys,Directory,Public_Key_Encryption,key_removal)
    print("*"*100)
    print("-"*41+" END of Encryption"+"-"*41)
    print("*"*100)

#Main function to create the directories and take the values as input. Creating Public and private key. Then calling the function to create encryption

def main(argv):
    store_detail = ""
    password = ""
    Keys = ""
    Directory = ""
    pwd = ""
    priv_key = ""
    pub_key = ""
    list_keys = ""
    Keyname = ""
    system = ""
    key_folder = ""
    Entries = ""
    Multi_entry = ""
    opts, args = getopt.getopt(argv,"k:f:m:",["kfile=","ffile=","mfile="])
    for opt, arg in opts:
        if opt in ("-k", "--kfile"):# To be used for Keyname for single entry
            Keyname = str(arg)
        elif opt in ("-f", "--ffile"):# To be used for Folder for the keys to be created/stored
            key_folder = arg
        elif opt in ("-m", "--mfile"):# To input Multi value separated by (:). Eg. key1,password123:key2,passwd12
            Multi_entry = str(arg)
    print "||"*40
    print "="*32 + "Activity STARTED" + "="*32
    print "||"*40
    print('\n')
    print('Pre-requisite Steps:')
    print('\n')
    Keys='/oitp_odi/ODI_KEYS/'
    Directory="/oitp_odi/"+str(key_folder)
    print("The Name of Requested Key Directory is: "+Directory)
    if os.path.exists(Keys): #Checking if the Folder containing Public/Private keys existing or not.
        os.chdir(Keys)
        print(Keys+" Directory already existing, checking for the keys in the: "+os.getcwd())
        if not (os.path.exists('./public.pem') and os.path.exists('./private.pem')): # Checking if Public Private Keys are existing in ODI_KEYS folder or not
            print("Keys not there, generating the same in : "+os.getcwd())
            print("Creating Public/Private keys")
            priv_key='openssl genrsa -out private.pem 1024'
            pub_key='openssl rsa -in private.pem -out public.pem -outform PEM -pubout'
            subprocess.call(priv_key, shell=True)
            subprocess.call(pub_key, shell=True)
            print('-'*70)
            list()
            print('-'*70)
        #if Public Private Keys Existing we listing the same.
        else:
            print("Public/Private Keys already created please find below:")
            print('-'*70)
            list()
            print('-'*70)
		#Creating the Public Private keys if not there.	
    else:
        print("Creating the"+Keys+" folder")
        os.makedirs(Keys)
        os.chdir(Keys)
        print("Creating Public/Private keys in: ---- "+os.getcwd()+" ----")
        priv_key='openssl genrsa -out private.pem 1024'
        pub_key='openssl rsa -in private.pem -out public.pem -outform PEM -pubout'
        subprocess.call(priv_key, shell=True)
        subprocess.call(pub_key, shell=True)
        print('-'*70)
        list()
        print('-'*70)

        #To check if the Directory is already present or not, if not then will create the Directory first and then Encryption will happen.
    print('\n')
    storeList = prepareStoreList(Multi_entry)
    if not os.path.exists(Directory):
        print('Creating the: '+Directory)
        os.makedirs(Directory)
        os.chdir(Directory)
        print("Directory Created: ", os.getcwd())
        KeyEncrypt(Directory,storeList,Keys)
        print "*"*39+"Completed Successfully"+"*"*39
        print "*"*101

        #To check if the entries are already there in the existing Directories
    else:
        os.chdir(Directory)
        print('The ######### '+Directory+' ######### already there')
        KeyEncrypt(Directory,storeList,Keys)
        print "*"*39+"Completed Successfully"+"*"*39
        print "*"*100



if __name__ == "__main__":
  try:
    main(sys.argv[1:])
    print "Execution completed successfully!!!"
  except OSError as e:
    sys.exit("Execution failed",e)

