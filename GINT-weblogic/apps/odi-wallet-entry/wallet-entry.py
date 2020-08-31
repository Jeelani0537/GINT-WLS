# -*- coding: utf-8 -*-
from __future__ import with_statement
import re
import sys
import getopt
import ConfigParser as configparser
from subprocess import Popen, PIPE, STDOUT

#props_path='/oitp_odi/wallet/Automation_wallet/wallet_prop.properties'

def tns(tnsnamespath,tns_name):
    print("="*79+ '\n'+"THE NEW TNS ENTRIES ARE AS BELOW: " +'\n'+"="*79 + '\n')
    tns_entry = tns_name.split(':')
    for tns in tns_entry:
        alias = tns.split("=")[0]
        counter=1
        fo = open(tnsnamespath, 'ra+')
        existing_entry = fo.read()
        existing_alias = existing_entry.split("\n")
        list_length=len(existing_alias)
        for existing_entries in existing_alias:
            existing_alias_name = existing_entries.split("=")[0]
            counter+=1
            if alias == existing_alias_name:
                print "TNS Already existing with alias name = " + existing_alias_name
                break
            elif alias != existing_alias_name and list_length == counter:
                #print "The New alias name = " + alias
                fo.write(str(tns))
                fo.write('\n')
                print "The New TNS Added to the tnsnames.ora is : " + tns
    fo.close()
    print "||"*40
    print "="*20 + "ACTIVITY COMPLETED" + "="*40
    print "||"*40

def prepareStoreList(entries):
    storeList = {}
    for item in entries.split(':'):
        storeName = item.split(',')[0]
        storeList[storeName] = item

    print "Entries to be added: ", storeList.keys()
    return storeList

# This method is no longer used. prepareStoreList method replaced this functionality
def store(store_list_p,entries):
    store_list = entries.split(':')
    hs = open(store_list_p, 'w')
    for store_str in store_list:
        hs.write(str(store_str))
        hs.write('\n')
        print(store_str)
    hs.close()

def getEnvDetailsParam():
    #print "THE ENVIRONMENT NAME IS:  ",envName
    conf = configparser.ConfigParser()
    props_path = "/opt/oracle/scripts/.wallet.properties"
    conf.read(props_path)
    envLogParam = {}
    envLogParam["wallet_password"] = conf.get('EnvDetails','wallet_password')
    envLogParam["wallet_path"]=conf.get('EnvDetails','wallet_path')
    #envLogParam["store_list_p"]=conf.get('EnvDetails','store_list_p')
    return envLogParam

def walletEntry(inputaction,entries,tns_name,mkstore,domain):
    properties_details = getEnvDetailsParam()
    mkstore_path = mkstore
    wallet_dir = properties_details['wallet_path']
    #store_list_p = properties_details['store_list_p']
    wallet_pwd = properties_details['wallet_password']
    #tnsnamespath = "/oitp_odi/" + domain + "/network/admin/tnsnames.ora"
    tnsnamespath = "/oitp_odi/network/admin/tnsnames.ora"

    storeList = prepareStoreList(entries)
    #store(store_list_p,entries)
    print 'Mkstore: ', mkstore_path
    print 'Domain name is: ', domain
    print "Wallet: ", wallet_dir
    print 'Chosen Action: ', inputaction
    print "="*79
    print "EXISTING WALLET ENTRIES:"
    print "="*79
    myargs = []
    myargs.append(mkstore_path)
    myargs.append("-wrl")
    myargs.append(wallet_dir)
    myargs.append("-listCredential")

    p = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input=wallet_pwd)[0]
    print grep_stdout.decode()
    print "||"*40
    print "="*70
    print "ADDING NEW WALLET ENTRIES:"
    print "="*79
    print "||"*40
    if inputaction == 'create':
        Action = "-createCredential"
    elif inputaction == 'modify':
        Action = "-modifyCredential"
    print 'Action :',inputaction
    #file = open(store_list_p,"r")
    #for line in file:
    for store in storeList:
        fields = storeList[store].split(",")
        Alias = fields[0]
        User = fields[1]
        Pwd = fields[2]
        myargs = []
        myargs.append(mkstore_path)
        myargs.append("-wrl")
        myargs.append(wallet_dir)
        myargs.append(Action)
        myargs.append(Alias)
        myargs.append(User)
        myargs.append(Pwd)
        print "="*79
        print 'Trying to add ' +  Alias + ' having user: ' + User
        print "="*79

        p = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        grep_stdout = p.communicate(input=wallet_pwd)[0]
        print grep_stdout.decode()
    print "||"*40
    print "="*79
    print "UPDATED WALLET ENTRIES:"
    print "="*79
    print "||"*40
    myargs = []
    myargs.append(mkstore_path)
    myargs.append("-wrl")
    myargs.append(wallet_dir)
    myargs.append("-listCredential")

    p = Popen(myargs,stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input=wallet_pwd)[0]
    print grep_stdout.decode()
    print "||"*40
    print "="*20 + "WALLET ENTRIES COMPLETED" + "="*20
    print "||"*40
    print ""
    tns(tnsnamespath,tns_name)


def main(argv):
    mkstore = ""
    store_file = ""
    username = ""
    password = ""
    wallet_dir = ""
    wallet_pwd = ""
    Action = ""
    inputaction = ""
    envName = ""
    entries = ""
    domain = ""
    tns_name = ""
    opts, args = getopt.getopt(argv,"a:e:s:x:m:d:",["afile=","efile=","sfile=","xfile=", "mfile=", "dfile="])
    for opt, arg in opts:
        if opt in ("-a", "--afile"):
            inputaction = str(arg)
        elif opt in ("-e", "--efile"):
            envName = arg
        elif opt in ("-s", "--sfile"):
          tns_name = str(arg)
        elif opt in ("-x", "--xfile"):
          entries = str(arg)
        elif opt in ("-m", "--mfile"):
          mkstore = str(arg)
        elif opt in ("-d", "--dfile"):
          domain = str(arg)
    print "||"*40
    print "="*20 + "ACTIVITY STARTED" + "="*40
    print "||"*40
    walletEntry(inputaction,entries,tns_name,mkstore,domain)

if __name__ == "__main__":
  try: 
    main(sys.argv[1:])
    print "Execution completed successfully!!!"
  except Exception as e:
    print e
    sys.exit("Execution failed")
