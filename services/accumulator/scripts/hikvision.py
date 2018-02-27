from dicttoxml import dicttoxml
import xmltodict
import yaml
from config import *
import requests

class Hikvision():
    def __init__(self, config=hikvision_url_default):
        if config:
            self.auth = config['auth']
            self.device_url = config['device_url']
        else:
            self.auth = ''
            self.device_url = ''

    def set_config_part(self, config_xml, url):
        return requests.put(self.device_url + url, data=config_xml, auth=self.auth)

    def put_config(self, config_yaml):
        config = yaml.load(config_yaml)
        previous_url = None
        for key, url in sorted([(k, urls[k]) for k in config], key=lambda x: x[1]):
            if not previous_url or previous_url != url:
                if previous_url:
                    print(self.set_config_part(dicttoxml(data), previous_url))
                current_setting_xml = requests.get(self.device_url + urls[key], auth=self.auth).text
                current_setting = data = xmltodict.parse(current_setting_xml)
            else:
                current_setting = data

            for i in place[key][:-1]:
                current_setting = current_setting[i]
            current_setting[place[key][-1]] = config[key]
            previous_url = url
        print(self.set_config_part(dicttoxml(data), urls[key]))
