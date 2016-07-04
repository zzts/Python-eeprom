# Python-eeprom
Python wrapper for smbus/i2c library to read m24c32,64 and m24128 eeproms

Requires smbus and RPi.GPIO

If you are accessing the eeprom on a Hat, they are usually accessed on i2c-0 for RPi 2 and 3s.  You must add dtparam=i2c_vc to the
/boot/config.txt to enable it.

I have only test this on a RASPio Pro Hat with an m24c32 chip.
