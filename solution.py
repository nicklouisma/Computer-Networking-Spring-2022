from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2
    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    myID = os.getpid() & 0xFFFF
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = []
    tracelist2 = []
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("d \t *\t *\t *\t Request timed out.")
                    tracelist1.append("d \t *\t *\t *\t Request timed out.")
                    tracelist2.append(tracelist1)
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("d \t *\t *\t *\t Request timed out.")
                    tracelist1.append("d \t *\t *\t *\t Request timed out.")
                    tracelist2.append(tracelist1)
            except timeout:
                continue
            else:
                icmpHeader = recvPacket[20:28]
                request_type, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
                try:
                    hostName = gethostbyaddr(addr[0])[0]
                except herror as msg: 
                    hostName = str(msg)
                if request_type == 11:
                    bytes = struct.calcsize("d")
                    print("%d\t rtt = %.00f ms\t %s\t %s" % (ttl, (timeReceived - t) * 1000, addr[0], hostName))
                    tracelist1.append(str(ttl))
                    tracelist1.append(str(addr[0]))
                    tracelist1.append(str(hostName))
                    tracelist2.append(tracelist1)
                elif request_type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("%d\t rtt = %.00f ms\t %s\t %s" % (ttl, (timeReceived - t) * 1000, addr[0], hostName))
                    tracelist1.append(str(ttl))
                    tracelist1.append(str(addr[0]))
                    tracelist1.append(str(hostName))
                    tracelist2.append(tracelist1)
                elif request_type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("%d\t rtt=%.00f ms\t %s\t %s" % (ttl, (timeReceived - t) * 1000, addr[0], hostName))
                    tracelist1.append(str(ttl))
                    tracelist1.append(str(addr[0]))
                    tracelist1.append(str(hostName))
                    tracelist2.append(tracelist1)
                    return tracelist2
                else:
                    print("error")
                break
            finally:
                mySocket.close()

if __name__ == '__main__':
    get_route("google.co.il")
