#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:21:42 2019
@author: asbhu1
"""
import cx_Oracle as co
import sys,getopt
import ConfigParser as configparser

#props_path = "/home/kakum7/scripts/.MHS_ACT_PM_PARAM.properties"
props_path = "/home/s-oitpans-u-itseelm/scripts/.MHS_ACT_PM_PARAM.properties"

def getPmParameter(env):
    conf = configparser.ConfigParser()
    conf.read(props_path)
    pmParameter = {}
    pmUserPwd = {}
    pmParameter["host_name"] = conf.get(env, 'hostName')
    pmParameter["port"] = conf.get(env, 'portNumber')
    pmParameter["service_name"] = conf.get(env, 'serviceName')
    pmUserPwd["MHS_FCST_OUSER"]=conf.get(env, 'MHS_FCST_OUSER_PASSWORD')
    pmUserPwd["MHS_LT_OUSER"]=conf.get(env, 'MHS_LT_OUSER_PASSWORD')
    pmUserPwd["MHS_MR_OUSER"]=conf.get(env, 'MHS_MR_OUSER_PASSWORD')
    pmUserPwd["MHS_RU_OUSER"]=conf.get(env, 'MHS_RU_OUSER_PASSWORD')
    pmUserPwd["MHS_STOCK_OUSER"]=conf.get(env, 'MHS_STOCK_OUSER_PASSWORD')
    pmUserPwd["MHS_TAX_OUSER"]=conf.get(env, 'MHS_TAX_OUSER_PASSWORD')
    pmUserPwd["SASR_OUSER"]=conf.get(env, 'MHS_SASR_OUSER_PASSWORD')
    pmUserPwd["SIS_OUSER"]=conf.get(env, 'MHS_SIS_OUSER_PASSWORD')
    pmParameter["sys_id_SASR_PFIX"] =conf.get(env, 'sys_id_SASR_PFIX')
    pmParameter["sys_id_SIS_PFIX"] = conf.get(env, 'sys_id_SIS_PFIX')
    return pmParameter,pmUserPwd
def getStoreEntitySysID(cursor,schema_name,stre_name):
    SQL_store_id = "select STORE_ID from "+schema_name+".MHS_STORE where STORE_NAME="+stre_name
    cursor.execute(SQL_store_id) 
    store_id = ''
    for row in cursor:
        store_id = row[0]
    return store_id

def closePmCon(conn,cursor):
    conn.commit() 
    cursor.close()
    conn.close()
def performActivity(conParam,upParam,stre_name):
    try:
        host_name = conParam["host_name"]
        port = conParam["port"]
        service_name = conParam["service_name"]
        dsn_tns = co.makedsn(host_name, port, service_name=service_name) 
        strTable = "<table border=2><tr style='background-color:gray;'><th>SCHEMA_NAME</th><th>STR/SYS-ID</th><th>ENTITY-ID</th><th>VALID FROM</th><th>VALID TO</th><th>ERROR-MSG</th></tr>"
        for i in upParam:
            try:
                schema_name = str(i)
                pwd = upParam[i]
                conn = co.connect(user= schema_name ,password= pwd, dsn=dsn_tns)
                cursor = conn.cursor()
                if(schema_name!="SASR_OUSER" and schema_name != "SIS_OUSER"):
                    store_id_fetched = getStoreEntitySysID(cursor,schema_name,stre_name)        #Call the getStoreEntitySysID to fetch the store_id and entity_id
                    if(store_id_fetched == '' ):raise co.Error('Store Number '+stre_name+' NOT EXIST')
                    Select_Query = "Select store_id, entity_id, valid_from, Valid_to from "+ schema_name +".MHS_ENTITY_STORE_XREF  where store_id ="+store_id_fetched
                else:
                    if(schema_name == "SASR_OUSER"):
                        store_id_fetched = conParam["sys_id_SASR_PFIX"]+stre_name
                    else: 
                        store_id_fetched = conParam["sys_id_SIS_PFIX"]+stre_name
                    Select_Query ="Select SYS_ID, entity_id, valid_from, Valid_to from "+ schema_name +".SYSTEM_ENTITY_XREF where sys_id ='"+store_id_fetched+"'"
                out_come = cursor.execute(Select_Query)
                sys_id_test =''
                for row in out_come:
                    sys_id_test = row[0]                    
                    strRW = "<tr style='text-align:center;'><td>"+schema_name+"</td><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td><td>"+row[2].strftime("%b %d %Y,%H:%M:%S")+"</td><td>"+row[3].strftime("%b %d %Y,%H:%M:%S")+"</td><td>NA</td></tr>"
                    strTable = strTable+strRW 
                if(sys_id_test ==''):raise co.Error('SYS ID '+store_id_fetched+' NOT EXIST')
                closePmCon(conn,cursor)
            except co.Error as e:
                print '{:<16s},{:>10s},{:>12s},{:>14s},{:>23s},{:>42s}'.format(schema_name, 'No Data' , "No Data", "No Data", "No Data",str(e))
                strRWError = "<tr style='text-align:center;'><td>"+schema_name+"</td><td>Not-Found</td><td>Not-Found</td><td>No-Data</td><td>No-Data</td><td>"+str(e)+"</td></tr>"
                strTable = strTable+strRWError  
                closePmCon(conn,cursor)
        strTable = strTable+"</table>"
        return strTable             
    except co.Error as e:
        print "Error ",schema_name," #######",e
              
def main(argv): 
    #opts, args = getopt.getopt(argv,"s:e:",["sfile=","efile="])
    opts, args = getopt.getopt(argv,"s:a:e:u:",["sfile=","afile=","efile=","user="])
    for opt, arg in opts:
       if opt in ("-s", "--sfile"):
          stre_name = str(arg)
       elif opt in ("-e", "--efile"):
          env_name = arg
    store_list = stre_name.split(',')
    myvar1, myvar2 = getPmParameter(env_name)
    strHTMLpage = "<html>" 
    for store in store_list:
        strTableHeader = "<h2>The Status of Store Number : "+store+"</h2>"
        tableStr = performActivity(myvar1,myvar2,store)
        strHTMLpage = strHTMLpage+strTableHeader+tableStr+"<br>"
    strHTMLpage = strHTMLpage + "</html>"
    hs = open("MhsStoreStatus.html", 'w')
    hs.write(strHTMLpage)
    hs.close()         
if __name__ == "__main__":
   main(sys.argv[1:])
