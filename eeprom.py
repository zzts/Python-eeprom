#eprom I2c access
# code to access  24c32, 24c64 and 24128 eproms from rasberry pi
# these eproms use a writestrobe which need to be held low while writing


from smbus import SMBus
import RPi.GPIO as rGPIO  # if you try to import RPi.GPIO you get an error message
import time


slaveaddr= 0x50 # for the RASPio Pro Hat

# for the RASPio Pro hat the eeprom is on the i2c-0 bus
# you must enable the i2c-0 bus by adding dtparam=i2c_vc to /boot/config.txt

smb = SMBus(0) # set bus

writestrobe = 26 # hold pin low to write to eeprom

# set up gpio for write strobe
rGPIO.setmode(rGPIO.BCM)
rGPIO.setup(writestrobe, rGPIO.OUT)



def eeprom_set_addr(addr) :
    smb.write_byte_data(slaveaddr, addr//256, addr%256)

def eeprom_read_byte(addr) :
    eeprom_set_addr(addr)
    return smb.read_byte(slaveaddr)

def eeprom_read_next_byte() :
    return smb.read_byte(slaveaddr)

# according to data sheet you can write upto 32 bytes if starting on page boundry
def eeprom_write_block(addr, data) :
    data.insert(0, addr%256)

    try:
        rGPIO.output(writestrobe, rGPIO.LOW)  # enable write
        smb.write_i2c_block_data(slaveaddr, addr//256, data)
        rGPIO.output(writestrobe, rGPIO.HIGH)
    finally:
        time.sleep(0.015) # data sheet says 10 msec max

def eeprom_write_byte(addr, byte) :
    data = [addr%256,byte]
    
    try:
        rGPIO.output(writestrobe, rGPIO.LOW)  # enable write
        smb.write_i2c_block_data(slaveaddr, addr//256, data)
        rGPIO.output(writestrobe, rGPIO.HIGH)
    finally:
        time.sleep(0.015) # data sheet says 10 msec max

if __name__ == '__main__' :
    
    eeprom_set_addr(1024)
    
    for i in range(9):
        print( i+1024, eeprom_read_next_byte())

    eeprom_write_block(1024, [1,2,3,4,5,6,7,8,9])

    for i in range(9):
        print( i+1024, eeprom_read_byte(i+1024))

    for i in range(9):
        eeprom_write_byte(i+1024, 9-i)

    eeprom_set_addr(1024)    

    for i in range(9):
        print( i+1024, eeprom_read_next_byte())
