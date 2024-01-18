"""
example

"""
import time
import platform
import ble_adv_event_scanner as BleScanAdvEvents
import parser_ring_info as ParserRingInfo
import datetime

bleScan = BleScanAdvEvents.BLE_AdvEventScan()
ringInfo = ParserRingInfo.PARSER_name()
eventInfo = ParserRingInfo.PARSER_events()


print(f'Scan \"PlumeF\"')
info = bleScan.getAdvEventScanInfo('local_name', 'PlumeF')

#print(f'Scan \"PlumeF-100111200-13-0606\"')
#info = bleScan.getAdvEventScanInfo('local_name', 'PlumeF-100111200-13-0606')


#print(f'Scan \"PlumeF-110101100-13-0695\"')
#info = bleScan.getAdvEventScanInfo('local_name', 'PlumeF-110101100-13-0695')

#

#print(f'Scan \"PlumeF-000000000-00-AAAA\"')
#print(f'Scan \"000000-000000000-00-0000\"')
#info = bleScan.getAdvEventScanInfo('local_name', '000000-000000000-00-0000')
#

#print(f'Scan \"\"')
#info = bleScan.getAdvEventScanInfo('local_name', '')
#

#print(f'Scan \"60:B4:F7:B3:06:9E\"')
#info = bleScan.getAdvEventScanInfo('bd_addr', '60:B4:F7:B3:06:9E')
#

#print(f'Scan \"AA:AA:AA:AA:AA:AA\"')
#info = bleScan.getAdvEventScanInfo('bd_addr', 'AA:AA:AA:AA:AA:AA')
#
if (info != None):
    for i, dev in enumerate(info):
        print(dev)
        print(f'Adv Name   : {dev["local_name"]}')
        print(f'BD addr    : {dev["bd_addr"]}')
        print(f'Size       : {dev["ring_size"]}')
        print(f'Color      : {ringInfo.get_ring_color(dev["ring_color"])}')
        print(f'Ship region: {ringInfo.get_ship_region(dev["ship_region"])}')
        print(f'PPG_type   : {ringInfo.get_ppg_type(dev["ppg_type"])}')
        print(f'Flash_type : {ringInfo.get_flash_type(dev["flash_type"])}')
        print(f'HW ver     : {dev["hw_ver"]}')
        
        if ('event_type' in dev):
            print(f'Event type : {dev["event_type"]}')
            print(f'time       : {datetime.datetime.fromtimestamp(dev["timestamp"])}')
            
            if dev["event_type"] == 'BATT':
                print(f'Warn type  : {eventInfo.get_batt_warn_type(dev["warn_type"])}')
                print(f'BATT level : {dev["batt_lvl"]}')

            if dev["event_type"] == 'HR':
                print(f'Warn type  : {eventInfo.get_hr_warn_type(dev["warn_type"])}')
                print(f'HR         : {dev["hr"]}')
                print(f'Threshold  : {dev["hr_threshold"]}')

            if dev["event_type"] == 'SPO2':
                print(f'Warn type  : {eventInfo.get_spo2_warn_type(dev["warn_type"])}')
                print(f'SpO2       : {dev["spo2"]}')
                print(f'Threshold  : {dev["spo2_threshold"]}')

            if dev["event_type"] == 'ACTIVITY':
                print(f'Warn type  : {eventInfo.get_activity_warn_type(dev["warn_type"])}')
                if dev["warn_type"] == 1:
                    print(f'Risk Level : {dev["fall_risk_lvl"]}')
                    print(f'Threshold  : {dev["fall_threshold"]}')
                    print(f'Fll HR     : {dev["fall_hr"]}')
                    print(f'Rest HR    : {dev["fall_rest_hr"]}')

                if dev["warn_type"] == 2:
                    print(f'State      : {dev["activity_state"]}')


        print('\n')

