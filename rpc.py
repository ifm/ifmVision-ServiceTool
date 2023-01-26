import xmlrpc.client
import requests
import functools
import os
import json
from pathlib import Path


def message_decorator(func):
    def wrapper_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
            success_message = "Download for function {} was successful.".format(func.__name__)
            return success_message
        except Exception as e:
            error_message = "Download for function {} failed:\n{}".format(func.__name__, e)
            return error_message

    return wrapper_function


class RPC(object):
    def __init__(self, address="192.168.0.69", api_path="/api/rpc/v1/",
                 save_folder=str(os.path.join(Path.home(), "Downloads"))):
        self.address = address
        self.api_path = api_path
        self.save_folder = save_folder
        self.storage_path = "http://" + self.address + "/storage/"
        self.baseURL = "http://" + self.address + self.api_path
        self.mainURL = self.baseURL + "com.ifm.efector/"
        self.rpc = xmlrpc.client.ServerProxy(self.mainURL, allow_none=True)
        self.timeout = 2

        self.request = requests.Session()
        self.request.request = functools.partial(self.request.request, timeout=self.timeout)

    @property
    def save_path(self) -> str:
        ip_regex = self.address.replace('.', '_')
        sensor_name = self.call_getParameter_function(param="Name").replace(' ', '_')
        sensor_model = self.call_getParameter_function(param="ArticleNumber").replace(' ', '_')
        path = os.path.join(self.save_folder, ip_regex + "_{name}_{model}"
                            .format(name=sensor_name, model=sensor_model))
        path_exist_flag = os.path.exists(path)
        if not path_exist_flag:
            # Create a new directory because it does not exist
            os.makedirs(path)
        return path

    def call_getParameter_function(self, param) -> str:
        response = self.rpc.getParameter(param)
        return response

    @staticmethod
    def save_dict_as_json(data, file_path):
        parsed = json.dumps(data, indent=4)
        with open(file_path, "w") as f:
            print(parsed, file=f)

    @message_decorator
    def start_getAllParameters_download(self):
        response = self.rpc.getAllParameters()
        json_file = os.path.join(self.save_path, "getAllParameters.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_getSWVersion_download(self):
        response = self.rpc.getSWVersion()
        json_file = os.path.join(self.save_path, "getSWVersion.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_getHWInfo_download(self):
        response = self.rpc.getHWInfo()
        json_file = os.path.join(self.save_path, "getHWInfo.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_getApplicationList_download(self):
        response = self.rpc.getApplicationList()
        json_file = os.path.join(self.save_path, "getApplicationList.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_getActiveDataConnections_download(self):
        response = self.rpc.getActiveDataConnections()
        json_file = os.path.join(self.save_path, "getActiveDataConnections.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_getTraceLogs_download(self, lines=1000):
        response = self.rpc.getTraceLogs(lines)
        json_file = os.path.join(self.save_path, "getTraceLogs.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_getDmesgData_download(self):
        response = self.rpc.getDmesgData()
        json_file = os.path.join(self.save_path, "getDmesgData.json")
        self.save_dict_as_json(data=response, file_path=json_file)

    @message_decorator
    def start_serviceReport_download(self):
        receive = requests.get(self.storage_path + "service_report/")
        _save_path_dir = os.path.join(self.save_path, "service_report.zip")
        with open(r'{}'.format(_save_path_dir), 'wb') as f:
            f.write(receive.content)

    @message_decorator
    def start_deviceAndApplicationSettings_download(self):
        receive = requests.get(self.storage_path + "device_configuration/")
        _save_path_dir = os.path.join(self.save_path, "device_configuration.zip")
        with open(r'{}'.format(_save_path_dir), 'wb') as f:
            f.write(receive.content)

    def call_doPing_function(self) -> str:
        try:
            result = self.request.get(self.mainURL + "?method=doPing&params=[]")
            if result.ok:
                return "up"
        except requests.exceptions.ConnectTimeout:
            return "down"
        except requests.exceptions.ConnectionError:
            return "error"

