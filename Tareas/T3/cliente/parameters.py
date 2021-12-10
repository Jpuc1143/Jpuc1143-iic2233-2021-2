import json


# https://stackoverflow.com/questions/3155436/getattr-for-static-class-variables-in-python
class MetaParameters(type):
    __parameters = json.load(open("parametros.json", "r"))

    def __getattr__(cls, parameter):
        return MetaParameters.__parameters[parameter]


class Parameters(metaclass=MetaParameters):
    pass
