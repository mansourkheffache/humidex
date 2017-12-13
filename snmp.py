from easysnmp import Session

switch_ip = '10.10.10.1'
pdu_ip = '10.10.10.151'

# QUERIES THE PDU FOR POWER ON ALL OUTLETS (8)
# RETURNS A SUM OF ACTUAL POWER FOR ALL OUTLETS IN WATTS
def get_power():
    session = Session(hostname=pdu_ip, community='perccom', version=2)
    sum = 0
    for i in range(1,9):
        snmp_response = session.get('1.3.6.1.4.1.13742.6.5.4.3.1.4.1.' + str(i) + ".5")
        sum += int(snmp_response.value)
    return sum


# QUERY THE SWITCH (10.10.10.1) FOR IN AND OUT BYTES
# RETURNS SUM FOR ALL PORTS (IN AND OUT DIRECTION)
def get_traffic():
    session = Session(hostname=switch_ip, community='perccom', version=2)
    # variable to hold SNMP return values
    inOctets = 0
    outOctets = 0
    #  Loop to get the necessary SNMP-GET queries
    for i in range(1,25):
        if i < 10:
            bytes_in = session.get('1.3.6.1.2.1.2.2.1.10.1010' + str(i))
            bytes_out = session.get('1.3.6.1.2.1.2.2.1.16.1010' + str(i))
        else:
            bytes_in = session.get('1.3.6.1.2.1.2.2.1.10.101' + str(i))
            bytes_out = session.get('1.3.6.1.2.1.2.2.1.16.101' + str(i))
        inOctets += int(bytes_in.value)
        outOctets += int(bytes_out.value)
    # RETURN IN + OUT BYTES
    return inOctets + outOctets
