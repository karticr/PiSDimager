import pyudev
import re

context = pyudev.Context()
# for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
for device in context.list_devices():
    # print(device)
    if(device.get('ID_USB_DRIVER') == "usb-storage" and device.get('DEVTYPE') == "disk"):
        count = 0
        dev_name = device.get('DEVNAME')
        result = re.sub(r'[0-9]+', '', dev_name)
        name   = device.get("ID_MODEL")
        print(result, name)
        
        # for i in device:
        #     print(i, " ", device.get(i))