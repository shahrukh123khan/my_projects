import re

# ISIS Status 

def find_column_indices(header_row,):   
    indices = {}
    for column in header_row:
        try:
            indices[column] = header_row.index(column)
        except ValueError:
            raise ValueError(f"Column {column} not found in header row.")
    return indices


def isis_status(data1):    #1,2, #empty output 3,4,5,6
    try:
        if data1 !='':
            lines = data1.casefold().split('\n')
            cleaned_lines = [line for line in lines if line.strip()]
            

            for line in cleaned_lines:
                if line.strip().startswith("interface") and line.strip().endswith("dis"):
                    index_line=cleaned_lines.index(line)
                    header_row=re.split(r'\s+',line.strip())           #ine.split()
            indices = find_column_indices(header_row)
            state_list=[]
            for line in cleaned_lines[index_line:]:
                    if '-------' in line or 'interface' in line :
                        continue
                    parts=re.split(r'\s+',line.strip())
                    ipv4_state_value = parts[indices["ipv4.state"]]      #   ipv=parts[7]
                    state_list.append(ipv4_state_value)
            print("state list",state_list)
            if all(value == 'up' or value=='admin' or value=='down' for value in state_list):
                return True,"All IPV4.State are Up & admin down"
    
            else:
                 return False, "All IPV4.State are not Up"
        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    
#LDP Status

def ldp_status(data1):  #1,2,3,4,5,6
    try:
        if data1 !='':
            lines = data1.casefold().split('\n')
            cleaned_lines = [line for line in lines if line.strip()]    
            for line in cleaned_lines:
                if line.strip().startswith("interface") and line.strip().endswith("dis"):
                    index_line=cleaned_lines.index(line)
                    header_row=re.split(r'\s+',line.strip())  
                                                    
            #indices = find_column_indices(header_row)
            interface_list=[]
            interface_counts = {}

            for line in cleaned_lines[index_line:]:
                if '----' in line or 'interface' in line or 'ifname' in line:
                        continue
                parts=re.split(r'\s+',line.strip())
                if len(parts)<2:
                    continue
                first_value,second_value=parts[0],parts[1]
                interface_list.append((first_value,second_value))
            for f_value, second_value in interface_list:
                if f_value in interface_counts:
                    interface_counts[f_value] += 1
                else:
                    interface_counts[f_value] = 1
            list_of_interfaces= [(f_value,s_value) for f_value, s_value in interface_list if s_value == 'active' and interface_counts[f_value] > 1]
            matched_interfaces=set(list_of_interfaces)
            active_list=[lvalue for fvalue,lvalue in matched_interfaces]
        
            if active_list:
                print("final list ",active_list,len(active_list))
                return True,"Status of interfaces are Active"
    
            else:
                 return False, "Status of interfaces are not Active"
        else: 
            return False ,"False NA"  
    except:
        return False ,"Unable to validate output"

# bfd status 

def bfd_status(data1):  #1,5 ,2,3,4,6 empty
    try:
        if data1 !='':
            lines = data1.casefold().split('\n')
            cleaned_lines = [line for line in lines if line.strip()]    
            for line in cleaned_lines:
                if line.strip().startswith("interface") and line.strip().endswith("dis"):
                    index_line=cleaned_lines.index(line)
                    header_row=re.split(r'\s+',line.strip())  
                                                    
            #indices = find_column_indices(header_row)
            interface_list1=[]
            interface_list2=[]
            interface_counts = {}

            for line in cleaned_lines[index_line:]:
                if line.strip().startswith("local") and line.strip().endswith("interfacename"):
                        for line in cleaned_lines[32:]:
                            if '----' in line or 'local' in line or 'interfacename' in line:
                                continue
                            parts_new=re.split(r'\s+',line.strip())
                            if len(parts_new)<5:
                                continue
                            second_value=parts_new[5],parts_new[3]
                            interface_list2.append(second_value)
                
                if '----' in line or 'interface' in line or 'ifname' in line:
                        continue
                parts=re.split(r'\s+',line.strip()) 
                if len(parts)<2:
                    continue
                f_value=parts[0],parts[1]
                interface_list1.append((f_value))
            combined_list=interface_list1+interface_list2
            for f_value, second_value in combined_list:
                if f_value in interface_counts:
                    interface_counts[f_value] += 1  
                else:
                    interface_counts[f_value] = 1
            list_of_interfaces= [(f_value,s_value) for f_value, s_value in combined_list if s_value == 'up' and interface_counts[f_value] >1]
            matched_interfaces=set(list_of_interfaces)
            state_value_list=[lvalue for fvalue,lvalue in matched_interfaces]
            if state_value_list:
                return True,"State of interfaces are Up and admin down"
    
            else:
                 return True, "State of interfaces are not Up and admin down"
        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    
# bgp neighbor status 
def bgp_status(data1):  #1,2, #empty output 3,4,5,6
    try:
        if data1 !='':
            lines = data1.casefold().split('\n')
            for line in lines:
                if line.strip().startswith("peer") and line.strip().endswith("prefrcv"):
                    index_line=lines.index(line)
                    print("index line ",index_line)
                    header_row=re.split(r'\s+',line.strip())           #ine.split()
            indices = find_column_indices(header_row)
            state_list=[]
            for line in lines[index_line+1:]:
                parts=re.split(r'\s+',line.strip())
                print("parts",parts)
                ipv4_state_value = parts[indices["state"]]      #   ipv=parts[7]
                state_list.append(ipv4_state_value)
            if all(value=='established' or value=='admin' or value=='down' for value in state_list):
                
                return True,"All State are Established and admin down"
    
            else:
                 return False, "All State are not Established and admin down"
        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"    

#ntp status

def ntp_status(data):  #1,2,3,4,5,6
    try:
        if data !='':
            clock_sources = 0
            master_status_found = False
            data1_no_spaces = data.replace(' ', '')
            lines=data1_no_spaces.casefold().split('\n')
            for line in lines:
                    if 'clocksource:' in line:
                                clock_sources += 1
                    if 'clockstatus:configured,master,sane,valid' in line:
                                master_status_found = True
            if clock_sources >= 2 and master_status_found:
                                return True,"Atlest two clock source are available  and One clock status is configured, master, sane, valid"
            else:
                return False,"Atlest two clock source are not available  and One clock status is not configured, master, sane, valid"
        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    
# user status

def user_check(data,threshold):  #1,2,3,4,5,6
    try:
        if data !='':
            delay_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')
            delay_values = delay_pattern.findall(data)
            #matching_delays = [delay for delay in delay_values if delay <=threshold]
            if all(value<=f'{threshold}' for value in delay_values):
                 return True,"Delay is less than four hours"
            else: 
                return False, "Delay is not less than four hours"
        else:   
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    