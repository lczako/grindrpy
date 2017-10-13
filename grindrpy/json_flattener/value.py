class AbstractValue:

    def getValue(self, json_object):
        raise Exception("Abstract class method cannot be called")


class Value(AbstractValue):

    def __init__(self, path, required):
        self.path = path if isinstance(path, list) else path.split(".")
        self.required = required
        self.get = Value.get_required if required else Value.get_optional

    def __str__(self):
        return "Value instance: %s" % self.__dict__

    @staticmethod
    def get_required(json_object, key):
        if json_object[key] is None: raise ValueError("Got None for a required value: %s" % key)
        return json_object[key]

    @staticmethod
    def get_optional(json_object, key):
        return json_object.get(key, None)

    def getValue(self, json_object):
        sub_path = list(self.path)
        key = sub_path.pop(0)
        element = self.get(json_object, key)
        if isinstance(element, list) and sub_path: return map(lambda x: Value(sub_path, self.required).getValue(x)[0], element)
        elif isinstance(element, dict) and sub_path: return Value(sub_path, self.required).getValue(element)
        else: return element if isinstance(element, list) else [element]


class DerivedValue(AbstractValue):

    def __init__(self, func, values):
        if not isinstance(values, dict): raise ValueError("DerivedValue needs dict type values")
        self.func = func
        self.values = values

    def getValue(self, json_object):
        result = self.func(**{k: v.getValue(json_object) for k, v in self.values.iteritems()})
        return result if isinstance(result, list) else [result]


class ListValue(AbstractValue):

    def __init__(self, value):
        if not isinstance(value, AbstractValue): raise ValueError("ListValue needs an AbstractValue type parameter")
        self.value = value

    def getValue(self, json_object):
        result = self.value.getValue(json_object)
        return result if isinstance(result, list) else [result]
