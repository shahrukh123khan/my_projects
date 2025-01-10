#condition -- All State should be Established and admin down || NA if no command output 
#|| state should not be Idle,Active,Connect,OpenSent and OpenConfirm in all six category 
import re 
import pandas as pd
from io import StringIO
data1='''<MPRPRRKMSAR01HNE40>display bgp vpnv4 all peer 
 
 BGP local router ID : 10.220.3.15  
 Local AS number : 55410
 Total number of peers : 31                 
      '''

data2='''#######################['screen-length 0 temporary', 'display bgp peer', 'display bgp vpnv4 all peer', 'display bgp vpnv6 all peer']#######################
Info: The max number of VTY users is 20, the number of current VTY users online is 1, and total number of terminal users online is 1. 
      The current login time is 2024-06-29 12:56:14+05:30. 
<APGNTKPDACR01HA910>screen-length 0 temporary 
Info: The configuration takes effect on the current user terminal interface only. 
<APGNTKPDACR01HA910>display bgp peer 
2024-06-29 12:56:34.858 +05:30 

<APGNTKPDACR01HA910>
#######################END#######################'''

data3=''''''  # empty outputs

data4='''#######################display bgp all summary#######################
Info: The max number of VTY users is 20, the number of current VTY users online is 1, and total number of terminal users online is 1.
      The current login time is 2024-06-28 09:46:13+05:30.
<APHYDUPLSAR02HNE90>display bgp all summary
 
 BGP local router ID : 10.220.136.194 
 Local AS number : 55410

 Address Family:Ipv4 Unicast
 --------------------------------------------------------------------------------------------
 Total number of peers : 97                 Peers in established state : 92



#######################END#######################

'''  # empty outputs

data5=''''''  # empty outputs

data6=''''''  # empty outputs

new_data='''#######################['screen-length 0 temporary', 'display bgp peer', 'display bgp vpnv4 all peer', 'display bgp vpnv6 all peer']#######################
Info: The max number of VTY users is 10, and the number 
      of current VTY users on line is 1. 
      The current login time is 2024-07-03 09:09:07+05:30. 
<MHNGPWDIPSR06HNE40>screen-length 0 temporary 
Info: The configuration takes effect on the current user terminal interface only. 
<MHNGPWDIPSR06HNE40>display bgp peer 
<MHNGPWDIPSR06HNE40>display bgp vpnv4 all peer 
BGP local router ID : 10.137.186.55 
Local AS number : 65089 
Total number of peers : 37		  Peers in established state : 37
  Peer            V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State PrefRcv 

  Peer of IPv4-family for vpn instance : 
VPN-Instance Ga, Router ID 10.137.186.53: 
  10.137.184.45   4       55644  1655031  1648368     0 **23232h*123422m Established       4 
  10.137.186.9    4       65089  7587751  7587670     0 ****h48m Established       8 
VPN-Instance Gb, Router ID 10.137.186.62: 
  10.137.186.73   4       65089  7981101  7939084     0 ****h10m Established      76 
  10.220.104.121  4       55644  1808834  1648370     0 ****h23m Established      75 
VPN-Instance Gi_bbry, Router ID 10.137.186.50: 
  10.137.184.141  4       55644  1648326  1648364     0 ****h23m Established       0 
  10.137.186.33   4       65089  7582521  7582450     0 ****h48m Established       3 
VPN-Instance Gi_int4, Router ID 10.137.186.48: 
  10.137.182.97   4       65080    22697    22699     0 0189h06m Established       2 
  10.137.186.25   4       65089  7806054  7804877     0 ****h48m Established      15 
  10.137.206.80   4       65089  3492770  2995981     0 ****h29m Established       3 
VPN-Instance Gi_wap, Router ID 10.137.186.49: 
  10.137.184.125  4       55644  1648327  1648365     0 ****h23m Established       0 
  10.137.186.29   4       65089  7582391  7582311     0 ****h48m Established       4 
VPN-Instance Gn, Router ID 10.137.186.46: 
  10.137.182.105  4       65080    22364    22351     0 0186h13m Established      26 
  10.137.186.1    4       65089 12806960 12773540     0 ****h48m Established    2937 
  10.220.147.61   4       55644  3436701  1648468     0 ****h23m Established    2900 
  10.220.147.77   4       55644  1952694  1648367     0 ****h24m Established     106 
VPN-Instance Gr, Router ID 10.137.186.66: 
  10.110.213.110  4       55644  1648847  1648419     0 ****h23m Established       8 
  10.137.182.133  4       65080    63116    63117     0 0525h57m Established       4 
  10.137.186.89   4       65089  7520293  7520330     0 ****h24m Established      13 
  10.137.206.88   4       65089  3492596  2996089     0 ****h29m Established       2 
VPN-Instance GxGy, Router ID 10.137.186.51: 
  10.137.184.29   4       55644  1668211  1648362     0 ****h23m Established     105 
  10.137.186.5    4       65089  7597104  7596736     0 ****h48m Established     130 
VPN-Instance IUPS-CP, Router ID 10.137.186.64: 
  10.137.186.81   4       65089  7572359  7571953     0 ****h10m Established       1 
  10.220.104.113  4       55644  1648326  1648372     0 ****h23m Established       0 
VPN-Instance IUPS-UP, Router ID 10.137.186.65: 
  10.137.186.85   4       65089 12947440 12906089     0 ****h10m Established    2940 
  10.220.104.105  4       55644  1648328  1648390     0 ****h24m Established       0 
VPN-Instance LTE_SIG, Router ID 10.137.186.54: 
  10.137.186.17   4       65089  7603759  7602626     0 ****h48m Established      94 
  10.220.65.85    4       55644  1649125  1648369     0 ****h23m Established      15 
  10.220.104.137  4       55644  1668966  1648474     0 ****h23m Established      68 
VPN-Instance Li, Router ID 10.137.186.52: 
  10.112.188.170  4       55410 12904063   291758     0 2431h17m Established       2 
  10.137.184.61   4       55644  1655031  1648366     0 ****h23m Established       5 
  10.137.186.13   4       65089  7588156  7587752     0 ****h48m Established      12 
VPN-Instance OAM, Router ID 10.137.186.55: 
  10.137.182.150  4       65080    63146    63123     0 0525h57m Established      22 
  10.137.184.161  4       65089  7592095  7592882     0 ****h48m Established      44 
VPN-Instance S1_MME, Router ID 10.137.186.63: 
  10.137.186.77   4       65089 12528557 12523067     0 ****h53m Established   19202 
  10.220.104.129  4       55644  3333243  1648398     0 ****h23m Established   19200 
VPN-Instance S1_U, Router ID 10.137.186.47: 
  10.137.184.93   4       55644  3602113  1648379     0 ****h23m Established   19202 
  10.137.186.21   4       65089 12683673 12682299     0 ****h48m Established   19216 
<MHNGPWDIPSR06HNE40>display bgp vpnv6 all peer 
BGP local router ID : 10.137.186.55 
Local AS number : 65089 
Total number of peers : 6		  Peers in established state : 6
  Peer            V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State PrefRcv 

  Peer of IPv6-family for vpn instance : 
VPN-Instance Gi_ims64, Router ID 10.137.186.55: 
  2402:8100:1:0:80::224 
                  4       55644  1107422  1106995     0 9224h57m Established       1 
VPN-Instance Gi_intv6, Router ID 10.137.186.55: 
  2402:8100:1:0:31::2E0 
                  4       65089  3492905  4076393     0 ****h30m Established      21 
  2402:8100:1:0:80::12 
                  4       65089  9786966  9814415     0 ****h48m Established    2012 
  2402:8100:1:0:80::31 
                  4       55644  1649446  2386202     0 ****h24m Established       2 
  2402:8100:1:1:49::1 
                  4       65080    35487    36262     0 0230h47m Established    1083 
VPN-Instance S1_U, Router ID 10.137.186.55: 
  2402:8100:4000::6:0:1B 
                  4       55644   525026   525035     0 4375h17m Established       1 
<MHNGPWDIPSR06HNE40>
#######################END#######################'''



new_data1='''#######################['screen-length 0 temporary', 'display bgp peer']#######################
Info: The max number of VTY users is 5, the number of current VTY users online is 1, and total number of terminal users online is 1.
      The current login time is 2024-07-04 12:50:55+05:30.
      The last login time is 2024-07-04 12:49:52+05:30 from 10.19.32.189 through SSH.
<DLDLHMCIIMS05>screen-length 0 temporary
Info: The configuration takes effect on the current user terminal interface only.
<DLDLHMCIIMS05>display bgp peer
BGP local router ID : 10.137.186.55 
Local AS number : 65089 
Total number of peers : 37		  Peers in established state : 37
  Peer            V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State PrefRcv 

  Peer of IPv4-family for vpn instance : 
VPN-Instance Ga, Router ID 10.137.186.53: 
  10.137.184.45   4       55644  1655031  1648368     0 **23232h*123422m Established       4 
  10.137.186.9    4       65089  7587751  7587670     0 ****h48m Established       8 
VPN-Instance Gb, Router ID 10.137.186.62: 
  10.137.186.73   4       65089  7981101  7939084     0 ****h10m Established      76 
  10.220.104.121  4       55644  1808834  1648370     0 ****h23m Established      75 
VPN-Instance Gi_bbry, Router ID 10.137.186.50: 
  10.137.184.141  4       55644  1648326  1648364     0 ****h23m Established       0 
  10.137.186.33   4       65089  7582521  7582450     0 ****h48m Established       3 
VPN-Instance Gi_int4, Router ID 10.137.186.48: 
  10.137.182.97   4       65080    22697    22699     0 0189h06m Established       2 
  10.137.186.25   4       65089  7806054  7804877     0 ****h48m Established      15 
  10.137.206.80   4       65089  3492770  2995981     0 ****h29m Established       3 
VPN-Instance Gi_wap, Router ID 10.137.186.49: 
  10.137.184.125  4       55644  1648327  1648365     0 ****h23m Established       0 
  10.137.186.29   4       65089  7582391  7582311     0 ****h48m Established       4 
VPN-Instance Gn, Router ID 10.137.186.46: 
<DLDLHMCIIMS05>
#######################END#######################
'''


new_data2='''BGP Neighbor status value: ['screen-length 0 temporary', 'display bgp peer', 'display bgp vpnv4 all peer', 'display bgp vpnv6 all peer']
output: Info: The max number of VTY users is 10, and the number
      of current VTY users on line is 1.
      The current login time is 2024-07-06 14:04:02+05:30.
Info:  First time access.  Failed: 0

<APHYDUPLMBR01HNE40>screen-length 0 temporary
Info: The configuration takes effect on the current user terminal interface only.
<APHYDUPLMBR01HNE40>display bgp peer

 BGP local router ID : 10.144.80.27
 Local AS number : 65501
 Total number of peers : 9                Peers in established state : 9

  Peer            V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State PrefRcv

  10.144.80.19    4       65501   820412 30861486     0 ****h25m Established       3
  10.144.80.20    4       65501   909649 30861486     0 ****h26m Established       3
  10.144.80.28    4       65501 45243316 30861486     0 ****h17m Established       7
  10.144.80.31    4       65501   154564 13729525     0 2559h30m Established       4
  10.144.80.32    4       65501  6320179 11679075     0 2559h30m Established      12
  10.144.80.33    4       65501  1109109 30861486     0 ****h40m Established       1
  10.144.80.34    4       65501  1107445 30861486     0 ****h40m Established       1
  10.144.80.39    4       65501   156285 13729526     0 2559h30m Established       3
  10.144.80.40    4       65501   178405 13729524     0 2559h30m Established       3
<APHYDUPLMBR01HNE40>display bgp vpnv4 all peer

 VPN-Instance SIGNALING-VOICE, Router ID 10.144.80.27:
  10.110.102.18   4       55644   131863   110177     0 1836h02m Established       8
  10.110.108.213  4       55644   107695    90060     0 1500h55m Established       4
  10.112.221.152  4       65111   173836   173435     0 2889h11m Established       2
  10.115.254.49   4       65000   126364   114903     0 0957h29m Established       0
  10.144.67.140   4       65175  2032404  2080958     0 2890h35m Established      10
  10.144.67.173   4       65175  2032578  2079191     0 2890h35m Established      25
  10.147.145.229  4       65502   162291   163741     0 2724h49m Established       6
  10.160.8.137    4       55644   108846    99284     0 0827h17m Established      69
  10.188.16.225   4       55644   140255   130289     0 1085h10m Established     223
  10.188.157.202  4       65201  1450409   546726     0 ****h16m Established       2
  10.188.193.34   4       65201  1099866   546672     0 ****h21m Established       4
  10.196.182.46   4       65065        0        0     0 0695h36m Idle(Admin)       0
  10.196.182.118  4       55644  2126890   110237     0 1836h01m Established    9337
  10.220.57.209   4       55644   132068   110701     0 1836h02m admin down      54
  10.220.58.33    4       55644   131865   111093     0 1836h02m Established      18

<APHYDUPLMBR01HNE40>display bgp vpnv6 all peer
<APHYDUPLMBR01HNE40>'''
def find_column_indices(header_row,):   
    indices = {}
    if header_row is None:
        return header_row
    for column in header_row:
        try:
            indices[column] = header_row.index(column)
        except ValueError:
            raise ValueError(f"Column {column} not found in header row.")
    return indices


'''def bgp_status(data1):    #1,2, #empty output 3,4,5,6
    try:
        if data1 !='':
            lines = data1.casefold().split('\n')
            cleaned_lines = [line for line in lines if line.strip()]
            index_line=None
            header_row=None
            for line in cleaned_lines:
                
                if line.strip().startswith("peer") or 'state' in line :                 #line.strip().endswith("prefrcv")
            
                    index_line=cleaned_lines.index(line)
                    #print("index line value ",index_line)

                    header_row=re.split(r'\s+',line.strip())     
                    #print("header row",header_row)
            indices = find_column_indices(header_row)
            if not index_line and not header_row:
                return True,"NA"
            state_list=[]
            
            for line in cleaned_lines[index_line+1:]:
                    if '----' in line or 'interface' in line or '###' in line or  'error' in line or 'peer' in line or 'state' in line:
                        continue
                    parts=re.split(r'\s+',line.strip())
                    print("parts",parts)
                    if len(parts)<7:
                        continue
                    ipv4_state_value = parts[indices["state"]]      #   ipv=parts[7]
                    state_list.append(ipv4_state_value)
            #print("state list",state_list)
            if all(value == 'established' or value=='admin' or value=='down' for value in state_list):
                return True,"All IPV4.State are  established & admin down"
    
            else:
                 return False, "All IPV4.State are not established"
        else: 
            return True ,"NA"  
    except:
        return False ,"Unable to validate output"
    
result=bgp_status(new_data)
print(result)'''

def bgp_status(data1):  #1,2,3,4,5,6
    try:
        if data1 !='':
            
            list=[]
            new_data=data1.casefold().replace(' ', '')
            lines1 = new_data.casefold().split('\n')
            cleaned_lines1 = [line for line in lines1 if line.strip()]
            lines = data1.casefold().split('\n') 
            cleaned_lines = [line for line in lines if line.strip()]    
            index_line=None
            header_row=None 
            for line in cleaned_lines1:
              print(line)
              if "error:unrecognizedcommandfoundat'^'position" in line:
                  return False,"All State should be not established and admin down" 

            for line in cleaned_lines:
                if line.strip().startswith("peer") and 'state' in line:
                    index_line=cleaned_lines.index(line)
                    header_row=re.split(r'\s+',line.strip()) 
            
            
            if not index_line and not header_row:
                return True,"NA"
             
                                                    
            indices = find_column_indices(header_row)
            
            for line in cleaned_lines[index_line+1:]:
                if 'router id' in line or 'current login time' in line or 'last login time' in line:
                    continue
                #print("line=",line)
                pattern1 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
                matches1 = re.findall(pattern1, line, re.MULTILINE)
                #print("matches 1 ",matches1)
                pattern2 = r'[\d*]+h[\d*]+m'
                matches2 = re.findall(pattern2, line)
                #print("matches 2 ",matches2)
                
                if matches1 or matches2:
                    print("line==",line)
                    list.append(line)
            #print(list)
            if all('established' in value or 'idle(admin)'in value or 'admin down' in value for value in list):
                return True,"All State should be established and admin down"
            else:
                return False,"All State should be not established and admin down" 

        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    

result=bgp_status(new_data1)
print(result)
                       




   