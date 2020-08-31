#################################################################################################
#############################################Starting Services in LIP/SAPP#######################
#################################################################################################

- hosts: '{{primary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Starting SAPP Services in Primary node"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Starting SAPP Admin server service"
         shell: "sh start_AdminServer_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/SAPP{{str_no.stdout}}
         become_user: oracle
       - pause:
            seconds: 30
       - name: "Starting SAPP Managed service"
         shell: "sh start_sapp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m01.ikea.com_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/SAPP{{str_no.stdout}}
         become_user: oracle
		 
- hosts: '{{secondary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Starting SAPP Services in Secondary node"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Starting SAPP Managed service"
         shell: "sh start_sapp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m02.ikea.com_WithNodeManager.sh"
         args:
            chdir: "/opt/oracle/domains11.1.1.9/SAPP{{str_no.stdout}}"
         become_user: oracle
       - pause:
            seconds: 30
       tags:
          - sapp_start
		  
- hosts: '{{primary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Starting LIP Services in primary Server"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Starting Admin service in {{inventory_hostname}}"
         shell: "sh start_AdminServer_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/LIP{{str_no.stdout}}
         become_user: oracle
       - pause:
            seconds: 30
       - name: "Starting LIPP service Primary Server"
         shell: "sh start_lipp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m01.ikea.com_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/LIP{{str_no.stdout}}
			
- hosts: '{{secondary}}'
  become: true
  become_method: sudo
  tasks:
     - name: "Starting LIP Services in secondary node"
       block:
       - name: "Pre-requisite: Task to stop Service - Validating Store Number"
         shell: "hostname | cut  -c 6-8"
         register: str_no
       - name: "Pre-requisite: Task to stop Service - Validating BU Code"
         shell: "hostname | cut  -c 4-5"
         register: str_code
       - name: "Starting LIP service in Secondary Server"
         shell: "sh start_lipp-{{str_code.stdout}}-sto-00{{str_no.stdout}}-m02.ikea.com_WithNodeManager.sh"
         args:
            chdir: /opt/oracle/domains11.1.1.9/LIP{{str_no.stdout}}
       tags:
          - lip_start