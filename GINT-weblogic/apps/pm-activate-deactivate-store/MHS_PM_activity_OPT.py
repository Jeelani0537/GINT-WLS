#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 08:48:05 2019
@author: asbhu1
"""
import cx_Oracle as co
import sys,getopt
import ConfigParser as configparser

#props_path = "/home/kakum7/scripts/.MHS_ACT_PM_PARAM.properties"
props_path = "/home/s-oitpans-u-itseelm/scripts/.MHS_ACT_PM_PARAM.properties"

def getPmParameter(env,activity):
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
    pmParameter["update_date"]=conf.get('pmDate', activity)
    return pmParameter,pmUserPwd

def getStoreEntitySysID(cursor,schema_name,stre_name):
    if(schema_name != 'SASR_OUSER' and schema_name != 'SIS_OUSER'):
        SQL_store_id = "select STORE_ID from "+schema_name+".MHS_STORE where STORE_NAME="+stre_name
        cursor.execute(SQL_store_id)
        store_id = convToStr(cursor)        #Fetching Store_ID
        if(store_id == ''):raise co.Error('Store Number '+stre_name+' NOT EXIST')
        SQL_entity_id = "select entity_id from "+schema_name+".MHS_ENTITY_STORE_XREF where STORE_ID ="+store_id
        cursor.execute(SQL_entity_id)
        entity_idf = convToStr(cursor)      #Fetching entity_ID
        return store_id,entity_idf
        if(entity_idf == ''):raise co.Error('Entity ID for '+stre_name+' NOT EXIST')
    else:
        SQL_entity_id = "Select distinct(ENTITY_ID) from "+schema_name+".SYSTEM_ENTITY_XREF"
        cursor.execute(SQL_entity_id)       #Fetching entity_ID
        entity_idf = convToStr(cursor)
        return entity_idf

def convToStr(ID):      #Pass the cursor object from getStoreEntitySysID
    entity_id = []
    i=0
    for row in ID:
        entity_id.append(row[i])
        ++i
    strID = ','.join(str(s) for s in entity_id)
    return strID        # return string store_id

def closePmCon(conn,cursor):
    conn.commit()
    cursor.close()
    conn.close()

def performActivity(env_name,userList,stre_name,activity):
    try:
        conParam, upParam = getPmParameter(env_name,activity)
        if('ALL' in userList):
            schemaList = upParam
        else:
            schemaList = list(userList.replace('[','').replace(']','').split(','))
        host_name = conParam["host_name"]
        port = conParam["port"]
        service_name = conParam["service_name"]
        act_date = conParam["update_date"]
        dsn_tns = co.makedsn(host_name, port, service_name=service_name)
        dash = '-' * 120
        print dash
        print '{:<12s},{:>11s},{:>12s},{:>15s},{:>19s},{:>9s},{:>19s}'.format("STR/SYS ID","ENTITY ID","Activity","SCHEMA", "ROWS UPDATED","STATUS","ERROR MSG")
        print dash
        strTable = "<table border=2><tr style='background-color:gray;'><th>STR/SYS-ID</th><th>ENTITY-ID</th><th>Activity</th><th>SCHEMA</th><th>ROWS-UPDATED</th><th>STATUS</th><th>ERROR-MSG</th></tr>"
        for i in schemaList:
            try:
                schema_name = str(i)
                pwd = upParam[i]
                conn = co.connect(user= schema_name ,password= pwd, dsn=dsn_tns)
                cursor = conn.cursor()
                if(schema_name!="SASR_OUSER" and schema_name != "SIS_OUSER"):
                    store_id_fetched, entity_id = getStoreEntitySysID(cursor,schema_name,stre_name)        #Call the getStoreEntitySysID to fetch the store_id and entity_id
                    UPDATE_Query = "UPDATE "+ schema_name +".MHS_ENTITY_STORE_XREF  SET VALID_TO = TO_TIMESTAMP("+act_date+", 'YYYY-MM-DD HH24:MI:SS.FF') where store_id ="+store_id_fetched+"and entity_id in ("+entity_id+")"
                else:
                    if(schema_name == "SASR_OUSER"):
                        store_id_fetched = conParam["sys_id_SASR_PFIX"]+stre_name
                    else:
                        store_id_fetched = conParam["sys_id_SIS_PFIX"]+stre_name
                    entity_id = getStoreEntitySysID(cursor,schema_name,stre_name)                 #Call the getStoreEntitySysID fun to fetch the entity_id
                    UPDATE_Query ="UPDATE "+ schema_name +".SYSTEM_ENTITY_XREF SET VALID_TO = TO_TIMESTAMP("+act_date+", 'YYYY-MM-DD HH24:MI:SS.FF') where SYS_ID ='"+store_id_fetched+"'and ENTITY_ID in ("+entity_id+")"
                cursor.execute(UPDATE_Query)
                out_come = cursor.rowcount
                if(out_come <= 0):raise co.Error('SYS id '+store_id_fetched+' does not exist')
                print '{:<12s},{:>9s},{:>15s},{:>18s},{:>10d},{:>14s},{:>18s}'.format(store_id_fetched, entity_id, activity, schema_name, out_come,'SUCCESS','NA')      
                strRW = "<tr style='text-align:center;'><td>"+store_id_fetched+"</td><td>"+entity_id+"</td><td>"+activity+"</td><td>"+schema_name+"</td><td>"+str(out_come)+"</td><td>SUCCESS</td><td>NA</td></tr>"
                strTable = strTable+strRW
                closePmCon(conn,cursor)
            except co.Error as e:
                print '{:<12s},{:>9s},{:>15s},{:>18s},{:>12s},{:>12s},{:>34s}'.format('Not Found', 'Not Found', activity, schema_name, 'No Data','ERROR',str(e))
                strRWError = "<tr style='text-align:center;'><td>Not-Found</td><td>Not-Found</td><td>"+activity+"</td><td>"+schema_name+"</td><td>No-Data</td><td>ERROR</td><td>"+str(e)+"</td></tr>"
                strTable = strTable+strRWError
                closePmCon(conn,cursor)
        strTable = strTable+"</table>"
        return strTable
    except co.Error as e:
        print "Error " + schema_name + " #######" + e

def main(argv):
    opts, args = getopt.getopt(argv,"s:a:e:u:",["sfile=","afile=","efile=","user="])
    for opt, arg in opts:
       if opt in ("-s", "--sfile"):
          stre_name = str(arg)
       elif opt in ("-a", "--afile"):
          activity = arg
       elif opt in ("-e", "--efile"):
          env_name = arg
       elif opt in ("-u", "--user"):
          userList = arg
    store_list = stre_name.split(',')
    strHTMLpage = "<html>"
    for store in store_list:
        print
        print "The PM activity Status of Store Number : ", store
        strTableHeader = "<h2>The PM activity Status of Store Number : "+store+"</h2>"
        tableStr = performActivity(env_name,userList,store,activity)
        strHTMLpage = strHTMLpage+strTableHeader+tableStr+"<br>"
    strHTMLpage = strHTMLpage + "</html>"
    hs = open("PMactivity.html", 'w')
    hs.write(strHTMLpage)
    hs.close()
if __name__ == "__main__":
   main(sys.argv[1:])
