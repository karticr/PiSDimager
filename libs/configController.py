import json

class ConfigController:
    def __init__(self, conf_dir="config.json"):
        self.conf_dir = conf_dir

    def updateConfigToFile(self, data):
        with open(self.conf_dir, "w") as w:
            json.dump(data, w, indent=4)

    def loadConfigFromFile(self):
        with open(self.conf_dir) as f:
            data = json.load(f)
        return data

    def updateConfig(self, key, word):
        data = self.loadConfigFromFile()
        data['key'] = word
        updateConfigToFile(data)
