

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


data6=''''''  #empty output

import re
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
            index_line=None
            up_list=[]
            pattern1 = r'mtu:dn/lnk:dn/ip:dn|l1/l2'
            pattern1_new = r'Mtu:(?:Up|Dn)/Lnk:(?:Up|Dn)/IP:(?:Up|Dn)|L2|L1/L2|L1'

            pattern2 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            first_match = re.findall(pattern1_new, data1, re.MULTILINE)
            second_match = re.findall(pattern2, data1, re.MULTILINE)
            print("first match",first_match)
            print("second match",second_match)
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
                    print(parts)
                    f_value = parts[0]
                    list1.append(f_value)
            for line in cleaned_lines:
                matches = re.findall(pattern2, line, re.MULTILINE)
                if matches:
                    parts = re.split(r'\s+', line.strip())
                    print(parts)
                    f_value = parts[5]
                    list2.append(f_value)

            combined_list=list1+list2
            
            for value in combined_list:
                if value in interface_counts:
                    interface_counts[value] += 1  
                else:
                    interface_counts[value] = 1
            print("list 1==",list1,"\n\n")
            print("list 2==",list2)
            print("interface dict ",interface_counts)
            list_of_interfaces=[value for value in interface_counts if interface_counts[value]>1]
            print("interface matching",list_of_interfaces)
          
            for line in cleaned_lines:
                if line.strip().startswith("local") and 'state' in line:
                    index_line=cleaned_lines.index(line)
            
            for line in cleaned_lines[index_line+1:]:
                for value in list_of_interfaces:
                    if value in line:
                        parts = re.split(r'\s+', line.strip())
                        data=parts[3]
                        up_list.append(data)
            print("list of up",up_list)
            

            if all(value=='up' or value=='admin down' or value=='admin' for value in up_list):
                return True,"state of interfaces are up"

            else:
                return False,"state of interfaces are not up"     
        else: 
            return False ,"NA" 
    except:
        return False ,"Unable to validate output"
    
# result=bfd_status(data1)
# print(result)




        




import re
def bfd_status(data1):  #1,5 ,2,3,4,6 empty
    try:
        if data1 !='':
            interface_list=[]
            start_marker = ' Interface information for ISIS'
            end_marker = 'display bfd session all | i D_IP_IF'
            #print("interface ist ",interface_list)        
            lines = data1.casefold().split('\n')
            new_data=data1.casefold().replace(' ', '')
            lines1 = new_data.casefold().split('\n')
            cleaned_lines1 = [line for line in lines1 if line.strip()]
            cleaned_lines = [line for line in lines if line.strip()]   
            list1 = []
            list2 = []
            interface_counts = {}
            index_line=None
            up_list=[]
            pattern1 = r'mtu:dn/lnk:dn/ip:dn|l1/l2'
            pattern1_new = r'Mtu:(?:Up|Dn)/Lnk:(?:Up|Dn)/IP:(?:Up|Dn)|L2|L1/L2|L1'

            pattern2 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            first_match = re.findall(pattern1_new, data1, re.MULTILINE)
            second_match = re.findall(pattern2, data1, re.MULTILINE)
            # print("first match",first_match)
            # print("second match",second_match)
            for line in cleaned_lines1:
                if "error:unrecognizedcommandfoundat'^'position" in line:
                    return False,"state of interfaces are not up"
            
            if 'please enable bfd in global mode first' in line:
                    return True,"NA"
                
                
            if not first_match or not second_match:
                return True, "NA"
            start_index = data1.find(start_marker)
            end_index = data1.find(end_marker, start_index + len(start_marker))

            if start_index != -1 and end_index != -1:
                interface_data = data1[start_index + len(start_marker):end_index]
                print(interface_data,type(interface_data),"\n\n\n")

            # lines=interface_data.split('\n')
            trimed_lines = interface_data.casefold().split('\n')
            interface_cleaned_lines = [line for line in trimed_lines if line.strip()]
            for line in interface_cleaned_lines:
                if '---' in line or 'interface information of isis' in line or 'interface' in line or '<' in line:
                     continue
                parts = re.split(r'\s+', line.strip())
                if len(parts)==1 or len(parts)==7:
                    value=parts[0]
                    interface_list.append(value)
            for line in cleaned_lines:
                matches = re.findall(pattern1, line, re.MULTILINE)
                if matches:
                    parts = re.split(r'\s+', line.strip())
                    #print(parts)
                    f_value = parts[0]
                    list1.append(f_value)
            for line in cleaned_lines:
                matches = re.findall(pattern2, line, re.MULTILINE)
                if matches:
                    parts = re.split(r'\s+', line.strip())
                    #print(parts)
                    f_value = parts[5]
                    list2.append(f_value)

            combined_list=interface_list+list2
            
            for value in combined_list:
                if value in interface_counts:
                    interface_counts[value] += 1  
                else:
                    interface_counts[value] = 1
            # print("list 1==",list1,"\n\n")
            print("list 2==",list2)
            # print("interface dict ",interface_counts)
            list_of_interfaces=[value for value in interface_counts if interface_counts[value]>1]
            print("interface matching",list_of_interfaces)
          
            for line in cleaned_lines:
                if line.strip().startswith("local") and 'state' in line:
                    index_line=cleaned_lines.index(line)
            
            for line in cleaned_lines[index_line+1:]:
                for value in list_of_interfaces:
                    if value in line:
                        parts = re.split(r'\s+', line.strip())
                        data=parts[3]
                        up_list.append(data)
            print("list of up",up_list)
            

            if all(value=='up' or value=='admin down' or value=='admin' for value in up_list):
                return True,"state of interfaces are up"

            else:
                return False,"state of interfaces are not up"     
        else: 
            return False ,"NA" 
    except:
        return False ,"Unable to validate output"
    
result=bfd_status(data1)
print(result)