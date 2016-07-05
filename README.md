# Python-eeprom
Python wrapper for smbus/i2c library to read m24c32,64 and m24128 eeproms

Requires smbus and RPi.GPIO

If you are accessing the eeprom on a Hat, they are usually accessed on i2c-0 for RPi 2 and 3s.  You must add dtparam=i2c_vc to the
/boot/config.txt to enable it.

I have only tested this on a RASPio Pro Hat with an m24c32 chip.

This is a class based implementation

Base Class eeprom(bus #, slave address, write_strobe pin)
functions:  set_addr(mem addr) # sets mem address register for subsequent reads
            read_next_byte () # returns byte at current memory then increments register
            read_byte (mem addr) # sets register, reads byte and increments register
            write_byte (mem addr, byte) # writes single byte to mem addr
            write_block (mem addr, [data block]) # writes a list up to 32 bytes to mem address

