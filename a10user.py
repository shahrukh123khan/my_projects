data='''APHYDUPLPSR06#terminal length 0
 
APHYDUPLPSR06#show version
 
Thunder Series Unified Application Service Gateway TH6630
 
  Copyright 2007-2022 by A10 Networks, Inc.  All A10 Networks products are
 
  protected by one or more of the following US patents:
 
  10749904, 10742559, 10735267, 10708150, 10686683, 10659354, 10637717
 
  10630784, 0623992,  RE47924,  10601788, 10599680, 10594600, 10581976
 
  10581907, 10554517, 10536517, 10536481, 10530847, 10523748, 10516730
 
  10516577, 10505984, 10505964, 10491523, 10484465, 10469594, 10454844
 
  10447775, 10411956, 10397270, 10389835, 10389538, 10382562, 10360365
 
  10348631, 10341427, 10341335, 10341118, 10334030, 10318288, 10305904
 
  10305859, 10298457, 10268467, 10257101, 10250629, 10250475, 10243791
 
  RE47296,  10230770, 10187423, 10187377, 10178165, 10158627, 10129122
 
  10116634, 10110429, 10091237, 10069946, 10063591, 10044582, 10038693
 
  10027761, 10021174, 10020979, 10002141, 9992229,  9992107,  9986061
 
  9979801, 9979665, 9961136, 9961135, 9961130, 9960967, 9954899, 9954868
 
  9942162, 9942152, 9912555, 9912538, 9906591, 9906422, 9900343, 9900252
 
  9860271, 9848013, 9843599, 9843521, 9843484, 9838472, 9838425, 9838423
 
  9825943, 9806943, 9787581, 9756071, 9742879, 9722918, 9712493, 9705800
 
  9661026, 9621575, 9609052, 9602442, 9596286, 9596134, 9584318, 9544364
 
  9537886, 9531846, 9497201, 9477563, 9398011, 9386088, 9356910, 9350744
 
  9344456, 9344421, 9338225, 9294503, 9294467, 9270774, 9270705, 9258332
 
  9253152, 9231915, 9219751, 9215275, 9154584, 9154577, 9124550, 9122853
 
  9118620, 9118618, 9106561, 9094364, 9060003, 9032502, 8977749, 8943577
 
  8918857, 8914871, 8904512, 8897154, 8868765, 8849938, 8826372, 8813180
 
  8782751, 8782221, RE44701, 8595819, 8595791, 8595383, 8584199, 8464333
 
  8423676, 8387128, 8332925, 8312507, 8291487, 8266235, 8151322, 8079077
 
  7979585, 7804956, 7716378, 7665138, 7675854, 7647635, 7627672, 7596695
 
  7577833, 7552126, 7392241, 7236491, 7139267, 6748084, 6658114, 6535516
 
  6363075, 6324286, 8392563, 8103770, 7831712, 7606912, 7346695, 7287084
 
  6970933, 6473802, 6374300
 
 
 
          64-bit Advanced Core OS (ACOS) version 4.1.4-GR1-P10, build 65 (Apr-24-2022,06:52)
 
          Booted from Hard Disk primary image
 
          Number of control CPUs is set to 3
 
          Serial Number: TH66083016440008
 
          Firmware version: 5.16
 
          aFleX version: 2.0.0
 
          GUI primary image (default) version 4_1_4-GR1-P10-4_1_4-gr1-p10-8
 
          GUI secondary image version 2_8_2-P5-2_8_2-P5-107
 
          aXAPI version: 3.0
 
          Cylance version: N/A
 
          Hard Disk primary image (default) version 4.1.4-GR1-P10, build 65
 
          Hard Disk secondary image version 2.8.2-P5, build 107
 
          Compact Flash primary image (default) version 2.8.2-P6-SP4, build 9
 
          Compact Flash secondary image version 2.8.2-P5, build 107
 
          Last configuration saved at Apr-10-2024, 00:30
 
          Hardware: 48 CPUs(Stepping 4), Single 93G drive, Free storage is 75G
 
          Total System Memory 130149 Mbytes, Free Memory 105364 Mbytes
 
          Hardware Manufacturing Code: 164411
 
          Current time is Jul-4-2024, 16:28
 
          The system has been up 729 days, 15 hours, 35 minutes
 
APHYDUPLPSR06#show admin session
 
 Id    User Name                       Start Time                    Source IP                               Type        Partition Authen  Role            Cfg  
 
------------------------------------------------------------------------------------------------------------
 
 5     ipchm                           00:57:36 IST Wed Jul 6 2022   127.0.0.1                               CLI                   Local   ReadWriteAdmin  No  
 
*289   snenrc                          16:27:21 IST Thu Jul 4 2024   10.19.32.189                            CLI                   Local   ReadWriteAdmin  No  
 
APHYDUPLPSR06#
#######################END#######################'''
import re
from datetime import datetime,timedelta
def User_status(data):
    try:
        if data != '':
            # pattern1 = r'Current time is ([A-Z][a-z]{3}-\d{2}-\d{4}, \d{2}:\d{2})'
            # pattern2 = r'\d{2}:\d{2}:\d{2} [A-Z]{3} [A-Z][a-z]{2} \w{3} \d{2} \d{4}'
 
            pattern1 = r'Current time is ([A-Z][a-z]{2}-\d{1,2}-\d{4}, \d{2}:\d{2})'
            # Pattern to match the start time
            pattern2 = r'(\d{2}:\d{2}:\d{2} IST [A-Z][a-z]{2} \w{3} \d{1,2} \d{4})'
           
            match = re.search(pattern1, data)
            if match:
                current_time_str=match.group(1)
            else:
                return True, 'NA'    
           
            match= re.findall(pattern2, data, re.MULTILINE)
            for start_time in match:
                print("start time ",start_time)
                
            #print("match list",match)
            for value in match:
              if len(match) != 0:
                start_time_str = match[-1]
              else:
                return True, 'NA'
            start_time = datetime.strptime(start_time_str, '%H:%M:%S IST %a %b %d %Y')
            current_time = datetime.strptime(current_time_str, '%b-%d-%Y, %H:%M')
            print("current time",current_time)
            time_difference = current_time - start_time
            four_hours = timedelta(hours=4)
            if time_difference >= four_hours:
                print("Start time is not less than 4 hours from the current time.")
                return True, 'OK'
            else:
                print("Start time is less than 4 hours from the current time.")
                return False, 'NOK'
        else:
            return False, 'NA'
    except Exception as e:
        return False, 'unable to validate output'
   
print(User_status(data))