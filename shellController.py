import pyudev
import re
import subprocess
from threading import Thread
import sys
from subprocess import Popen, PIPE, CalledProcessError

class ShellController:
    def __init__(self):
        self.udev_context = pyudev.Context()
        self.usb_mnt_dir  = "/media/pisd_imager"
        self.dd_prog_msg  = {}
        self.status       = ""

    def formatDDOutput(self, msg):
        msg_list = msg.split(" ")
        if(len(msg_list) >= 10):
            data_in_bytes = msg_list[0] + " " + msg_list[1]
            data_moved    = msg_list[2] + " " + msg_list[3] + " " + msg_list[4] + " " + msg_list[5] + " " + msg_list[6]
            time_elapsed  = msg_list[7]
            speed         = msg_list[9] + " " + msg_list[10]

            data = {
                "data_in_bytes": data_in_bytes,
                "data_moved"   : data_moved,
                "time_elapsed"  : float(time_elapsed),
                "speed"        : speed
            }
            print(data)
            self.dd_prog_msg = data

    def ddExec(self, command):
        try:
            process = subprocess.Popen(command, stderr=subprocess.PIPE)
            line = ''
            while True:
                out = process.stderr.read(1)
                if out == '' and process.poll() != None:
                    break
                if out != '':
                    s = out.decode("utf-8")
                    if s == '\r':
                        self.formatDDOutput(line)
                        line = ''
                    else:
                        line = line + s
                    
        except Exception as e:
            print(str(e))
            return "error"
    
    def USBDeviceList(self):
        devices = {}
        for device in self.udev_context.list_devices():
            if(device.get('ID_USB_DRIVER') == "usb-storage" and device.get('DEVTYPE') == "disk"):
                dev_name = device.get('DEVNAME')
                devices[dev_name] = device
        return devices

    def MakeSDImage(self, sd_card, output, bs="1M"):
        # cmd = "sudo dd if={} of={} bs={} status=progress".format(sd_card, output, bs)
        cmd = ["sudo", "dd", "if={}".format(sd_card), "of={}".format(output), "bs={}".format(bs), "status=progress"]
        print(cmd)
        self.ddExec(cmd)


    def PiShrink(self, file, zip=True):
        if(zip):
            cmd = "sudo pishrink.sh -z {}".format(file)
        else:
            cmd = "sudo pishrink.sh {}".format(file)

        self.commandExec(cmd)
        # Thread(target=self.commandExec, args=(cmd,)).start()
    
    def mountMassStorage(self, device, location):
        pass


if __name__ == "__main__":
    sc = ShellController()
    # 21404581888 bytes (21 GB, 20 GiB) copied, 726 s, 29.5 MB/s
    sc.formatDDOutput("21404581888 bytes (21 GB, 20 GiB) copied, 726 s, 29.5 MB/s")

    sc.MakeSDImage("/dev/sda", "python.img")

    # res = sc.USBDeviceList()
    # print(res.keys())
    # print(res['/dev/sda'].get('ID_MODEL'))