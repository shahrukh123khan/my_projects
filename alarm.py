data1='''<MPRPRRKMSAR01HNE40>display alarm all
--------------------------------------------------------------------------------
Index  Level    Date       Time           Info                                  
--------------------------------------------------------------------------------
1      Critical 2023-06-29 13:33:42+05:30 GigabitEthernet3/0/23 is failed, the o
                                          ptical module's state on card is chang
                                          ed[OID:1.3.6.1.4.1.2011.5.25.129.2.1.1
                                          ,BasCode:65541]                       
2      Critical 2021-04-06 15:28:45+05:30 GigabitEthernet3/0/19 is failed, the o
                                          ptical module's state on card is chang
                                          ed[OID:1.3.6.1.4.1.2011.5.25.129.2.1.1
                                          ,BasCode:65541]                       
--------------------------------------------------------------------------------
1      Critical 2023-08-31 12:09:06+05:30 Slot 3 is failed, The board was powere
                                          d off[OID:1.3.6.1.4.1.2011.5.25.219.2.
                                          2.5,EntCode:132626]
2      Critical 2018-05-04 17:01:39+05:30 GigabitEthernet8/0/11 is failed, the o
                                          ptical module's state on card is chang
                                          ed[OID:1.3.6.1.4.1.2011.5.25.219.2.4.1
                                          ,EntCode:135680]
3      Critical 2018-01-25 17:29:25+05:30 The air filter inside the chassis was
                                          not cleaned.[OID:1.3.6.1.4.1.2011.5.25
                                          .219.2.1.3,EntCode:131328]
--------------------------------------------------------------------------------'''

data2='''<APHYDUPPIAR02HNE9K>display alarm active 
1:Critical  2:Major  3:Minor  4:Warning
--------------------------------------------------------------------------------
Sequence   AlarmId    Level Date Time  Description                              
--------------------------------------------------------------------------------
965368     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1055
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.96.227, TunnelName=T
                                       unnel1055, SignalledTunnelName=HYDUPLIAG0
                                       3_VRNCNTIAG02)                           
965367     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1054
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.96.226, TunnelName=T
                                       unnel1054, SignalledTunnelName=HYDUPLIAG0
                                       3_VRNCNTIAG01)                           
965366     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1051
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.99.20, TunnelName=Tu
                                       nnel1051, SignalledTunnelName=HYDUPLIAG03
                                       _ASNRAMIAG02)                            
965365     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1050
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.99.19, TunnelName=Tu
                                       nnel1050, SignalledTunnelName=HYDUPLIAG03
                                       _ASNRAMIAG01)                            
965360     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1042
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.97.114, TunnelName=T
                                       unnel1042, SignalledTunnelName=HYDUPLIAG0
                                       3_GWTAMBIAG02)                           
965358     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1041
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.97.113, TunnelName=T
                                       unnel1041, SignalledTunnelName=HYDUPLIAG0
                                       3_GWTAMBIAG01)                           
965356     0xF101BB   2     2023-12-03 Traffic switched from the primary LSP to 
                             12:25:17+ the hot-standby LSP.(SessionTunnelId=1037
                            05:30      , LocalLspId=0, IngressLsrId=182.19.99.98
                                       , EgressLsrId=182.19.97.195, TunnelName=T
                                       unnel1037, SignalledTunnelName=HYDUPLIAG0
                                       3_AGRFRDIAG02)  '''

data3='''<MHPUNVEGPSS04>display alarm all
----------------------------------------------------------------------------
 NO alarm
----------------------------------------------------------------------------
'''

data4='''<MUMUMAIRSBS01>display alarm active
A/B/C/D/E/F/G/H/I/J
A=Sequence, B=RootKindFlag(Independent|RootCause|nonRootCause)
C=Generating time, D=Clearing time
E=ID, F=Name, G=Level, H=State
I=Description information for locating(Para info, Reason info)
J=RootCause alarm sequence(Only for nonRootCause alarm)

  1/Independent/2018-10-11 00:39:21+05:30/-/0x418c2002/hwGtlDefaultValue/Major/Start/OID 1.3.6.1.4.1.2011.5.25.142.2.1 Current license value is default, the reason is No license available.
  4621/Independent/2021-03-05 00:19:14+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 17 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=XGigabitEthernet0/0/12)
  4622/Independent/2021-03-05 00:19:14+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 55 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=Vlanif607)
  4623/Independent/2021-03-05 00:19:14+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 62 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=Vlanif633)
  4624/Independent/2021-03-05 00:19:14+05:30/-/0x40e62000/ipv6IfStateChange/Major/Start/OID 1.3.6.1.2.1.55.2.0.1 The status of the IPv6 Interface changed. (IfIndex=56, IfDescr=To_MUM_SBC_SIGN, IfOperStatus=2, IfAdminStatus=1)
  4625/Independent/2021-03-05 00:19:14+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 19 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=XGigabitEthernet0/0/14)
  4626/Independent/2021-03-05 00:19:14+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 60 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=Vlanif621)
  4627/Independent/2021-03-05 00:19:15+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 16 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=XGigabitEthernet0/0/11)
  4628/Independent/2021-03-05 00:19:16+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 18 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=XGigabitEthernet0/0/13)
  4629/Independent/2021-03-05 00:19:16+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 59 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=Vlanif619)
  4630/Independent/2021-03-05 00:19:16+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 20 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=XGigabitEthernet0/0/15)
  4631/Independent/2021-03-05 00:19:16+05:30/-/0x502001/linkDown/Critical/Start/OID 1.3.6.1.6.3.1.1.5.3 Interface 64 turned into DOWN state.(AdminStatus=1,OperStatus=2,InterfaceName=Vlanif645)'''


["optical", "bfd", "gigabitethernet", "interface", "linkdown", "ipv6ifstatechange", "link", "optical", "bfd", "gigabitethernet", "traffic switched from the primary lsp", "the member of lag negotiation failed", "link bandwidth lost totally", "trunkind", "the interface status changes", "interface 64 turned into down state", "the status of the ipv6 interface changed praramter alarms"]


import re 
import pandas as pd 
pattern = re.compile(r'(\d+)\s+(Critical|Major|Minor|Warning)\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}\+\d{2}:\d{2})\s+([\s\S]*?)(?:\[OID:|\n-{80})')
matches = pattern.findall(data1)
pd.set_option('max_colwidth', None)
df = pd.DataFrame(matches, columns=['Index', 'Level', 'Date', 'Time', 'Info'])

#df['Info'] = df['Info'].str.replace(r'\s+', ' ')
df['Info'] = df['Info'].apply(lambda x: f'"{x}"')
df.to_csv('data.csv', index=True)
pd.reset_option('max_colwidth')


