#conditon---L2/3 ASIC should be present
data='''#######################['terminal length 0', 'show hardware']#######################
Last login: Tue Jul  2 13:48:35 2024 from 10.19.32.189

terminal length 0

System is ready now.

This system is for the use of authorized users only. Individuals using this system without authority or in excess of their authority are subject to having all of their activities on this system monitored and recorded by system personnel. In the course of monitoring individuals improperly using this system, or in the course of system maintenance, the activity of authorized users may also be monitored. Anyone using this system expressly consents to such monitoring and is advised that if such monitoring reveals possible evidence of criminal activity , system personnel may provide the evidence of such monitoring to law enforcement officials 


APHYDUPLPSR09#show hardware
Thunder Series Unified Application Service Gateway TH6630
      Serial No  : TH660F3018460010
      CPU        : Intel(R) Xeon(R) CPU E5-2697 v2 @ 2.70GHz
                   48 cores
                   4 stepping
      Storage    : Single 93G drive, Free storage is 78G
      Memory     : Total System Memory 130149 Mbytes, Free Memory 105117 Mbytes


      L2/3 ASIC  : 5 device(s) present
      IPMI       : IPMI Present

      Ports      : 16  
      Flags      : CF
      SMBIOS     : Build  4.6.5
                    04/25/2014
      FPGA       : 8 instance(s) present
                   Date: 12/01/2021
APHYDUPLPSR09#
#######################END#######################'''


import re

def card_status(data1):  #1,2,3,4,5,6
    try:
        if data1 !='':
            pattern = r'L2/3 ASIC'
            matches = re.findall(pattern, data)
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
    


result=card_status(data)
print(result)
                       



             
                           
                
            
