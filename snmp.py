from easysnmp import Session
import time
from datetime import datetime


# QUERIES THE PDU FOR POWER ON ALL OUTLETS (8)
# RETURNS A SUM OF ACTUAL POWER FOR ALL OUTLETS IN WATTS
def getPower():
    session = Session(hostname="10.10.10.151", community='perccom', version=2)
    energy_sum = 0
    for i in range(1,9):
        system_items = session.walk('1.3.6.1.4.1.13742.6.5.4.3.1.4.1.' + str(i))
        counter = 1
        for item in system_items:
            if counter == 3:
                energy_sum += int(item.value)
            counter += 1
    return energy_sum


# QUERY THE SWITCH (10.10.10.1) FOR IN AND OUT BYTES
# RETURNS SUM FOR ALL PORTS (IN AND OUT DIRECTION)
def getBytes(ip):
    session = Session(hostname=ip, community='perccom', version=2)
    # IN OCTETS
    system_items = session.walk('1.3.6.1.2.1.2.2.1.10')
    inOctets = 0
    i = 0
    for item in system_items:
        if i is not  0:
            inOctets += int(item.value)
        i+=1
    # OUT OCTETS
    system_items = session.walk('1.3.6.1.2.1.2.2.1.16')
    outOctets = 0
    j = 0
    for item in system_items:
        if j is not  0:
            outOctets += int(item.value)
        j+=1
    # RETURN THE SUM
    return inOctets + outOctets


# ONLY FOR SOME PRINTING AND DEBUGGING S***T
def main():
    prevBytes = 0
    while True:
        time.sleep(1)
        print "Current Bytes: [" + str(getBytes("10.10.10.1")) + "] ... Current Power: [" + str(getPower()) + "]"
    #     time.sleep(1)
    #     currentBytes = getBytes("10.10.10.1")
    #     if prevBytes == 0:
    #         print str(datetime.now()) + " : "+ str(currentBytes) + "(diff: N/A) ---- CURRENT POWER: " + str(getPower())
    #     else:
    #         print str(datetime.now()) + " : "+ str(currentBytes) + "(diff:" + str(currentBytes-prevBytes) +") ---- CURRENT POWER:" + str(getPower())
    #     prevBytes = currentBytes


if  __name__ =='__main__':
    main()
