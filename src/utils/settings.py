from src.adls_management import messages
import json


class GenericSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.1.0"

    def __init__(self, configuration_file="resources/connection_config.json"):
        # config.json settings
        self.main_config_file = configuration_file
        self.meta_version = None
        self.output_directory = None
        self.log_config = None
        self.suppress_azure_call = False
        self.azure_http_proxy = None
        self.azure_https_proxy = None
        self.storage_account_name = None
        self.storage_account_key = None
        self.storage_container = None
        self.azure_secrets = None

    def get_config(self):
        """
            get the main configuration settings. default file is resources/config.json
        """
        module = __name__ + ".get_config"
        result = messages.message["undetermined"]

        try:
            with open(self.main_config_file) as config:
                data = json.load(config)
                # self.schema_directory = self.base_schema_folder + self.meta_version + "/"
                if "azure_secrets" in data:
                    self.azure_secrets = data["azure_secrets"]
                if "suppress_azure_call" in data:
                    if data["suppress_azure_call"] == "True":
                        self.suppress_azure_call = True
                    elif data["suppress_azure_call"] == "False":
                        self.suppress_azure_call = False
                    else:
                        print("Incorrect config value >" + data["suppress_azure_call"]
                              + "< for suppress_azure_call. Must be True or False. Will default to False")
                        self.suppress_azure_call = False
            result = messages.message["ok"]

        except FileNotFoundError:
            print("FATAL:", module, "could find not main configuration file >" + self.main_config_file + "<.")
            return messages.message["main_config_not_found"]

        if self.azure_secrets is None:
            print("azure_secrets is unknown")
        else:
            azure_secrets_result = self.get_azure_secrets(self.azure_secrets)
            if azure_secrets_result == messages.message["ok"]:
                print("get_azure_secrets returned OK", module)
            else:
                print("get_azure_secrets returned: " + azure_secrets_result["code"], module)
                return azure_secrets_result

        return result

    def get_azure_proxy(self):

        if self.azure_http_proxy == "None":
            self.azure_http_proxy = None
        if self.azure_https_proxy == "None":
            self.azure_https_proxy = None

        proxies = {
            "http": self.azure_http_proxy,
            "https": self.azure_https_proxy
        }
        return proxies

    def get_azure_secrets(self, azure_secrets="resources/edc.secrets"):
        module = __name__ + ".get_azure_secrets"

        try:
            with open(azure_secrets) as azure:
                data = json.load(azure)
                result = self.determine_azure_secrets(data)

                if result == messages.message["ok"]:
                    print("EDC secrets file >" + self.azure_secrets + "< found and read."
                          , module)
                else:
                    print("determine edc secrets returned: " + result["code"])
                    return result
        except FileNotFoundError:
            print("Cannot find provided azure_secrets file >" + self.azure_secrets + "<."
                  , module)
            return messages.message["azure_secrets_not_found"]

        return messages.message["ok"]

    def determine_azure_secrets(self, data):
        module = __name__ + ".determine_azure_secrets"

        if "meta_version" in data:
            main_meta_version = data["meta_version"][:3]
            if main_meta_version == "0.1":
                print("main_meta_version of edc secrets is >" + main_meta_version + "<."
                      , module)
            else:
                print("Unsupported meta_version >" + data["meta_version"] + "<."
                      , module)
                return messages.message["unsupported_meta_version_azure_secrets"]
        else:
            print("Backward compatible edc secrets file detected. Please update to a later version."
                  , module)

        self.storage_container = data["container"]
        print("container: ", self.storage_container)
        if "azure_http_proxy" in data:
            self.azure_http_proxy = data["azure_http_proxy"]
            print("HTTP Proxy for Azure taken from edc secrets file: "
                  + self.azure_http_proxy, module)
        else:
            print("No HTTP Proxy for Azure found in edc secrets file. "
                  + "This is OK if no proxy is needed or has been set through the environment variable HTTP_PROXY"
                  , module)
        if "azure_https_proxy" in data:
            self.azure_https_proxy = data["azure_https_proxy"]
            print("HTTPS Proxy for Azure taken from edc secrets file: "
                  + self.azure_https_proxy, module)
        else:
            print("No HTTPS Proxy for Azure found in edc secrets file. "
                  + "This is OK if no proxy is needed or has been set through the environment variable HTTPS_PROXY"
                  , module)

        return messages.message["ok"]
