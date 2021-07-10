
class ShellController:
    def __init__(self):
        pass
    
    def commandExec(self, command):
        try:
            out = subprocess.check_output(command, shell=True)
            return out.decode().rstrip("\n")
        except:
            return "error"