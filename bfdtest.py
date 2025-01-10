data1 = '''<MPRPRRKMSAR01HNE40>display isis interface | exclude Tun|Lo
Info: It will take a long time if the content you search is too much or the string you input is too long, you can press CTRL_C to break.

                       Interface information for ISIS(6)
                       ---------------------------------
 Interface         Id      IPV4.State          IPV6.State      MTU  Type  DIS
 Eth1-Trunk1.2523  109             Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk25.2589  109         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --    
 Eth-Trunk26.2519  112         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk26.2621  116         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2645  126         Up          Mtu:Up/Lnk:Up/IP:Up 9189 L1/L2 --
 Eth-Trunk26.2828  130         Up          Mtu:Up/Lnk:Dn/IP:Dn 8997 L1/L2 --
 GigabitEthernet6/  455         Up          Mtu:Up/Lnk:Dn/IP:Dn 8997 L1/L2 -- 
 GigabitEthernet6/  455         Up          Mtu:Up/Lnk:Dn/IP:Dn 8997 L1/L2 -- 

                       Interface information for ISIS(100)
                       ---------------------------------
 Interface         Id      IPV4.State          IPV6.State      MTU  Type  DIS
 Eth-Trunk1.11     077         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk39       022         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2 --
 Eth-Trunk30       132         Up          Mtu:Up/Lnk:Dn/IP:Dn 9189 L1/L2
<MPRPRRKMSAR01HNE40>display bfd session all | i D_IP_IF
Info: It will take a long time if the content you search is too much or the string you input is too long, you can press CTRL_C to break.
(w): State in WTR
(*): State is invalid
--------------------------------------------------------------------------------
Local      Remote     PeerIpAddr      State     Type        InterfaceName 
--------------------------------------------------------------------------------
24316      19304      10.220.81.170   Up        D_IP_IF     Eth-Trunk1.2523
24317      17083      10.220.33.18    Up        D_IP_IF     Eth-Trunk1.11
24778      16576      10.17.122.88    Up        D_IP_IF     Eth-Trunk26.2828
26332      5          10.17.122.25    Up         addsd      Eth-Trunk30
--------------------------------------------------------------------------------
'''

'''def parse_isis_data(data):
    isis_interfaces = {}
    lines = data.splitlines()
    isis_section = False
    for line in lines:
        if "Interface information for ISIS" in line:
            isis_section = True
            continue
        if isis_section:
            if "Interface" in line and "Id" in line:
                continue
            parts = line.split()
            if len(parts) > 2:
                interface = parts[0]
                state = parts[2]
                isis_interfaces[interface] = state
    print("interfaces dict =",isis_interfaces)
    return isis_interfaces

def parse_bfd_data(data):
    bfd_interfaces = {}
    lines = data.splitlines()
    bfd_section = False
    for line in lines:
        if "Local" in line and "Remote" in line:
            bfd_section = True
            continue
        if bfd_section:
            parts = line.split()
            if len(parts) > 5:
                interface = parts[5]
                state = parts[3]
                bfd_interfaces[interface] = state
    print("interfaces dict =",bfd_interfaces)

    return bfd_interfaces

def compare_interfaces(isis_data, bfd_data):
    # Check each interface in the BFD data
    for interface in bfd_data:
        print("interfaces==",interface)
        # If the interface is also present in the ISIS data
        if interface in isis_data:
            # Check if the state is not 'Up' in either ISIS or BFD data
            if isis_data[interface] != "Up" or bfd_data[interface] != "Up":
                return "NA"
        else:
            # If the interface is in BFD but not in ISIS, return 'NA'
            return "NA"
    return "ok"

isis_data = parse_isis_data(data1)
bfd_data = parse_bfd_data(data1)
result = compare_interfaces(isis_data, bfd_data)
print(result)'''


import re
'''def parse_isis_data(data):
    isis_interfaces = {}
    # Use regular expression to find all matches for interface and its IPv4 state
    pattern = re.compile(r'^\s*(\S+)\s+\d+\s+(\S+)', re.MULTILINE)
    matches = pattern.findall(data)
    for match in matches:
        interface, state = match
        isis_interfaces[interface] = state
    print("interfaces dict =",isis_interfaces)

    return isis_interfaces

def parse_bfd_data(data):
    bfd_interfaces = {}
    # Use regular expression to find all matches for interface and its state
    pattern = re.compile(r'^\d+\s+\d+\s+\S+\s+(\S+)\s+\S+\s+(\S+)', re.MULTILINE)
    matches = pattern.findall(data)
    for match in matches:
        state, interface = match
        bfd_interfaces[interface] = state
    return bfd_interfaces

def compare_interfaces(isis_data, bfd_data):
    # Check each interface in the BFD data
    for interface in bfd_data:
        # If the interface is also present in the ISIS data
        if interface in isis_data:
            # Check if the state is not 'Up' in either ISIS or BFD data
            if isis_data[interface] != "Up" or bfd_data[interface] != "Up":
                return "NA"
        else:
            # If the interface is in BFD but not in ISIS, return 'NA'
            return "NA"
    return "ok"

isis_data = parse_isis_data(data1)
bfd_data = parse_bfd_data(data1)
result = compare_interfaces(isis_data, bfd_data)
print(result)'''
import re
def parse_isis_data(data):
    isis_interfaces = {}
    lines = data.splitlines()
    start_idx = None
    end_idx = None

    # Find start and end indices of ISIS section
    for idx, line in enumerate(lines):
        if "Interface information for ISIS" in line:
            start_idx = idx + 2  # Skip header lines
        if start_idx is not None and idx > start_idx and not line.strip():
            end_idx = idx
            break

    if start_idx is not None and end_idx is not None:
        # Extract interface and state using regex
        pattern = re.compile(r'^\s*(\S+)\s+\S+\s+(\S+)', re.MULTILINE)
        for line in lines[start_idx:end_idx]:
            match = pattern.search(line)
            if match:
                interface = match.group(1)
                state = match.group(2)
                isis_interfaces[interface] = state

    return isis_interfaces

def parse_bfd_data(data):
    bfd_interfaces = {}
    lines = data.splitlines()

    # Find start index of BFD section
    for idx, line in enumerate(lines):
        if "InterfaceName" in line:
            start_idx = idx + 2  # Skip header lines
            break

    if start_idx is not None:
        # Extract interface and state using regex
        pattern = re.compile(r'^\d+\s+\d+\s+\S+\s+(\S+)\s+\S+\s+(\S+)', re.MULTILINE)
        for line in lines[start_idx:]:
            match = pattern.search(line)
            if match:
                state = match.group(1)
                interface = match.group(2)
                bfd_interfaces[interface] = state

    return bfd_interfaces

def compare_interfaces(isis_data, bfd_data):
    matching_interfaces = {}

    # Iterate through ISIS interfaces
    for isis_interface, isis_state in isis_data.items():
        # Check if ISIS interface exists in BFD data
        if isis_interface in bfd_data:
            bfd_state = bfd_data[isis_interface]  # Get BFD state for matching interface
            matching_interfaces[isis_interface] = {
                'ISIS_State': isis_state,
                'BFD_State': bfd_state
            }

    return matching_interfaces

isis_data = parse_isis_data(data1)
bfd_data = parse_bfd_data(data1)
matching_interfaces = compare_interfaces(isis_data, bfd_data)

# Print matching interfaces and their states
print("Matching Interfaces and Their States:",matching_interfaces)
for interface, states in matching_interfaces.items():
    print(f"Interface: {interface}, ISIS State: {states['ISIS_State']}, BFD State: {states['BFD_State']}")