# The DS28E38 is an ECDSA public-key-based secure authenticator.
import time
import machine
import binascii
import os
import json
import onewire

cmd_start = 0x66
cmd_signMessage_len = 34
cmd_read_page = 0xa5
cmd_readPage_len = 2
cmd_read_mem = 0x44
cmd_parameter = 0b00000000

class DS28E38:  
    #constructor to initialize some variables
    def __init__(self, onewire):
        self.counter = 0
        dat = machine.Pin(14)
        self.ow = onewire.OneWire(dat)
        self.ow.pin.init(self.ow.pin.OPEN_DRAIN, None)
        self.crc16 = bytearray(2)
        self.roms = []
    
    #CRC_16 function to check the validity of the data transmitted and received
    def onewire_crc16(self,input,crc=0):
        oddparity = [False, True, True, False, True, False, False, True, True, False, False, True, False, True, True, False]
        for cdata in input:
            cdata = (cdata ^ crc) & 0xff
            crc = crc >> 8
            if (oddparity[cdata & 0x0F] == oddparity[cdata >> 4]):
                crc = crc ^ 0xC001  
            cdata = cdata << 6
            crc = crc ^ cdata
            cdata = cdata << 1
            crc = crc ^ cdata
        return crc

  
    # Read status	of the chip
    def read_status(self):
        self.ow.reset()
        self.ow.writebyte(self.ow.SKIP_ROM)
        self.ow.write(b'\x66\x02')
        self.ow.write(b'\xaa\x00')
        self.ow.readinto(self.crc16)
        self.ow.write(b'\xaa') #release byte
        time.sleep_ms(120)	
	
    #get the ROM and the man id of the chip.
    def read_man_rom_Id(self):
        self.ow.readbyte() # dummy
        self.ow.readbyte() # length
        self.ow.readbyte() # result
        rx_read_protection_values = bytearray(12)
        self.ow.readinto(rx_read_protection_values)
        self.crc16 = bytearray(2)
        self.ow.readinto(self.crc16)
        self.roms = self.ow.scan()
        device_data = {}
        self.ow.select_rom(self.roms[0])
        data = {}
        data['manId'] = binascii.hexlify(rx_read_protection_values[7:9])
        data['romId'] = binascii.hexlify(self.roms[0])
        device_data = json.dumps(data)      
        return device_data
    
    #get the digital signature after signing the message.
    def sign_message(self,challenge):
        signature = {}
        self.ow.writebyte(cmd_start)
        self.ow.writebyte(cmd_signMessage_len)
        self.ow.writebyte(cmd_read_page)
        self.ow.writebyte(cmd_parameter)
        self.ow.write(challenge)
        self.ow.readinto(self.crc16)
        signature['crc-16'] = binascii.hexlify(self.crc16)
        self.ow.write(b'\xaa') #release byte
        time.sleep_ms(410)
        self.ow.readbyte() #dummy
        self.ow.readbyte() #rx_result_length
        self.ow.readbyte() #rx_result_byte
        rx_result = bytearray(64)
        self.ow.readinto(rx_result)
        self.ow.readinto(self.crc16)
        signature['r'] = binascii.hexlify(rx_result[32:64])
        signature['s'] = binascii.hexlify(rx_result[0:32])
        signature_data = json.dumps(signature)
        return signature_data
  
    #get the pagedata, publickey(x,y). page number 0 is the pagedata, page number 4 is the x component of the publickey, page number 5 is the y component of the publickey.
    def read_page(self,page_num):
        self.ow.select_rom(self.roms[0])
        self.ow.writebyte(cmd_start)
        self.ow.writebyte(cmd_readPage_len)
        self.ow.writebyte(cmd_read_mem)
        self.ow.writebyte(page_num)
        self.crc16 = bytearray(2)
        self.ow.readinto(self.crc16)
        self.ow.write(b'\xaa') #release byte
        time.sleep_ms(410)
        self.ow.readbyte() #rx_dummy
        self.ow.readbyte() #rx_result_length
        self.ow.readbyte() #rx_result_byte
        rx_result = bytearray(32)
        self.ow.readinto(rx_result)
        self.ow.readinto(self.crc16)
        return rx_result
  




















































