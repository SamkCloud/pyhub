#!/usr/bin/python
# gd 20090320

import optparse
import shutil
import os

open_ldap_profile = "open_ldap"
open_ldap_profile_destination = "/etc/auth-client-config/profile.d/open_ldap"
ldap_conf_file = "/etc/ldap.conf"

def install_ladp_client(uri,base):
	from pyfig import Pyfig

	
	
	pyfig = Pyfig(ldap_conf_file,' ')
	
	#pyfig.change('rootbinddn','cn=admin,dc=zuccabar,dc=local')
	#pyfig.change('uri','ldap://10.134.27.153')
	#pyfig.change('base','dc=zuccabar,dc=local')
	
	pyfig.change('uri',uri)
	pyfig.change('base',base)
	
	# print pyfig.config
	
	#faccio il backup del file 
	shutil.copyfile(ldap_conf_file,ldap_conf_file+".orig")
	
	pyfig.commit(ldap_conf_file,' ')
	
	#copio  il file di configurazione per auth-client-config
	shutil.copyfile(open_ldap_profile,open_ldap_profile_destination)
	
	os.system ("auth-client-config -a -p open_ldap")



def main():
	p = optparse.OptionParser()
	p.add_option('--base', '-b', default="", help="the BaseDn of the LDAP server es: dc=zuccabar,dc=local")
	p.add_option('--ldapserver', '-l', default="",help="The hostname / IP addess of the ldap server")

	
	options, arguments = p.parse_args()
	
	if options.base == "":
		base = raw_input("Insert the base dn: ")
	else:
		base = options.base
	if options.ldapserver == "":
		ldapserver = raw_input("Insert hostname (or IP) of the Ldap server: ")
	else:
		ldapserver = options.ldapserver
	
	uri = "ldap://"+ldapserver
	
	
	install_ladp_client(uri,base)
	
	#print 'Hello %s' % options.person

if __name__ == '__main__':
	main()
