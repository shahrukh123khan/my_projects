import re

def card_status(data1):  #1,2,3,4,5,6
    try:
        if data1 !='':
            pattern = r'L2/3 ASIC'
            matches = re.findall(pattern, data1)
            if not matches:
                return True,"NA"
            list=[]
            lines = data.casefold().split('\n') 
            cleaned_lines = [line for line in lines if line.strip()]    
            for line in cleaned_lines:
                if 'l2/3 asic' in line:
                    list.append(line)
            print(list)
            if all('present' in value for value in list):
                return True,"OK"
            else:
                return False,"NOK" 

        else: 
            return False ,"NA"  
    except:
        return False ,"Unable to validate output"
    

    import re
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


def ntp_status(data1):    #1,2, #empty output 3,4,5,6
    try:
        if data1 !='':
            pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            lines = data1.casefold().split('\n')
            cleaned_lines = [line for line in lines if line.strip()]
            index_line=None
            header_row=None
            for line in cleaned_lines:
                if 'ntp' in line or 'server' in line or 'status' in line:
                    index_line=cleaned_lines.index(line)
                    print("index line ",index_line)
                    header_row=re.split(r'\s+',line.strip())     
                    print("header row",header_row)
            indices = find_column_indices(header_row)
            if not index_line and not header_row:
                return True,"NA"
            
            state_list=[]
            
            for line in cleaned_lines[index_line+1:]:
                    match = re.findall(pattern, line)
                    print("line",line)
                    if match:
                        parts=re.split(r'\s+',line.strip())
                        print(parts)
                        '''if len(parts)<2:
                            continue'''
                        print("header row in new ",header_row)
                        if 'server' in header_row:
                            print("parts value ",parts[indices["server"]])
                            ipv4_state_value = parts[indices["server"]]      #   ipv=parts[7]
                            print("value",ipv4_state_value)
                            state_list.append(ipv4_state_value)
                        else:
                            print("parts value ",parts[indices["status"]])
                            ipv4_state_value = parts[indices["status"]]      #   ipv=parts[7]
                            print("value",ipv4_state_value)
                            state_list.append(ipv4_state_value)
                    '''else:
                        return True,"NAA"'''
            print("state list",state_list)        
            if all(value == 'synchronized' or value=='polling'  for value in state_list):
                return True,"All synchronized"
    
            else:
                 return False, "All not synchronized"
        else: 
            return True ,"NA"  
    except:
        return False ,"Unable to validate output"


def memory_status(data):
    try:
        if data !='':
            list=[]
            pattern = r"^Memory:\s+\d+\s+\d+\s+\d+\s+\d{1,2}(?:\.\d{1,2})?%$"
            matches = re.findall(pattern, data, re.MULTILINE)
            if not matches:
                return True,"NA"
            
            for match in matches:
                pattern = r"\b\d{1,2}(?:\.\d{1,2})?%"
                m = re.findall(pattern, match)
                list.append(m)
            flat_list = sum(list, [])
            if all(value<="80%" for value in flat_list):
                return True,"memory usage is not greater than 80%"
            else:
                return False,"memory usage is greater than 80%"
            print("final list ",final_list)
        else:
            
            return True ,"NA"  
    except:
        return False ,"Unable to validate output"
    

def cpu_status(data):
    try:
        if data !='':
            list=[]
            lines = data.casefold()
            pattern = r'control\d+\s+\d+%\s+\d+%\s+\d+%\s+\d+%\s+\d+%'
            matches = re.findall(pattern, lines, re.MULTILINE)
            print("list",matches)
            for line in matches:
                parts=re.split(r'\s+',line.strip())
                value=parts[5]
                list.append(value)
            print(list)
            if not matches:
                return True,"NA"
            if all(value<='60%' for value in list):
                return True,"control 60sec is not greater than 60%"
            else:
                return False,"control 60sec is greater than 60%"
        else:
            
            return True ,"NA"  
    except:
        return False ,"Unable to validate output"