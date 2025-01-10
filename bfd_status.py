

#condition---State of interfaces should be Up and admin down || NA if no command output 
# || NA if Please enable BFD in global mode first in the command output


data1='''#######################['screen-length 0 temporary', 'display isis interface | exclude Tun|Lo', 'display bfd session all | i D_IP_IF']#######################
Info: The max number of VTY users is 10, and the number
      of current VTY users on line is 1.
      The current login time is 2024-07-24 05:42:23+05:30.
Info:  First time access.  Failed: 0

<APGDVRJMAGR02HNE40>screen-length 0 temporary
Info: The configuration takes effect on the current user terminal interface only.
<APGDVRJMAGR02HNE40>display isis interface | exclude Tun|Lo

                       Interface information for ISIS(1)
                       ---------------------------------
 Interface       Id      IPV4.State          IPV6.State      MTU  Type  DIS   
 Eth-Trunk16.2544
                 002         Up                 Down         9189 L1/L2 --
 Eth-Trunk1.130  001         Up                 Down         9189 L1/L2 --

                       Interface information for ISIS(12)
                       ----------------------------------
 Interface       Id      IPV4.State          IPV6.State      MTU  Type  DIS   
 Eth-Trunk17.2540
                 001         Up                 Down         9189 L1/L2 --
 Eth-Trunk1.100  002         Up                 Down         9189 L1/L2 --
 Eth-Trunk4.2577 013         Up                 Down         9189 L1/L2 --

                       Interface information for ISIS(8)
                       ---------------------------------
 Interface       Id      IPV4.State          IPV6.State      MTU  Type  DIS   
 Eth-Trunk18.2552
                 001         Up                 Down         9189 L1/L2 --
 Eth-Trunk4.8    002         Up                 Down         8997 L1/L2 --
<APGDVRJMAGR02HNE40>display bfd session all | i D_IP_IF
--------------------------------------------------------------------------------
Local Remote     PeerIpAddr      State     Type         InterfaceName           
--------------------------------------------------------------------------------
9739  16424      10.220.86.9     Up        D_IP_IF      Eth-Trunk1.130
9743  16425      10.147.43.21    Up        D_IP_IF      Eth-Trunk1.100
9656  1058       10.220.86.14    Up        D_IP_IF      Eth-Trunk16.2544
10081 1092       10.147.44.110   Up        D_IP_IF      Eth-Trunk18.2552
10255 29252      10.147.44.158   Up        D_IP_IF      Eth-Trunk17.2540
10283 262486     10.220.215.2    Up        D_IP_IF      Eth-Trunk4.8
10280 262487     10.220.57.61    Up        D_IP_IF      Eth-Trunk4.2577
--------------------------------------------------------------------------------
     Total UP/DOWN Session Number : 30/34
<APGDVRJMAGR02HNE40>
#######################END#######################
'''

data2='''#######################['display isis interface | exclude Tun|Lo', 'display bfd session all | i D_IP_IF']#######################
Info: The max number of VTY users is 21, the number of current VTY users online is 1, and total number of terminal users online is 1.
      The current login time is 2024-06-28 09:40:19+05:30.
Warning: The password of the root account is the default password. Please change the password.
<APHYDUPPSAR02HNE40>display isis interface | exclude Tun|Lo
Info: It will take a long time if the content you search is too much or the string you input is too long, you can press CTRL_C to break.

<APHYDUPPSAR02HNE40>display bfd session all | i D_IP_IF
Info: It will take a long time if the content you search is too much or the string you input is too long, you can press CTRL_C to break.
(w): State in WTR
(*): State is invalid
 
 error: in line then print ok
--------------------------------------------------------------------------------
Local      Remote     PeerIpAddr      State     Type        InterfaceName 
--------------------------------------------------------------------------------
16525      16412      10.220.57.77    Up        D_IP_IF     Eth-Trunk1.10
16526      16413      10.220.159.66   Up        D_IP_IF     Eth-Trunk1.11
16710      0          10.110.176.187  Down      D_IP_IF     Eth-Trunk21.306
16711      0          10.110.176.175  Down      D_IP_IF     Eth-Trunk21.325
16712      0          10.110.176.207  Down      D_IP_IF     Eth-Trunk21.318
16713      0          10.110.176.157  Down      D_IP_IF     Eth-Trunk21.302
16714      0          10.110.176.189  Down      D_IP_IF     Eth-Trunk21.323
16715      0          10.110.176.173  Down      D_IP_IF     Eth-Trunk21.310
16716      0          10.110.176.169  Down      D_IP_IF     Eth-Trunk21.305
16717      0          10.110.176.161  Down      D_IP_IF     Eth-Trunk21.319
16718      0          10.110.176.215  Down      D_IP_IF     Eth-Trunk21.316
 23        3          23              Down      D_IP_IF     Eth-Trunk21.324
16720      0          10.110.176.219  Down      D_IP_IF     Eth-Trunk21.307
16721      0          10.110.176.191  Down      D_IP_IF     Eth-Trunk21.324
23         3          2               Down      D_IP_IF     Eth-Trunk21.303
16723      0          10.110.176.171  Down      D_IP_IF     Eth-Trunk21.308
16724      0          10.110.176.165  Down      D_IP_IF     Eth-Trunk21.322
16725      0          10.110.176.163  Down      D_IP_IF     Eth-Trunk21.320
  ---- More ----
#######################END#######################
'''   #empty output

data3=''''''   #empty output

data4=''''''   #empty output

data5=''''<MPRPRRKMSAR01HNE40>display isis interface | exclude Tun|Lo
Info: It will take a long time if the content you search is too much or the string you input is too long, you can press CTRL_C to break.

                       Interface information for ISIS(6)
                       ---------------------------------
 Interface         Id      IPV4.State          IPV6.State      MTU  Type  DIS
 Eth-Trunk1.2523   079         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk25.2589  109         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --    
 Eth-Trunk26.2519  112         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk26.2621  116         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2623  118         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2627  120         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2629  122         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2633  124         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2645  126         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2886  128         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk26.2888  130         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk26.2892  132         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk26.2896  134         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 GE6/0/9.2625      068         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk26.2828  130         Up          Mtu:Up/Lnk:Dn/IP:Dn 8997 L1/L2 --
 Eth-Trunk26.2820  164         Up          Mtu:Up/Lnk:Dn/IP:Dn 8997 L1/L2 --
GigabitEthernet6/  455         Up          Mtu:Up/Lnk:Dn/IP:Dn 8997 L1/L2 -- 
                       Interface information for ISIS(100)
                       ---------------------------------
 Interface         Id      IPV4.State          IPV6.State      MTU  Type  DIS
 Eth-Trunk1.11     077         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk39       022         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk30       132         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2
<MUMUMAIRSBS01>display bfd session all | i D_IP_IF
--------------------------------------------------------------------------------
Local Remote     PeerIpAddr      State     Type         InterfaceName           
--------------------------------------------------------------------------------
8685  52         10.188.187.185  Up        D_IP_IF      Vlanif1003
8686  0          10.188.188.170  Down      D_IP_IF      Vlanif1010
8687  57         10.188.187.201  Up        D_IP_IF      Vlanif1005
8688  54         10.188.187.193  Up        D_IP_IF      Vlanif1004
8689  55         10.188.187.169  Up        D_IP_IF      Vlanif1001
8690  56         10.188.187.177  Up        D_IP_IF      Vlanif1002
                                                        Vlanif1005
8701  0          10.188.188.145  Down      D_IP_IF      Vlanif1009
8702  0          10.188.188.129  Down      D_IP_IF      Vlanif1007
8703  0          10.188.188.137  Down      D_IP_IF      Vlanif1008
--------------------------------------------------------------------------------
     Total UP/DOWN Session Number : 5/5'''

data6=''''''  #empty output


'''import re
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

def bfd_status(data1):  #1,5 ,2,3,4,6 empty
    try:
        if data1 !='':
            lines = data1.casefold().split('\n')
            cleaned_lines = [line for line in lines if line.strip()]    
            index_line=None
            header_row=None 
            for line in cleaned_lines:
                if line.strip().startswith("interface") and line.strip().endswith("dis"):
                    index_line=cleaned_lines.index(line)
                    header_row=re.split(r'\s+',line.strip())  
                                                    
            indices = find_column_indices(header_row)
            if not index_line and not header_row:
                return True,"NA"
            interface_list1=[]
            interface_list2=[]
            interface_counts = {}

            for line in cleaned_lines[index_line:]:
                if line.strip().startswith("local") and line.strip().endswith("interfacename"):
                        index_line2=cleaned_lines.index(line)
                        for line in cleaned_lines[index_line2+1:]:
                            if '----' in line or 'local' in line or 'interfacename' in line or 'error' in line:
                                continue
                            parts_new=re.split(r'\s+',line.strip())
                            print("parts",parts_new)
                            if len(parts_new)<2:
                                continue
                            
                            second_value=parts_new[5],parts_new[4]
                            
                            interface_list2.append(second_value)
                
                if '----' in line or 'interface' in line or 'ifname' in line:
                        continue
                pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
                match = re.findall(pattern, line)
                if match:
                    continue
                parts=re.split(r'\s+',line.strip()) 
                print("parts",parts)
                if len(parts)<2:
                    continue
                f_value=parts[0],parts[2]
                interface_list1.append((f_value))
            print("list 1 =",interface_list1,"\n\n")
            print("list 2 =",interface_list2)
            combined_list=interface_list1+interface_list2
            #print("combined list ",combined_list)
            for f_value, second_value in combined_list:
                if f_value in interface_counts:
                    interface_counts[f_value] += 1  
                else:
                    interface_counts[f_value] = 1
            #print("intercafe count ",interface_counts)
            list_of_interfaces= [(f_value,s_value) for f_value, s_value in combined_list if interface_counts[f_value] >1]
            print("list of intefaces ",list_of_interfaces)
            matched_interfaces=set(list_of_interfaces)
            state_value_list=[lvalue for fvalue,lvalue in matched_interfaces]
            if state_value_list:
                return True,"State of interfaces are Up "
    
            else:
                 return True, "State of interfaces are not Up "
        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    
result=bfd_status(data2)
print(result)'''

import re 
'''pattern = r'Mtu:Dn/Lnk:Dn/IP:Dn|L1/L2'
lines = data1.casefold().split('\n')
cleaned_lines = [line for line in lines if line.strip()]   
list1=[]
list2=[]
for line in cleaned_lines:
    matches = re.findall(pattern,line,re.MULTILINE)
    print("matche=",matches)
    if matches:
        parts=re.split(r'\s+',line.strip()) 
        f_value=parts[0],parts[2]
        list1.append(f_value)
print("list=",list1)'''     

'''pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
matches1 = re.findall(pattern, line, re.MULTILINE)
pattern = r'\b\d+h\d+m\b'
matches2 = re.findall(pattern, line)'''

'''pattern1 = r'mtu:dn/lnk:dn/ip:dn|l1/l2'
pattern2 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
lines = data2.casefold().split('\n')
cleaned_lines = [line for line in lines if line.strip()]   
list1 = []
list2 = []
interface_counts = {}


for line in cleaned_lines:
    matches = re.findall(pattern1, line, re.MULTILINE)
    if matches:
        parts = re.split(r'\s+', line.strip())
    
        f_value = (parts[0], parts[2])
        list1.append(f_value)
for line in cleaned_lines:
    matches = re.findall(pattern2, line, re.MULTILINE)
    if matches:
        parts = re.split(r'\s+', line.strip())
    
        f_value = (parts[5], parts[4])
        list2.append(f_value)

combined_list=list1+list2
 
for f_value, second_value in combined_list:
    if f_value in interface_counts:
        interface_counts[f_value] += 1  
    else:
        interface_counts[f_value] = 1
print("interface dict ",interface_counts)
list_of_interfaces= [(f_value,s_value) for f_value, s_value in combined_list if interface_counts[f_value] >1]
list_new=[(f_value,s_value) for f_value, s_value in list_of_interfaces if s_value!='d_ip_if']
print("fina list ",list_new)
if all(s_value=='up'for f_value, s_value in list_new):
    print("True")
else:
    print("False")    

print("new list =",list_new)
print("final list",list_of_interfaces)'''

def bfd_status(data1):  #1,5 ,2,3,4,6 empty
    try:
        if data1 !='':
           
            lines = data1.casefold().split('\n')
            new_data=data1.casefold().replace(' ', '')
            lines1 = new_data.casefold().split('\n')
            cleaned_lines1 = [line for line in lines1 if line.strip()]
            cleaned_lines = [line for line in lines if line.strip()]   
            list1 = []
            list2 = []
            interface_counts = {}
        
            pattern1 = r'mtu:dn/lnk:dn/ip:dn|l1/l2'
            pattern1_new = r'Mtu:(?:Up|Dn)/Lnk:(?:Up|Dn)/IP:(?:Up|Dn)|L2|L1/L2|L1'

            pattern2 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            first_match = re.findall(pattern1_new, data1, re.MULTILINE)
            second_match = re.findall(pattern2, data1, re.MULTILINE)
            #print("first match",first_match)
            #print("second match",second_match)
            for line in cleaned_lines1:
                if "error:unrecognizedcommandfoundat'^'position" in line:
                    return False,"state of interfaces are not up"
            
            if 'please enable bfd in global mode first' in line:
                    return True,"NA"
                
                
            if not first_match or not second_match:
                return True, "NA"
            for line in cleaned_lines:
                matches = re.findall(pattern1, line, re.MULTILINE)
                if matches:
                    parts = re.split(r'\s+', line.strip())
                
                    f_value = (parts[0], parts[5])
                    list1.append(f_value)
            for line in cleaned_lines:
                matches = re.findall(pattern2, line, re.MULTILINE)
                if matches:
                    parts = re.split(r'\s+', line.strip())
                
                    f_value = (parts[5], parts[3])
                    list2.append(f_value)

            combined_list=list1+list2
            
            for f_value, second_value in combined_list:
                if f_value in interface_counts:
                    interface_counts[f_value] += 1  
                else:
                    interface_counts[f_value] = 1
            print("list 1==",list1,"\n\n")
            print("list 2==",list2)
            #print("interface dict ",interface_counts)
            list_of_interfaces= [(f_value,s_value) for f_value, s_value in combined_list if interface_counts[f_value] >1]
            print("interface matching",list_of_interfaces)
            list_new=[(f_value,s_value) for f_value, s_value in list_of_interfaces if s_value!='l1/l2']
            print("fina list ",list_new)
            if all(s_value=='up' or s_value=='admin down' or s_value=='admin' for f_value, s_value in list_new):
                return True,"state of interfaces are up"

            else:
                return False,"state of interfaces are not up"


           
           
        else: 
            return False ,"NA" 
    except:
        return False ,"Unable to validate output"
    
result=bfd_status(data1)
print(result)


'''def check(data2):
    pattern2 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    matches = re.findall(pattern2, data2, re.MULTILINE)
    print("matches",matches)
    if  not matches:
        return True,"NA"
result=check(data2)
print(result)'''
