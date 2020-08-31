#################################################################################################
#############################################Stopping Services in LIP/SAPP#######################
#################################################################################################

- hosts: '{{secondary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Stopping the SAPP Services in Secondary Server"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Stopping SAPP service"
         shell: "sh stop_sapp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m02.ikea.com_WithNodeManager.sh"
         args:
            chdir: "/opt/oracle/domains11.1.1.9/SAPP{{str_no.stdout}}"
         become_user: oracle
       - pause:
            seconds: 30
			
- hosts: '{{primary}}'
  become: true
  become_method: sudo
  become_user: oracle
  tasks:
     - name: "Stopping the SAPP Services in Primary Server"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Stopping SAPP service"
         shell: "sh stop_sapp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m01.ikea.com_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/SAPP{{str_no.stdout}}
         become_user: oracle
       - pause:
            seconds: 30
       - name: "Stopping SAPP Admin server service in {{GINT-LIP-SAPP}}"
         shell: "sh stop_AdminServer_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/SAPP{{str_no.stdout}}
       - pause:
            seconds: 30
       tags:
          - sapp_stop
         		 
- hosts: '{{secondary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Stopping the LIP Services in Secondary Server"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Stopping LIP service"
         shell: "sh stop_lipp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m02.ikea.com_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/LIP{{str_no.stdout}}
         become_user: oracle
       - pause:
            seconds: 30
			
- hosts: '{{primary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Stopping the LIP Services in Primary Server"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Stopping LIP service"
         shell: "sh stop_lipp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m01.ikea.com_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/LIP{{str_no.stdout}}
         become_user: oracle
       - pause:
            seconds: 30
       - name: "Stopping Admin service"
         shell: "sh stop_AdminServer_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/LIP{{str_no.stdout}}
         become_user: oracle
       - pause:
            seconds: 30
       tags:
          - lip_stop