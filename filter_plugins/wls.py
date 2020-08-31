#!/usr/bin/python
import re
import ldap


class FilterModule(object):
    def filters(self):
        return {
            'shutdown_wls_command': self.shutdown_wls_cmd,           
            'get_domains': self.get_domains,
            'get_datasource_files': self.get_datasource_files,
            'get_db_conn': self.get_db_conn,
            'append_tuple_to_dict': self.append_tuple_to_dict
            #'lookup_connect_string': self.lookup_connect_string
        }           


    def lookupJDBCUrlFromLDAP(self, jdbcLdapUrl, ldapUsername = None, ldapPassword = None):
        # for future usa: ldapUsername = None, ldapPassword = None
        ldap_urls = jdbcLdapUrl.split(" ")

        if len(ldap_urls) == 0:
            return ""

        for url in ldap_urls:
            t = url.split(",",1)
            domain = t[0]
            domains = domain.rsplit('/', 1)
            basedn = t[1]
            # basedn ="cn=OracleContext,dc=ikeadt,dc=com"
            server =  domains[0]
            database = domains[1]

            conn = ldap.initialize(server)           #"ldap://ppoid1.ikeadt.com:389")
            searchFilter =  "(&(objectClass=*)(cn=%s))" % database
            result = conn.search_s(basedn, ldap.SCOPE_SUBTREE, searchFilter)
            if len(result) > 0:
                return result[0][1]["orclNetDescString"][0]

        return ""

    def lookup_connect_string(self, url, ldapUsername = None, ldapPassword = None):
        if url.lower().startswith( 'ldap' ):
            return  self.lookupJDBCUrlFromLDAP(url,ldapUsername = None, ldapPassword = None)
        else:
            return "//" + url    


    def append_tuple_to_dict(self, mytuple, mydict):
        #print(mytuple[0])
        if "IAU_APPEND" in mytuple[0]:
            s = mytuple[0].replace("_APPEND","")
            url = mytuple[1].replace("jdbc:oracle:thin:@","")
            url = self.lookup_connect_string(url)
            mydict["IAU"] = {"schema": s, "url": url}
        elif "MASTER" in mytuple[0]:
            url = mytuple[1].replace("jdbc:oracle:thin:@","")
            url = self.lookup_connect_string(url)
            mydict["ODI"] = {"schema": mytuple[0], "url": url}
        elif "OPSS" in mytuple[0]:
            url = mytuple[1].replace("jdbc:oracle:thin:@","")
            url = self.lookup_connect_string(url)
            mydict["OPSS"] = {"schema": mytuple[0], "url": url}
        elif "STB" in mytuple[0]:
            url = mytuple[1].replace("jdbc:oracle:thin:@","")
            url = self.lookup_connect_string(url)
            mydict["STB"] = {"schema": mytuple[0], "url": url}
        elif "WLS_RUNTIME" in mytuple[0]:
            url = mytuple[1].replace("jdbc:oracle:thin:@","")
            url = self.lookup_connect_string(url)
            s = mytuple[0].replace("_RUNTIME","")
            mydict["WLS"] = {"schema": s, "url": url}
        #print(mydict)
        return mydict

# Internally used
# Reads a WLS jdbc config file and returs schema name and jdbc url
    def get_db_conn(self, input):
        m = re.search(r"(.*)(<url>)(.*)(</url>)(.*)",input)
        m1 = re.search(r"(.*)(<value>)(.*)(</value>)(.*)",input)
        return m1.group(3), m.group(3)


# Generates a server shutdown command
# Input; Tuple Content from "config.xml" + domain home
# Output:  dictionary schemaname: jdbc url

    def get_datasource_files(self, input, domainHome):

#ORACLE_HOME="/mnt/c/kari/base_domain"
#f_config=ORACLE_HOME + "/config/config.xml"
        result = list()
        m = re.findall(r"(.*)(<descriptor-file-name>)(.*)(</descriptor-file-name>)(.*)",input)
        for e in m:
            if (e[2].startswith("jdbc")):
                result.append(domainHome + "/config/" + e[2])
                #print(e[2])
            #    schema, url = self.getUrl(domainHome + "/config/" + e[2])
            #    dbs[schema] = url
    # <url>jdbc:oracle:thin:@//localhost:1521/ODI.IKEA.COM</url>    
        return result

# Generates a server shutdown command
# Input; Output from "ps ax | grep weblogic.Server | grep  -v grep || true" 
# Output: List of shell scrips with FQP
    def shutdown_wls_cmd(self, input):
        result = list()
        for row in input.split("\n"):
            m = re.search(r"(.*)(-Dweblogic.Name=)([^\s]+)(.*)(-Ddomain.home=)([^\s]+)(.*)",row)
            command = "%s/stop_%s_WithNodeManager.sh" % (m.group(6),m.group(3))
            result.append(command)
        return result

# Generates a collection of all registered domains fro a Oracle home
# Input; Content of file domain-registry.xml
# Output: List of domain homes
    def get_domains(self, input):
        m = re.findall(r"(.*)(<domain location=\")(.*)(\"\/>)(.*)",input)
        return [e[2] for e in m]



