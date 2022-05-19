import os
import pandas as pd
import argparse
import datetime
import sys
import re
import xml.etree.ElementTree as ET

End_time = 0
start_time = datetime.datetime.now()
#Path_S = raw_input("Enter a Path to session : ")
Path_S = input("Enter a Path to session : ")
frame_number_dict_list_ILOG = []
LINE_MISSING_ILOG = 0
LINE_MISSING_PSLOG = 0
total_traffic_lane_PS = []
NV_for_traffic_count_speed_70_72 = []
execuition_count = 0

def ILOG_check(Path):
    with open (Path) as ILOG:
        frame_number_ILOG_int = []
        
        ILOG_empty_line = 0
        Primary_speed_ILOG = []
        frame_number_ILOG = []
        Quarantine_code_ILOG = []
        ILOG_LANE_ID = []
        ILOG_LANE_Direction = []
        Total_Count_Lane1 = 0
        Total_Count_Lane2 = 0
        Total_Count_Lane3 = 0
        Total_Count_Lane4 = 0
        Total_Count_Lane5 = 0
        Total_Count_Lane6 = 0
        Total_Count_NV_Lane1 = 0
        Total_Count_NV_Lane2 = 0
        Total_Count_NV_Lane3 = 0
        Total_Count_NV_Lane4 = 0
        Total_Count_NV_Lane5 = 0
        Total_Count_NV_Lane6 = 0
        Total_Count_TA_Lane1 = 0
        Total_Count_TA_Lane2 = 0
        Total_Count_TA_Lane3 = 0
        Total_Count_TA_Lane4 = 0
        Total_Count_TA_Lane5 = 0
        Total_Count_TA_Lane6 = 0
        Total_Count_SC_Lane1 = 0
        Total_Count_SC_Lane2 = 0
        Total_Count_XX = 0
        Total_Count_NV = 0
        Total_Count_TS = 0
        Total_Count_MP = 0
        SSV_Corroborated_speed = []
        SSV_Corroborated_speed_InT = []
        Primary_speed_ILOG_int = []
        frame_number_dict = {}
        frame_number_dict_list = []
        Ta_count_counter = 0
        NV_for_traffic_count1 = 0
        NV_for_traffic_count2 = 0
        NV_for_traffic_count3 = 0
        NV_for_traffic_count4 = 0
        NV_for_traffic_count5 = 0
        NV_for_traffic_count6 = 0
        NV_for_traffic_count = []        
        iamin = 'ILOG'
        for line in ILOG.readlines():
            if line in ['\n','\r\n']:
                ILOG_empty_line += 1
                print("XXXXXXXXXX-> Fail: The Empty line is found in : '{}'.".format(str(Path)))
                break
            else:
                attributes = line.split(',')
                number_attribute_ILOG = len(attributes)
                if(attributes[17] == 'SC'):
                    if((attributes[16] != 'F') and (attributes[16] != 'P')):
                        SSV_Corroborated_speed.append(attributes[14])
                        print("SSV corroborated with PSMD and SSMD Speed : '{}'.'{}'.'{}'.".format(str(attributes[14]),str(attributes[15]),str(attributes[8])))
                    else:
                        pass
                else:
                    frame_number_dict = {'Speed':int(attributes[14]),'Lane_ID':int(attributes[9]),'Traffic_Towards':attributes[10],'Frame_number':int(attributes[8]),'Quarantine_code':attributes[17]}
                    frame_number_dict_list.append(frame_number_dict)                
                    Primary_speed_ILOG.append(attributes[14])
                    frame_number_ILOG.append(attributes[8])
                    ILOG_LANE_ID.append(attributes[9])
                    ILOG_LANE_Direction.append(attributes[10])
                    Quarantine_code_ILOG.append(attributes[17])
                if(number_attribute_ILOG != 23):
                    print("XXXXXXXXXX-> Fail: Attribute count in ILOG is not the same : '{}.'".format(str(number_attribute_ILOG)))
                if(((attributes[16] == "P") or (attributes[16] == "F") or (attributes[15] != ''))):
                    if(attributes[17] == 'XX'):
                        print("XXXXXXXXXX-> Fail: SSV Corroboration incident is quarantined with '{}'.'{}'.".format(str(attributes[17]),str(attributes[8])))
                    else:
                        pass
                    SSV_Corroborated_speed.append(attributes[14])
                    print("SSV corroborated with PSMD and SSMD Speed : '{}'.'{}'.'{}'.".format(str(attributes[14]),str(attributes[15]),str(attributes[8])))                     
                if(attributes[17] == "TA"):
                   attributes_14 = int(attributes[14])
                   if((attributes_14 >= 70) and (attributes_14 <= 72)):
                       print("Automated Test Shot Passed with Speed : '{}'.'{}'.'{}'.".format(str(attributes_14),str(attributes[9]),str(int(attributes[8]))))
                   else:
                       print("XXXXXXXXXX-> Fail: Automated Test Shot Failed with Speed : '{}'. '{}'.".format(str(attributes_14),str(attributes[9]),str(int(attributes[8]))))
                   Ta_count_counter += 1                
                if(attributes[17] == "XX"):
                    Total_Count_XX += 1
                    if(int(attributes[14]) != 0):
                        print("XXXXXXXXXX-> Fail: Quarantine code XX speed verification failed : '{}'.'{}'.".format(str(attributes[14]),str(int(attributes[8]))))
                    else:                    
                        pass
                if(attributes[17]  == "MP"):
                    Total_Count_MP += 1
                    if(int(attributes[14]) !=0):
                        print("XXXXXXXXXX-> Fail: Quarantine code MP speed verification failed : '{}'.'{}'.".format(str(attributes[14]),str(int(attributes[8]))))
                    else:
                        pass
                if(attributes[17]  == "TS"):
                    Total_Count_TS += 1
                    if(int(attributes[14]) !=0):
                        print("XXXXXXXXXX-> Fail: Manual Test shot TS speed verification failed : '{}'.'{}'.".format(str(attributes[14]),str(int(attributes[8]))))
                    else:
                        pass                    
                if(attributes[17]  == "NV"):
                    Total_Count_NV += 1
                    if(int(attributes[14]) ==0):
                        print("XXXXXXXXXX-> Fail: Quarantine code NV speed verification failed : '{}'.'{}'.".format(str(attributes[14]),str(int(attributes[8]))))
                    else:
                        pass 
                if(attributes[9] != "0"):
                    if(attributes[9] == "1"):
                        if(attributes[17] == "NV"):
                            Total_Count_NV_Lane1 += 1
                            if(70 <= int(attributes[14]) <= 72):
                                NV_for_traffic_count1 += 1
                            else:
                                pass
                        elif(attributes[17] == "TA"):
                            Total_Count_TA_Lane1 += 1
                        elif(attributes[17] == "SC"):
                            Total_Count_SC_Lane1 += 1
                        else:
                            pass
                        Total_Count_Lane1 += 1
                    elif(attributes[9] == "2"):
                        if(attributes[17] == "NV"):
                            Total_Count_NV_Lane2 += 1
                            if(70 <= int(attributes[14]) <= 72):
                                NV_for_traffic_count2 += 1
                            else:
                                pass                            
                        elif(attributes[17] == "TA"):
                            Total_Count_TA_Lane2 += 1
                        elif(attributes[17] == "SC"):
                            Total_Count_SC_Lane2 += 1                        
                        else:
                            pass                
                        Total_Count_Lane2 += 1
                    elif(attributes[9] == "3"):
                        if(attributes[17] == "NV"):
                            Total_Count_NV_Lane3 += 1
                            if(70 <= int(attributes[14]) <= 72):
                                NV_for_traffic_count3 += 1
                            else:
                                pass                            
                        elif(attributes[17] == "TA"):
                            Total_Count_TA_Lane3 += 1
                        else:
                            pass                
                        Total_Count_Lane3 += 1
                    elif(attributes[9] == "4"):
                        if(attributes[17] == "NV"):
                            Total_Count_NV_Lane4 += 1
                            if(70 <= int(attributes[14]) <= 72):
                                NV_for_traffic_count4 += 1
                            else:
                                pass                            
                        elif(attributes[17] == "TA"):
                            Total_Count_TA_Lane4 += 1
                        else:
                            pass                
                        Total_Count_Lane4 += 1
                    elif(attributes[9] == "5"):
                        if(attributes[17] == "NV"):
                            Total_Count_NV_Lane5 += 1
                            if(70 <= int(attributes[14]) <= 72):
                                NV_for_traffic_count5 += 1
                            else:
                                pass                            
                        elif(attributes[17] == "TA"):
                            Total_Count_TA_Lane5 += 1
                        else:
                            pass                
                        Total_Count_Lane5 += 1
                    elif(attributes[9] == "6"):
                        if(attributes[17] == "NV"):
                            Total_Count_NV_Lane6 += 1
                            if(70 <= int(attributes[14]) <= 72):
                                NV_for_traffic_count6 += 1
                            else:
                                pass                            
                        elif(attributes[17] == "TA"):
                            Total_Count_TA_Lane6 += 1
                        else:
                            pass                
                        Total_Count_Lane6 += 1
                    else:
                        print("Lane ID not defined : '{}'.".format(str(attributes[9])))
            frame_number_dict_list = sorted(frame_number_dict_list, key = lambda i: i['Frame_number'])
            SSV_Corroborated_speed_InT = convert_string_integer_list(SSV_Corroborated_speed)
            frame_number_ILOG_int = convert_string_integer_list(frame_number_ILOG)
            TA_count = Total_Count_TA_Lane1 +Total_Count_TA_Lane2 +Total_Count_TA_Lane3 + Total_Count_TA_Lane4 + Total_Count_TA_Lane5 + Total_Count_TA_Lane6
            Primary_speed_ILOG_int = convert_string_integer_list(Primary_speed_ILOG)
            ILOG_LANE_ID_int = convert_string_integer_list(ILOG_LANE_ID)
            ILOG_Speed_Count_Lane1 = Total_Count_Lane1 - Total_Count_TA_Lane1 - Total_Count_NV_Lane1 - Total_Count_SC_Lane1
            ILOG_Speed_Count_Lane2 = Total_Count_Lane2 - Total_Count_TA_Lane2 - Total_Count_NV_Lane2 - Total_Count_SC_Lane2
            ILOG_Speed_Count_Lane3 = Total_Count_Lane3 - Total_Count_TA_Lane3 - Total_Count_NV_Lane3
            ILOG_Speed_Count_Lane4 = Total_Count_Lane4 - Total_Count_TA_Lane4 - Total_Count_NV_Lane4
            ILOG_Speed_Count_Lane5 = Total_Count_Lane5 - Total_Count_TA_Lane5 - Total_Count_NV_Lane5
            ILOG_Speed_Count_Lane6 = Total_Count_Lane6 - Total_Count_TA_Lane6 - Total_Count_NV_Lane6
            ILOG_Speed_Count_Lane = [ILOG_Speed_Count_Lane1,ILOG_Speed_Count_Lane2,ILOG_Speed_Count_Lane3,ILOG_Speed_Count_Lane4,ILOG_Speed_Count_Lane5,ILOG_Speed_Count_Lane6]
            ILOG_Quarantine_Count = [TA_count,Total_Count_XX,Total_Count_TS,Total_Count_NV,Total_Count_MP,ILOG_LANE_ID_int,ILOG_LANE_Direction,Ta_count_counter]
            NV_for_traffic_count = [NV_for_traffic_count1,NV_for_traffic_count2,NV_for_traffic_count3,NV_for_traffic_count4,NV_for_traffic_count5,NV_for_traffic_count6]
        Check_missing_frame_number(frame_number_ILOG_int,iamin)
        Check_duplicate_FrameNumber(frame_number_ILOG_int,iamin)
        return(len(frame_number_ILOG),SSV_Corroborated_speed_InT,Primary_speed_ILOG_int,Quarantine_code_ILOG,ILOG_Speed_Count_Lane,ILOG_Quarantine_Count,frame_number_dict_list,ILOG_empty_line,NV_for_traffic_count)

def SSLOG_Check(path,SSV_Corroborated_speed_ILOG,ILOG_LINE_missing):    
    with open (path) as SSLOG:
        SSLOG_empty_line = 0
        SSV_Corroborated_speed_SSLOG = []
        SSV_Corroborated_speed_SSLOG_InT = []
        for line in SSLOG.readlines():
            if line in ['\n','\r\n']:
                SSLOG_empty_line += 1
                print("XXXXXXXXXX-> Fail: The Empty line is found in : '{}'.".format(str(path)))
            else:
                pass            
            attributes = line.split(',')
            if(len(attributes) != 18):
                print("XXXXXXXXXX-> Fail: Attribute count is not the same for row in SS LOG : '{}'.".format(str(line)))
            else:
                if(attributes[13] == "V"):
                    SSV_Corroborated_speed_SSLOG.append(attributes[12])
                else:
                    pass
        SSV_Corroborated_speed_SSLOG_InT = convert_string_float_integer_list(SSV_Corroborated_speed_SSLOG)
        try:            
            if(ILOG_LINE_missing == 0):
                for i in range(len(SSV_Corroborated_speed_SSLOG_InT)):
                    if((SSV_Corroborated_speed_SSLOG_InT[i] - SSV_Corroborated_speed_ILOG[i]) > 2 or (SSV_Corroborated_speed_SSLOG_InT[i] - SSV_Corroborated_speed_ILOG[i]) < -2):
                        print("XXXXXXXXXX-> Fail: SSV Speed verification failed : '{}'.'{}'.".format(str(SSV_Corroborated_speed_SSLOG_InT[i]),str(SSV_Corroborated_speed_ILOG[i])))
                    else:
                        print("SSV Speed verification passed : '{}'.'{}'.".format(str(SSV_Corroborated_speed_SSLOG_InT[i]),str(SSV_Corroborated_speed_ILOG[i])))
            else:
                pass
        except IndexError:
            print("XXXXXXXXXX-> Fail: IndexError '{}'.'{}'.".format(str(len(SSV_Corroborated_speed_SSLOG_InT)),str(len(SSV_Corroborated_speed_ILOG))))

def PSLOG_Check(path,frame_number_ILOG_dict,ILOG_MissingLine):
    with open (path) as PSLOG:
        PSLOG_empty_line = 0
        frame_number_dict_PSLOG = {}
        Primary_speed_PS_Frame_number = []
        PSLOG_LANE_Direction = []
        frame_number_dict_list_PSLOG = []
        total_traffic_lane1 = []
        total_traffic_lane2 = []
        total_traffic_lane3 = []
        total_traffic_lane4 = []
        total_traffic_lane5 = []
        total_traffic_lane6 = []
        total_traffic_lane = []
        Primary_Speed_PS = []
        Primary_Speed_PS_int = []
        Primary_speed_PS_Frame_number_int = []
        PSLOG_LANE_ID_int = []
        PSLOG_LANE_ID = temp = []        
        iamin = 'PSLOG'
        if(ILOG_MissingLine == 0):
            for line in PSLOG.readlines():
                if line in ['\n','\r\n']:
                    PSLOG_empty_line += 1
                    print("XXXXXXXXXX-> Fail: The Empty line is found in : '{}'.".format(str(path)))
                else:
                    pass             
                attributes = line.split(',')
                number_attribute_PSLOG = len(attributes)
                if(attributes[7] == '2'):
                    temp.append(attributes[12])
                if(number_attribute_PSLOG != 20):
                    print("XXXXXXXXXX-> Fail: Attribute count in PSLOG is not the same : '{}.'".format(str(number_attribute_PSLOG)))                              
                if(((attributes[10] == "T") or (attributes[10] == "S")) and (attributes[10] != "")):                
                    Primary_Speed_PS.append(attributes[12])
                    Primary_speed_PS_Frame_number.append(attributes[16])
                    PSLOG_LANE_ID.append(attributes[7])
                    PSLOG_LANE_Direction.append(attributes[8])
                    frame_number_dict_PSLOG = {'Speed':int(float(attributes[12])),'Lane_ID':int(attributes[7]),'Traffic_Towards':attributes[8],'Frame_number':int(attributes[16]),'Quarantine_code':(attributes[10]),'Speed_verified_N_V':(attributes[13])}
                    frame_number_dict_list_PSLOG.append(frame_number_dict_PSLOG)                
                else:
                    pass
                if((attributes[10] == 'T') and (int(float(attributes[12])) != 0)):
                    if(70 <= int(float(attributes[12])) <= 72):
                        pass
                    else:
                        if(attributes[7] == '1'):
                            total_traffic_lane1.append(int(float(attributes[12])))
                        elif(attributes[7] == '2'):
                            total_traffic_lane2.append(int(float(attributes[12])))
                        elif(attributes[7] == '3'):
                            total_traffic_lane3.append(int(float(attributes[12])))                
                        elif(attributes[7] == '4'):
                            total_traffic_lane4.append(int(float(attributes[12])))
                        elif(attributes[7] == '5'):
                            total_traffic_lane5.append(int(float(attributes[12])))
                        elif(attributes[7] == '6'):
                            total_traffic_lane6.append(int(float(attributes[12])))                    
                        else:
                            pass
                else:
                    if(int(float(attributes[12])) != 0):                        
                        if(attributes[7] == '1'):
                            total_traffic_lane1.append(int(float(attributes[12])))
                        elif(attributes[7] == '2'):
                            total_traffic_lane2.append(int(float(attributes[12])))
                        elif(attributes[7] == '3'):
                            total_traffic_lane3.append(int(float(attributes[12])))                
                        elif(attributes[7] == '4'):
                            total_traffic_lane4.append(int(float(attributes[12])))
                        elif(attributes[7] == '5'):
                            total_traffic_lane5.append(int(float(attributes[12])))
                        elif(attributes[7] == '6'):
                            total_traffic_lane6.append(int(float(attributes[12])))                
                        else:
                            pass
                    else:
                        pass
            total_traffic_lane = [total_traffic_lane1,total_traffic_lane2,total_traffic_lane3,total_traffic_lane4,total_traffic_lane5,total_traffic_lane6]
            frame_number_dict_list_PSLOG = sorted(frame_number_dict_list_PSLOG, key = lambda i: i['Frame_number'])
            PSLOG_LANE_ID_int = convert_string_float_integer_list(PSLOG_LANE_ID)    
            Primary_Speed_PS_int = convert_string_float_integer_list(Primary_Speed_PS)
            Primary_speed_PS_Frame_number_int = convert_string_integer_list(Primary_speed_PS_Frame_number)
            Check_missing_frame_number(Primary_speed_PS_Frame_number_int,iamin)
            Check_duplicate_FrameNumber(Primary_speed_PS_Frame_number_int,iamin)
            if(len(frame_number_ILOG_dict) == len(frame_number_dict_list_PSLOG)):
                for i in range(len(frame_number_ILOG_dict)):
                    if(frame_number_ILOG_dict[i]['Speed'] != frame_number_dict_list_PSLOG[i]['Speed']):
                        if(frame_number_dict_list_PSLOG[i]['Speed_verified_N_V'] != 'N'):
                            print("XXXXXXXXXX-> Fail: ILOG and PSLOG speed is not same : '{}'.'{}'.'{}'.".format(str(frame_number_ILOG_dict[i]['Speed']),str(frame_number_dict_list_PSLOG[i]['Speed']),str(frame_number_dict_list_PSLOG[i]['Frame_number'])))
                        else:
                            pass
                    elif((frame_number_ILOG_dict[i]['Lane_ID'] != frame_number_dict_list_PSLOG[i]['Lane_ID']) and (frame_number_ILOG_dict[i]['Quarantine_code']) != 'TS'):
                        print("XXXXXXXXXX-> Fail: lane ID in ILOG and PS LOG is not the same : '{}'.'{}'.'{}'.".format(str(frame_number_ILOG_dict[i]['Lane_ID']),str(frame_number_dict_list_PSLOG[i]['Lane_ID']),str(frame_number_dict_list_PSLOG[i]['Frame_number'])))
                    elif(frame_number_ILOG_dict[i]['Traffic_Towards'] != frame_number_dict_list_PSLOG[i]['Traffic_Towards']):
                        print("XXXXXXXXXX-> Fail: Traffic Towards in ILOG and PS LOG is not the same : '{}'.'{}'.'{}'.".format(str(frame_number_ILOG_dict[i]['Traffic_Towards']),str(frame_number_dict_list_PSLOG[i]['Traffic_Towards']),str(frame_number_dict_list_PSLOG[i]['Frame_number'])))
                    elif((frame_number_dict_list_PSLOG[i]['Quarantine_code'] == 'T') and (frame_number_ILOG_dict[i]['Frame_number'] != frame_number_dict_list_PSLOG[i]['Frame_number'])):
                        print("The Automated Test Shot frame number is not same in ILOG and PSLOG : '{}'.'{}'.'{}'.'{}'.".format(str(frame_number_ILOG_dict[i]['Quarantine_code']),str(frame_number_dict_list_PSLOG[i]['Quarantine_code']),str(frame_number_ILOG_dict[i]['Frame_number']),str(frame_number_dict_list_PSLOG[i]['Frame_number'])))
                    else:
                        pass            
            else:
                print("XXXXXXXXXX-> Fail: Length of ILOG and PSLOG is not the same : '{}'.'{}'.".format(str(len(frame_number_ILOG_dict)),str(len(frame_number_dict_list_PSLOG))))
        return(Primary_Speed_PS_int,Primary_speed_PS_Frame_number_int,PSLOG_LANE_ID_int,PSLOG_LANE_Direction,PSLOG_empty_line,total_traffic_lane)

def TLOG_Check(path,ILOG_Speed_Count_lst,ILOGMIssing_line,total_traffic_lane_ps,NV_for_traffic_count_speed_70_72_ILOG):
    with open (path) as TLOG:
        total_Speed_Incidents_Detected_Lane1 = 0
        total_Speed_Incidents_Detected_Lane2 = 0
        total_Speed_Incidents_Detected_Lane3 = 0
        total_Speed_Incidents_Detected_Lane4 = 0
        total_Speed_Incidents_Detected_Lane5 = 0
        total_Speed_Incidents_Detected_Lane6 = 0
        total_traffice_lane1 = 0
        total_traffice_lane2 = 0
        total_traffice_lane3 = 0
        total_traffice_lane4 = 0
        total_traffice_lane5 = 0
        total_traffice_lane6 = 0
        TLOG_empty_line = 0
        valid_lane = 0
        total_traffice_lane_lst = []
        lane_id = []
        total_Speed_Incidents_Detected_Lane = []
        if(ILOGMIssing_line == 0):
            for line in TLOG.readlines():
                if line in ['\n','\r\n']:
                    TLOG_empty_line += 1
                    print("XXXXXXXXXX-> Fail: The Empty line is found in : '{}'.".format(str(path)))
                else:
                    pass             
                attributes = line.split(',')
                if(attributes[8] != "0"):
                    valid_lane += 1
                    lane_id.append(int(attributes[8]))
                    if(attributes[8] == "1"):
                        total_Speed_Incidents_Detected_Lane1 = int(attributes[12])
                        total_traffice_lane1 = (int(attributes[11]))
                    elif(attributes[8] == "2"):
                        total_Speed_Incidents_Detected_Lane2 = int(attributes[12])
                        total_traffice_lane2 = (int(attributes[11]))
                    elif(attributes[8] == "3"):
                        total_Speed_Incidents_Detected_Lane3 = int(attributes[12])
                        total_traffice_lane3 = (int(attributes[11]))
                    elif(attributes[8] == "4"):
                        total_Speed_Incidents_Detected_Lane4 = int(attributes[12])
                        total_traffice_lane4 = (int(attributes[11]))
                    elif(attributes[8] == "5"):
                        total_Speed_Incidents_Detected_Lane5 = int(attributes[12])
                        total_traffice_lane5 = (int(attributes[11]))
                    elif(attributes[8] == "6"):
                        total_Speed_Incidents_Detected_Lane6 = int(attributes[12])
                        total_traffice_lane6 = (int(attributes[11]))
                    else:
                        print("Lane id not available : '{}'.".format(str(attributes[12])))            
                else:
                    pass
            total_traffice_lane_lst = [total_traffice_lane1,total_traffice_lane2,total_traffice_lane3,total_traffice_lane4,total_traffice_lane5,total_traffice_lane6]
            total_Speed_Incidents_Detected_Lane = [total_Speed_Incidents_Detected_Lane1,total_Speed_Incidents_Detected_Lane2,total_Speed_Incidents_Detected_Lane3,total_Speed_Incidents_Detected_Lane4,total_Speed_Incidents_Detected_Lane5,total_Speed_Incidents_Detected_Lane6]
            for i in range(valid_lane):
                try:
                    if((len(total_traffic_lane_ps[i]) + NV_for_traffic_count_speed_70_72_ILOG[i]) != total_traffice_lane_lst[i]):
                        print("XXXXXXXXXX-> Fail: Total Traffic count is not same in PSLOG and TLOG for lane : '{}'.'{}'.'{}'.".format((str(lane_id[i])),str((len(total_traffic_lane_ps[i]) + NV_for_traffic_count_speed_70_72_ILOG[i])),str(total_traffice_lane_lst[i])))
                    else:
                        print("Total Traffic count is same in PSLOG and TLOG for lane : '{}'.'{}'.'{}'.".format((str(lane_id[i])),str((len(total_traffic_lane_ps[i]) + NV_for_traffic_count_speed_70_72_ILOG[i])),str(total_traffice_lane_lst[i])))
                    if(ILOG_Speed_Count_lst[i] == total_Speed_Incidents_Detected_Lane[i]):
                        print("The Total speed incidents detected in ILOG and TLOG are equal for Lane : '{}'.'{}'.'{}'.".format((str(lane_id[i])),str(ILOG_Speed_Count_lst[i]),str(total_Speed_Incidents_Detected_Lane[i])))
                    else:
                        print("XXXXXXXXXX-> Fail: The Total speed incidents detected in ILOG and TLOG are not equal for Lane : '{}'.'{}'.'{}'.".format((str(lane_id[i])),str(ILOG_Speed_Count_lst[i]),str(total_Speed_Incidents_Detected_Lane[i])))
                except Exception as e:
                    print("XXXXXXXXXX-> '{}'.".format(str(e)))

def OLOG_Read(path):
    with open (path) as OLOG:
        for line in OLOG.readlines():
            attributes = line.split(',')
            #print(len(attributes))
            #print(attributes)
            #if(attributes > 21):
            if(len(attributes) > 21):
                TSeries_Serial_Num = attributes[20]
                Vehicle_Reg_Num = attributes[25]
                CS_Version = attributes[18]
                SSV_Type = attributes[21]
                SSV_Code = attributes[22]
                Operator_ID = attributes[26]
                MDRSC_Technology_Type = attributes[5]
                Camera_Code = attributes[6]
                break
            else:
                pass  
        print("Vehicle Registration : '{}'.".format(str(Vehicle_Reg_Num)))
        print("CS Software Version : '{}'.".format(str(CS_Version)))
        print("PSMD Serial Number : '{}'.".format(str(TSeries_Serial_Num)))
        print("PSMD Device : '{}'.'{}'".format(str(MDRSC_Technology_Type),str(Camera_Code)))
        print("SSMD Device : '{}'.'{}'".format(str(SSV_Type),str(SSV_Code)))
        print("Operator_ID : '{}'.".format(str(Operator_ID)))
        
def convert_string_integer_list(str_list):
    return(list(map(int,str_list)))
    
def convert_string_float_integer_list(str_list):
    float_lst = list(map(float,str_list))
    return(list(map(int,float_lst)))
    
def Check_missing_frame_number(lst,whereis):
    lst_missing_frame = []
    try:
        lst_missing_frame = [x for x in range(lst[0], lst[-1]+1) 
                        if x not in lst]
    except IndexError:
        print("XXXXXXXXXX->IndexError->XXXXXXXXXX")
    if(len(lst_missing_frame) != 0):
        print("XXXXXXXXXX-> Fail: Missing Frame in : '{}'.'{}'.".format((str(whereis)),str(lst_missing_frame)))
    else:
        pass
    
def Check_duplicate_FrameNumber(lst,whereis):
    lst_duplicate_frame = []
    temp_lst = []
    try:
        for i in lst:
            if i not in temp_lst:
                temp_lst.append(i)
            else:
                lst_duplicate_frame.append(i)
    except IndexError:
        print("XXXXXXXXXX->IndexError->XXXXXXXXXX")
    if(len(lst_duplicate_frame) != 0):
        print("XXXXXXXXXX-> Fail: Duplicate Frame in : '{}'.'{}'.".format((str(whereis)),str(lst_duplicate_frame)))
    else:
        pass


def SCXML_apf_check(xmlpath):
    iamin = 'SC.xml'
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    xml_data = {}
    find_lst = ['Mode','SessionToQuarantine','SessionQuarantine','SessionEnd','SessionStart','FileCount','file']
    sessionfileslst = []
    apffileslst = []
    framenumscxml = []
    quarantinereasonslst = []
    testmode = root.find(find_lst[0]).text
    isSessionQuarantine = root.find(find_lst[1]).text
    SessionEnd = root.find(find_lst[3]).text
    SessionStart = root.find(find_lst[4]).text
    FileCount = int(root.find(find_lst[5]).text)
    filename = root.find('files')
    for sessionfiles in tree.findall('.//files//file'):
        sessionfileslst.append(sessionfiles.text)
        if(sessionfiles.text.endswith('.apf')):
            apffileslst.append(sessionfiles.text)
            framenumscxml.append(int(sessionfiles.text[24:29]))



    for quarantinereason in tree.findall('.//SessionQuarantine//SessionQuarantineReason'):
        quarantinereasonslst.append(quarantinereason.text)

    print("Session Mode : '{}'.".format(str(testmode)))
    print("IS Session Quarantine : '{}'.".format(str(isSessionQuarantine)))
    if(isSessionQuarantine == 'Y'):
        if(len(quarantinereasonslst) == 0):
            print("XXXXXXXXXX-> Fail: Session is Quarantine but NO QUARANTINE REASON : ")
        else:
            print("QUARANTINE REASON : '{}'.".format(str(quarantinereasonslst)))
    print("Session End Time : "+SessionEnd)
    print("Session Start Time : "+SessionStart)
    if(FileCount != len(sessionfileslst)):
        print("XXXXXXXXXX-> Fail: Filecount and Total listed files is not the same in SC.XML : '{}'.'{}'.".format(str(FileCount),str(len(sessionfileslst))))
    else:
        print("Filecount and Total listed files is the same in SC.XML : '{}'.'{}'.".format(str(FileCount),str(len(sessionfileslst))))
    print(quarantinereasonslst)
    framenumscxml.sort()
    #print(len(framenumscxml),len(apffileslst))
    #print(framenumscxml)
    apffileslst.sort()
    #print(apffileslst)
    Check_missing_frame_number(framenumscxml,iamin)
    Check_duplicate_FrameNumber(framenumscxml,iamin)
    return(framenumscxml)
    
    

def SCXML_apf_check_org(path):
    iamin = 'SC.xml'
    frame_number_apf_lst = []
    with open (path) as scxml:
        for line in scxml:
            if '.apf' in line:
                extension = ".apf"
                apf_name = line[-42:line.find(extension) + 4]
                frame_number_apf = apf_name[24:29]
                frame_number_apf_lst.append(int(frame_number_apf))
            if 'SessionToQuarantine' in line:
                print(line[2:])
                SessionToQuarantine = line[23:24]                
                if(SessionToQuarantine == "Y"):
                    print("XXXXXXXXXX-> Fail: Session is Quarantined")
                else:
                    print("Session is not Quarantined")
            if 'SessionQuarantineReason' in line:
                print(line[4:])
        frame_number_apf_lst.sort()
        Check_missing_frame_number(frame_number_apf_lst,iamin)
        Check_duplicate_FrameNumber(frame_number_apf_lst,iamin)
    return(frame_number_apf_lst)

def apf_check(apf_frame_lst,SCxmlpath):
    iamin = 'apf'
    Check_missing_frame_number(apf_frame_lst,iamin)
    Check_duplicate_FrameNumber(apf_frame_lst,iamin)
    try:
        print("APF file starting with : '{}'.".format(str(apf_frame_lst[0])))
        print("APF file ending with : '{}'.".format(str(apf_frame_lst[-1])))
        print("APF file in total : '{}'.".format(str(len(apf_frame_lst))))
    except IndexError:
        print("APF file not found")
    try:
        scxml_frame_lst = SCXML_apf_check(SCxmlpath)
        if(len(scxml_frame_lst) == len(apf_frame_lst)):
            for i in range(len(apf_lst)):
                if(apf_frame_lst[i] != scxml_frame_lst[i]):
                    print("XXXXXXXXXX-> Fail: apf frame number is not same in apf and scxml '{}'.'{}'.".format(str(apf_frame_lst[i]),str(scxml_frame_lst[i])))
                else:
                    pass
        else:
            print("XXXXXXXXXX-> Fail: apf frame number is not same in directory and in scxml '{}'.'{}'.".format(str(len(apf_frame_lst)),str(len(scxml_frame_lst))))
            apfindir = set(apf_frame_lst)
            apfinscxml = set(scxml_frame_lst)
            apfmissingdir = list(sorted(apfinscxml - apfindir))
            apfmissingscxml = list(sorted(apfindir - apfinscxml))
            if(len(apfmissingdir) != 0):
                print("XXXXXXXXXX-> Fail: APF Missing in directory : '{}'.".format(str(apfmissingdir)))
            if(len(apfmissingscxml) != 0):
                print("XXXXXXXXXX-> Fail: APF Missing in SCXML : '{}'.".format(str(apfmissingscxml)))
    except NameError:
        print("SC XML file not found")


def precisiontime_xml_check(path_xml_precisiontime):
    leng = 10
    regexp_hpt = re.compile("Hpt.{%d}" % leng)
    keyword_hpt = "<Hpt>"
    with open (path_xml_precisiontime) as prectime_xml:
        for line in prectime_xml:
            for m in regexp_hpt.findall(line):
                if(m == "THpt"):
                    pass
                elif(m == "RHpt"):
                    pass
                else:
                    print(m[3:16])
##            try:
##                 line = line.decode("utf-8")  # try to decode the contents to utf-8
##            except ValueError:# decoding failed, skip the line
##                 continue
##            if keyword_hpt in line:
##                print(line)
##            else:
##                pass
            

try:
    for folderName, subfolders, filenames in os.walk(Path_S):
        is_ILOG = 0
        is_SSLOG = 0
        is_PSLOG = 0
        is_TLOG = 0
        is_OLOG = 0
        is_apf = 0
        is_SCxml = 0
        is_precisiontime_xml = 0
        apf_lst = []
        for filename in filenames:
            if filename.endswith('.apf'):
                is_apf = 1
                apf_path = folderName
                frame_number = filename[24:29]
                apf_lst.append(int(frame_number))



            if filename.endswith('.mj2.xml'):
                is_precisiontime_xml = 1
                precisiontime_xml = folderName
                precisiontime_xml_path = os.path.join(folderName,filename)
##                print(is_precisiontime_xml)
##                print("is_precisiontime_xml : '{}'.".format(str(precisiontime_xml)))
##                print("is_precisiontime_xml : '{}'.".format(str(precisiontime_xml_path)))
##                if(is_precisiontime_xml == 1):
##                    precisiontime_xml_check(precisiontime_xml_path)


            
            if filename.endswith("I.log"):
                Log_Path = folderName
                print("*****************************************************************")
                print("Folder Path : '{}'.".format(str(Log_Path)))
                name = os.path.basename(Log_Path)
                execuition_count += 1
                for filename in os.listdir(Log_Path):
                    if filename.endswith("I.log"):
                        is_ILOG = 1
                        ILOG_name = filename[0:len(filename) - 5]
                        ILOG_Path = os.path.join(Log_Path,filename)
                        if(ILOG_name != name):
                            print("XXXXXXXXXX-> Fail: ILOG file naming is not correct : '{}'.'{}'.".format(str(ILOG_name),str(name)))
                    elif filename.endswith("SS.log"):
                        is_SSLOG = 1
                        SSLOG_name = filename[0:len(filename) - 6]
                        SSLOG_Path = os.path.join(Log_Path,filename)
                        if(SSLOG_name != name):
                            print("XXXXXXXXXX-> Fail: SSLOG file naming is not correct : '{}'.'{}'.".format(str(SSLOG_name),str(name)))
                    elif filename.endswith("PS.log"):
                        is_PSLOG = 1
                        PSLOG_name = filename[0:len(filename) - 6]
                        PSLOG_Path = os.path.join(Log_Path,filename)
                        if(PSLOG_name != name):
                            print("XXXXXXXXXX-> Fail: PSLOG file naming is not correct : '{}'.'{}'.".format(str(PSLOG_name),str(name)))
                    elif filename.endswith("T.log"):
                        is_TLOG = 1
                        TLOG_name = filename[0:len(filename) - 5]
                        TLOG_Path = os.path.join(Log_Path,filename)
                        if(TLOG_name != name):
                            print("XXXXXXXXXX-> Fail: TLOG file naming is not correct : '{}'.'{}'.".format(str(TLOG_name),str(name)))
                    elif filename.endswith("O.log"):
                        is_OLOG = 1
                        OLOG_name = filename[0:len(filename) - 5]
                        OLOG_Path = os.path.join(Log_Path,filename)
                        if(OLOG_name != name):
                            print("XXXXXXXXXX-> Fail: OLOG file naming is not correct : '{}'.'{}'.".format(str(OLOG_name),str(name)))                            
                    elif filename.endswith("S.log"):
                        is_SLOG = 1
                        SLOG_name = filename[0:len(filename) - 5]
                        SLOG_Path = os.path.join(Log_Path,filename)
                        if(SLOG_name != name):
                            print("XXXXXXXXXX-> Fail: SLOG file naming is not correct : '{}'.'{}'.".format(str(SLOG_name),str(name)))
                    elif filename.endswith("SC.xml"):
                        is_SCxml = 1
                        SCxml_name = filename[0:len(filename) - 6]
                        SCxml_Path = os.path.join(Log_Path,filename)
                        if(SCxml_name != name):
                            print("XXXXXXXXXX-> Fail: SC.xml file naming is not correct : '{}'.'{}'.".format(str(SCxml_name),str(name)))
                    else:
                        pass
                if((is_ILOG == 1) and (is_SSLOG == 1) and (is_PSLOG == 1) and (is_TLOG == 1) and (is_OLOG == 1)):              
                    length_frame_nubmer,SSV_Corroborated_speed_ILOG,Primary_speed_ILOG_int_ILOG,Quarantine_code,ILOG_Speed_Count_Lane_lst,ILOG_Quarantine_Count_all,frame_number_dict_list_ILOG,LINE_MISSING_ILOG,NV_for_traffic_count_speed_70_72 = ILOG_check(ILOG_Path)
                    SSLOG_Check(SSLOG_Path,SSV_Corroborated_speed_ILOG,LINE_MISSING_ILOG)
                    Primary_Speed_PS,Primary_speed_PS_Frame_number,PSLOG_LANE_ID,PSLOG_LANE_Direct,LINE_MISSING_PSLOG,total_traffic_lane_PS = PSLOG_Check(PSLOG_Path,frame_number_dict_list_ILOG,LINE_MISSING_ILOG)  
                    TLOG_Check(TLOG_Path,ILOG_Speed_Count_Lane_lst,LINE_MISSING_ILOG,total_traffic_lane_PS,NV_for_traffic_count_speed_70_72)  
                    OLOG_Read(OLOG_Path)
                    print("Total TA Automated Test Shot Count : '{}'.".format(str(ILOG_Quarantine_Count_all[7])))
                    print("Total TS Manual Test Shot Count : '{}'.".format(str(ILOG_Quarantine_Count_all[2])))
                    print("Total NV Quarantine Count : '{}'.".format(str(ILOG_Quarantine_Count_all[3])))
                    print("Total XX Quarantine Count : '{}'.".format(str(ILOG_Quarantine_Count_all[1])))
                    print("Total MP Quarantine Count : '{}'.".format(str(ILOG_Quarantine_Count_all[4])))
                else:
                    if(is_ILOG == 0):
                        print("XXXXXXXXXX-> Fail: ILOG is not available")
                    elif(is_SSLOG == 1):
                        print("XXXXXXXXXX-> Fail: SSLOG is not available")
                    elif(is_PSLOG == 1):
                        print("XXXXXXXXXX-> Fail: PSLOG is not available")
                    elif(is_TLOG == 1):
                        print("XXXXXXXXXX-> Fail: TLOG is not available")
                    elif(is_OLOG == 1):
                        print("XXXXXXXXXX-> Fail: OLOG is not available")
                    else:
                        print("XXXXXXXXXX-> Fail: LOGs are not available")
        End_time = datetime.datetime.now()
        if((is_apf == 1) and (is_SCxml == 1)):
            apf_lst.sort()
            apf_check(apf_lst,SCxml_Path)
        else:
            if((is_apf != 1) and (is_SCxml == 1)):                
                print("XXXXXXXXXX-> APF's missing")
            elif((is_apf == 1) and (is_SCxml != 1)):
                print("XXXXXXXXXX-> SC.xml is missing")
            else:
                pass
    Time_taken = End_time - start_time
    print("Time taken to execute : '{}'.".format(str(Time_taken)))
    print("Number of Sessions Executed : '{}'.".format(str(execuition_count)))
except WindowsError:
    End_time = datetime.datetime.now()
    Time_taken = End_time - start_time
    print("The system cannot find the path specified:'{}'.".format(str(Path_S)))
    print("Time taken to execute : '{}'.".format(str(Time_taken)))
    print("Number of Sessions Executed : '{}'.".format(str(execuition_count)))
print("*****************************************************************")
