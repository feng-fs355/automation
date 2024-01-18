"""
example

"""
import time

color_types = ['Unknown', 'Titanium', 'Gold']
ship_regions = ['Unknown', 'US', 'EU', 'UK']
ppg_types = ['Error', 'MAXIM', 'Renesas']
flash_types = ['Error', 'W25Q64JW_JEDEC_ID', 'W25Q64JWBYIQ_JEDEC_ID']

class PARSER_name(object):

    def get_ring_color(self, index):
        if (index > (len(color_types) - 1)):
            index = 0
        return color_types[index]

    def get_ship_region(self, index):
        if (index > (len(ship_regions) - 1)):
            index = 0
        return ship_regions[index]

    def get_ppg_type(self, index):
        if (index > (len(ppg_types) - 1)):
            index = 0
        return ppg_types[index]

    def get_flash_type(self, index):
        if (index > (len(flash_types) - 1)):
            index = 0
        return flash_types[index]

batt_warn_type = ['BATT critical low', 'Batt Low', 'Full charged', 'Status changed']
hr_warn_type = ['HR Low', 'Rest HR High', 'Activity HR High']
spo2_warn_type = ['SpO2 low']
activity_warn_type = ['Sleep', 'Fall', 'Activity']
activity_state = ['Resting', 'Walking', 'Running', 'Unknow']

class PARSER_events(object):

    def get_batt_warn_type(self, index):
        if (index > (len(batt_warn_type) - 1)):
            index = 0
        return batt_warn_type[index]

    def get_hr_warn_type(self, index):
        if (index > (len(hr_warn_type) - 1)):
            index = 0
        return hr_warn_type[index]

    def get_spo2_warn_type(self, index):
        if (index > (len(spo2_warn_type) - 1)):
            index = 0
        return spo2_warn_type[index]

    def get_activity_warn_type(self, index):
        if (index > (len(activity_warn_type) - 1)):
            index = 0
        return activity_warn_type[index]

    def get_activity_state(self, index):
        if (index > (len(activity_state) - 1)):
            index = 0
        return activity_state[index]