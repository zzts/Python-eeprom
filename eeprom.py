#eprom I2c access
# code to access  24c32, 24c64 and 24128 eproms from raspberry pi
# these eproms use a writestrobe which need to be held low while writing


from smbus import SMBus
import RPi.GPIO as rGPIO  # if you try to import RPi.GPIO you get an error message
import time

class eeprom() :
    """Code to access  24c32, 24c64 and 24128 eproms from raspberry pi
These eproms use a writestrobe which need to be held low while writing"""
    def __init__(self, bus=0, slaveaddr = 0x50, write_str_pin=26):
        """slaveaddr= 0x50 for the RASPio Pro Hat
        for the RASPio Pro hat the eeprom is on the i2c-0 bus
        you must enable the i2c-0 bus by adding dtparam=i2c_vc to /boot/config.txt"""

        self.smb = SMBus(bus) # set bus
        self.saddr = slaveaddr
        self.writestrobe = write_str_pin # hold pin low to write to eeprom
        
        # set up gpio for write strobe
        rGPIO.setmode(rGPIO.BCM)
        rGPIO.setup(self.writestrobe, rGPIO.OUT)

    def set_addr(self, addr) :
        self.smb.write_byte_data(self.saddr, addr//256, addr%256)

    def read_byte(self,addr) :
        self.set_addr(addr)
        return self.smb.read_byte(self.saddr)

    def read_next_byte(self) :
        return self.smb.read_byte(self.saddr)

    # according to data sheet you can write upto 32 bytes if starting on page boundry
    def write_block(self, addr, data) :
        data.insert(0, addr%256)

        try:
            rGPIO.output(self.writestrobe, rGPIO.LOW)  # enable write
            self.smb.write_i2c_block_data(self.saddr, addr//256, data)
            rGPIO.output(self.writestrobe, rGPIO.HIGH)
        finally:
            time.sleep(0.015) # data sheet says 10 msec max

    def write_byte(self, addr, byte) :
        data = [addr%256,byte]
        
        try:
            rGPIO.output(self.writestrobe, rGPIO.LOW)  # enable write
            self.smb.write_i2c_block_data(self.saddr, addr//256, data)
            rGPIO.output(self.writestrobe, rGPIO.HIGH)
        finally:
            time.sleep(0.015) # data sheet says 10 msec max

if __name__ == '__main__' :

    eep=eeprom()  #use defaults
    
    eep.set_addr(1024)
    
    for i in range(9):
        print( i+1024, eep.read_next_byte())

    eep.write_block(1024, [1,2,3,4,5,6,7,8,9])

    for i in range(9):
        print( i+1024, eep.read_byte(i+1024))

    for i in range(9):
        eep.write_byte(i+1024, 9-i)

    eep.set_addr(1024)    

    for i in range(9):
        print( i+1024, eep.read_next_byte())
