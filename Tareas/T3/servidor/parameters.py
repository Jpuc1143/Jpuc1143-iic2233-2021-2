import json
import os
from PyQt5.QtCore import QSize


# https://stackoverflow.com/questions/3155436/getattr-for-static-class-variables-in-python
class MetaParameters(type):
    __parameters = json.load(open("parametros.json", "r"))

    def __getattr__(cls, parameter):
        if "PATH_" in parameter:
            return os.path.join(*MetaParameters.__parameters[parameter])
        if "SIZE_" in parameter:
            return QSize(*MetaParameters.__parameters[parameter])
        else:
            return MetaParameters.__parameters[parameter]


class Parameters(metaclass=MetaParameters):
    pass
