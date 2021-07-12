import pyudev
import re
import subprocess
from threading import Thread
import sys
from subprocess import Popen, PIPE, CalledProcessError

class ShellController:
    def __init__(self):
        self.udev_context = pyudev.Context()
        self.local_dir    = "/home/ubuntu/PiSDimager/static/images"
        self.usb_mnt_dir  = "/media/pisdImager/"
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
            self.status="dd-copy"
            line = ''
            while True:
                out = process.stderr.read(1)
                # print(type(out))
                if out == '' and process.poll() != None:
                    print("ending here")
                    break
                if out != '':
                    s = out.decode("utf-8")
                    if s == '\r':
                        self.formatDDOutput(line)
                        line = ''
                    else:
                        line = line + s
                if out == b'':
                    print("wtf",out.decode('utf-8'))
                    break

        except Exception as e:
            print(str(e))
            return "error"
    
    def commandExec(self, command):
        try:
            out = subprocess.check_output(command, shell=True)
            return out.decode().rstrip("\n")
        except:
            return "error"
    
    def execute(self, cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


    def PishrinkExec(self, command):
        try:
            process = subprocess.Popen(command, stderr=subprocess.PIPE)
            self.status="pishrink"
            line = ''
            while True:
                out = process.stderr.read(1)
                # print(type(out))
                if out == '' and process.poll() != None:
                    print("ending here")
                    break
                if out != '':
                    s = out.decode("utf-8")
                    if s == '\r':
                        print("pishrink", line)
                        line = ''
                    else:
                        line = line + s
                if out == b'':
                    print("wtf",out.decode('utf-8'))
                    break

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
        cmd = ["sudo", "dd", "if={}".format(sd_card), "of={}".format(output), "bs={}".format(bs), "status=progress"]
        self.ddExec(cmd)


    def PiShrink(self, file, zip=True, reset=True):
        cmd = ['pishrink.sh']
        if(zip):
            cmd.append("-a")
            cmd.append("-z")
        if(reset):
            cmd.append("-p")

        cmd.append("-v")
        cmd.append(file)

        for out in self.execute(cmd):
            print("test", out, end="")

        # Thread(target=self.commandExec, args=(cmd,)).start()
    
    def mountMassStorage(self, device, location):
        pass


if __name__ == "__main__":
    sc = ShellController()
    # 21404581888 bytes (21 GB, 20 GiB) copied, 726 s, 29.5 MB/s
    # sc.formatDDOutput("21404581888 bytes (21 GB, 20 GiB) copied, 726 s, 29.5 MB/s")

    # sc.MakeSDImage("/dev/sda", "python.img")
    
    sc.PiShrink('python_back.img', zip=True)

    # res = sc.USBDeviceList()
    # print(res.keys())
    # print(res['/dev/sda'].get('ID_MODEL'))