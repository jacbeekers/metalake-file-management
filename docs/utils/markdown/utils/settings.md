Module utils.settings
=====================

Classes
-------

`GenericSettings(configuration_file='resources/connection_config.json')`
:   Some generic utilities, e.g. reading the config.json

    ### Class variables

    `code_version`
    :

    ### Methods

    `determine_azure_secrets(self, data)`
    :

    `get_azure_proxy(self)`
    :

    `get_azure_secrets(self, azure_secrets='resources/azure.secrets')`
    :

    `get_config(self)`
    :   get the main configuration settings. default file is resources/config.json

    `get_file_locations(self, config_file)`
    :