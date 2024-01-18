import os
import time
import subprocess
import signal

macaddress = "60:b4:f7:b3:07:b6"
macaddfilter ="07:b6"
#01-04 17:29:41.914  2637  2796 D bt_btif_config: btif_get_address_type: Device [60:b4:f7:b3:07:b6] address type 0

# adb logcat | FIND /I "apk" 

cmd = 'adb logcat | FIND /I "'+str(macaddress)+'"' 
process=os.popen(cmd)
A = process.readline()
print(A)
#preprocessed = process.read()
#process.close()
#print(preprocessed)
#process = subprocess.Popen(cmd)  # pass cmd and args to the function

time.sleep(3)	
#stdout, stderr = process.communicate()  # get command output and error
#RESULT=str(stdout)
#print(RESULT)

#subprocess.Popen.kill(process)
if "BluetoothActiveDeviceManager: handleMessage(MESSAGE_DEVICE_ACL_DISCONNECTED): device" in A: 
    
    if "macaddfilter" in A:
         print("ZENO is number 1")

#command = os.popen(cmd)
#result = command.read()

#cmd = 'adb logcat'
#command = os.popen(cmd)
#result = command.read()
#print(result)
