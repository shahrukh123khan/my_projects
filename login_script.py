
import paramiko
import re
import os
import json
import time
import random
import logging
import traceback
import shutil
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import pytz





def create_tunnel(source_server_credentials=None, target_server_credentials=None, timeout=None, ssh_connection = None):
    print("ssh connection",ssh_connection)
    if ssh_connection and ssh_connection[0] == False:
        return False, ssh_connection[1]
    elif ssh_connection and ssh_connection[0] == True:
        ssh_connection = ssh_connection[1]
    
    vmtransport = ssh_connection.get_transport()
    dest_addr = (target_server_credentials['ip'], 22)
    local_addr = (source_server_credentials['ip'], 22)
    try:
        vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr, timeout=timeout)
        return True, vmchannel
    except Exception as e:
        print(f"Error in creating tunnel to {target_server_credentials['ip']} \n Error: {e}")
        return False, f"Connection timed out to Server {target_server_credentials['ip']}"


def ssh_server_connect(server_credentials=None, timeout=None, tunnel=None):
    if tunnel and tunnel[0] == False:
        print("######################################## ssh connection #########################")
        return tunnel
    elif tunnel and tunnel[0] == True:
        print("######################################## ssh connection 1#########################")
        tunnel = tunnel[1]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ssh credential  @@@@@@@@@@@@@@          ##############")
        print(server_credentials['username'])
        print(server_credentials['password'])
        print(server_credentials['ip'])
        ssh.connect(server_credentials['ip'], 
                    username=server_credentials['username'], 
                    password=server_credentials['password'], 
                    timeout=timeout, sock=tunnel       # added by me 20/08/24
                    ) 
   
        print("after ssh connection")
    except paramiko.AuthenticationException as authException:
        print(f"Authentication failed #1 when connecting to {server_credentials['ip']}\n Error: {authException}")
        return False, f"Credential Issue to Server {server_credentials['ip']}"
    except paramiko.SSHException as sshException:
        print(f"Authentication failed #2 when connecting to {server_credentials['ip']} \n Error: {sshException}")
        return False, f"Credential Issue to Server {server_credentials['ip']}"
    except socket.timeout:
        print(f"Connection timed out when connecting to {server_credentials['ip']}")
        return False, f"Connection timed out to Server {server_credentials['ip']}"
    except Exception as e:
        print(f"Authentication failed #3 when connecting to {server_credentials['ip']} \n Error: {e}")
        return False, f"Credential Issue to Server {server_credentials['ip']}"
    
    return True, ssh
    
# command='ls'
# jump_server = {
#     'ip': '10.40.55.186',
#     'username': 'chatbotadm',
#     'password': 'Chatbot!234'
# }
# jump_server_credentials = {
#     'ip': jump_server['ip'],
#     'username': jump_server['username'],
#     'password': jump_server['password']
# }



def run_commands(command,jump_server):
    
    target_username = 'snenrc'
    target_password = 'SNrc!&2@23'
    
    
    target_server_credentials = {
        'ip': '10.95.189.67',
        'username': target_username,
        'password': target_password
    }


   
    tunnel = create_tunnel(jump_server_credentials, target_server_credentials, timeout=600, ssh_connection=jump_server)
    if not tunnel[0]:
        return f"Tunnel creation failed: {tunnel[1]}"

    target_server = ssh_server_connect(target_server_credentials, timeout=600, tunnel=tunnel)
    if not target_server[0]:
        return f"SSH connection failed: {target_server[1]}"

    ssh_client = target_server[1]
    stdin, stdout, stderr = ssh_client.exec_command(command)
    result = stdout.read().decode()
    error = stderr.read().decode()
    ssh_client.close()
    
    if error:
        return f"Error: {error}"
    return result
        


command = 'show router interface'
jump_server = {
    'ip': '10.40.55.186',
    'username': 'chatbotadm',
    'password': 'Chatbot!234'
}
jump_server_credentials = {
    'ip': jump_server['ip'],
    'username': jump_server['username'],
    'password': jump_server['password']
}

# jump_server = ssh_server_connect(jump_server_credentials, timeout=600)

jump_server = ssh_server_connect(jump_server_credentials, timeout=600)
# retry_jump_server = 3
# while jump_server[0] == False and retry_jump_server > 0:
#     time.sleep(5)
#     jump_server = ssh_server_connect(jump_server_credentials, timeout=60)
#     retry_jump_server -= 1

#print(f"jump_server: {jump_server[0]}; try: {3 - retry_jump_server}")
print("JUMP SERVER ====",jump_server)

# result = run_commands(command, jump_server_credentials)
# print(result)

