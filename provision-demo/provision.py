#!/usr/bin/env python3

import sys
sys.path.insert(0, "/var/www/MISP/PyMISP/examples/")
from pymisp import ExpandedPyMISP, MISPUser, MISPOrganisation
from keys import misp_url, misp_key, misp_verifycert, misp_client_cert

max_users = 10

default_password = "{user}"
default_siteadmin = "admin-{user}@DEMO"
default_user = "user-{user}@DEMO"
org_name = "training - DEMO"

api = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)

def provision():
    # Add demo organisation
    org = MISPOrganisation()
    org.name = org_name 
    org.nationality = "Belgium"
    org.sector = "IT"
    org.type = "Training organisation"
    org.local = 1

    #add_org = api.add_organisation(org, pythonify=True)
    #orgid = add_org.id
    orgid = 11

    # Add demo users
    current_user = 1
    while current_user <= max_users:
        user = MISPUser()
        user.email = default_siteadmin.format(user=current_user)
        user.password = default_password.format(user=current_user)
        user.enable_password = 1
        user.change_pw = 0
        user.org_id = orgid
        user.role_id = 1  # Site admin
        add_user = api.add_user(user, pythonify=True)
        print("Add user %s" % user.email)

        user = MISPUser()
        user.email = default_user.format(user=current_user)
        user.password = default_password.format(user=current_user)
        user.enable_password = 1
        user.change_pw = 0
        user.org_id = orgid
        user.role_id = 3  # User
        add_user = api.add_user(user, pythonify=True)    
        print("Add user %s" % user.email)

        current_user += 1

def unprovision():
    users = api.users()
    current_user = 1
    while current_user <= max_users:
        for el in users:
            obj = el['User']
            if obj['email'] == default_siteadmin.format(user=current_user):
                user = MISPUser()
                user.id = obj['id']
                api.delete_user(user)
                print("delete %s" % obj['email'])
            elif obj['email'] == default_user.format(user=current_user):
                user = MISPUser()
                user.id = obj['id']
                api.delete_user(user)
                print("delete %s" % obj['email'])
        current_user +=1 


#provision()
#unprovision()
