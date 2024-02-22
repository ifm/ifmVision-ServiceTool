import xmlrpc.client
import requests
import functools
import enum
import os
import json
import multiprocessing.pool
from datetime import date
import shutil
from pathlib import Path


class DevicesMeta(enum.Enum):
    O2D5xx = {"DeviceType": ["1:320", 0x140],
              "ConfigExtension": "o2d5xxcfg"}
    O2I5xx = {"DeviceType": ["1:256", 0x100],
              "ConfigExtension": "o2i5xxcfg"}
    O3D3xx = {"DeviceType": ["1:3", 0x003],
              "ConfigExtension": "o3d3xxcfg"}

    @classmethod
    def getData(cls, key, value):
        for s in DevicesMeta:
            _data = s.value[key]
            if isinstance(_data, list):
                for v in _data:
                    if v == value:
                        return s
            else:
                if _data == value:
                    return s


def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


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

    @timeout(3)
    def __init__(self, address="192.168.0.69", api_path="/api/rpc/v1/",
                 save_folder=str(os.path.join(Path.home(), "Downloads"))):
        self.address = address
        self.api_path = api_path
        self.save_folder = save_folder
        self.storage_path = "http://" + self.address + "/storage/"
        self.baseURL = "http://" + self.address + self.api_path
        self.mainURL = self.baseURL + "com.ifm.efector/"
        self.rpc = xmlrpc.client.ServerProxy(self.mainURL, allow_none=True)
        self.device_type = self.rpc.getParameter("DeviceType")
        self.operating_mode = self.rpc.getParameter("OperatingMode")
        if self.operating_mode != "0":
            raise ConnectionAbortedError
        self.device_meta = DevicesMeta.getData(key="DeviceType", value=self.device_type)
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

    def call_getFWVersion_function(self) -> str:
        response = self.rpc.getSWVersion()
        return response["IFM_Software"]

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
        if 0x003 not in self.device_meta.value["DeviceType"]:  # getDmesgData not available for O3D3xx sensor
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
        cfg_extension = self.device_meta.value["ConfigExtension"]
        _save_path_dir = os.path.join(self.save_path, "device_configuration.{}".format(cfg_extension))
        with open(r'{}'.format(_save_path_dir), 'wb') as f:
            f.write(receive.content)

    @message_decorator
    def start_ifmVisionAssistantCrashDumps_download(self):
        _save_path_dir = os.path.join(self.save_path, "crashDumps")
        Path(_save_path_dir).mkdir(parents=True, exist_ok=True)
        roaming_folder = os.getenv('APPDATA')
        crash_dumps_folder = os.path.join(roaming_folder, "ifm electronic", "ifmVisionAssistant", "crashDumps")
        crash_dump_files = [file for file in os.listdir(crash_dumps_folder) if file.endswith('.dmp')]
        for file in crash_dump_files:
            abs_file_path = os.path.join(crash_dumps_folder, file)
            path = Path(abs_file_path)
            timestamp = date.fromtimestamp(path.stat().st_mtime)
            if date.today() == timestamp:
                shutil.copy2(abs_file_path, _save_path_dir)

    @message_decorator
    def start_ifmVisionAssistantExtendedLogs_download(self):
        _save_path_dir = os.path.join(self.save_path, "logs")
        Path(_save_path_dir).mkdir(parents=True, exist_ok=True)
        roaming_folder = os.getenv('APPDATA')
        extended_logs_folder = os.path.join(roaming_folder, "ifm electronic", "ifmVisionAssistant", "logs")
        extended_logs_files = [file for file in os.listdir(extended_logs_folder) if file.endswith('.log')]
        for file in extended_logs_files:
            abs_file_path = os.path.join(extended_logs_folder, file)
            path = Path(abs_file_path)
            timestamp = date.fromtimestamp(path.stat().st_mtime)
            if date.today() == timestamp:
                shutil.copy2(abs_file_path, _save_path_dir)

    def call_doPing_function(self) -> str:
        try:
            result = self.request.get(self.mainURL + "?method=doPing&params=[]")
            if result.ok:
                return "up"
        except requests.exceptions.ConnectTimeout:
            return "down"
        except requests.exceptions.ConnectionError:
            return "error"

