- hosts: all
  gather_facts: no

  roles:
  - role: lip-sapp-restart
    activity: stop
    tags: weblogicstop

  - role: lip-sapp-restart
    activity: start
    tags: weblogicstart
