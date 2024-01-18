import uiautomator2 as u2

d = u2.connect('R5CT50K7ENH') # alias for u2.connect_usb('123456f')
print(d.info)