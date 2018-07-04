from value import Value, AbstractValue, ListValue


class Flattener:

    __field_names__ = {}

    def __init__(self):
        self.values = self.set_values()
        class_vars = self.set_class_vars()
        for i in self.values:
            if i in class_vars:
                setattr(self, i, getattr(self, i))
            else:
                setattr(self, i, Value(i, False))

    def __str__(self):
        return "\n".join(["%s = %s" % (k, v) for k, v in self.__dict__.iteritems()])

    def set_values(self):
        values = self.__class__.__field_names__
        if len(values) != len(set(values)): raise ValueError("Found duplicated field name")
        return set(values)

    def set_class_vars(self):
        class_vars = [attr for attr in dir(self.__class__) if isinstance(getattr(self.__class__, attr), AbstractValue)]
        if not set(class_vars).issubset(self.values): raise ValueError("All result field names should be listed in __field_names__")
        return class_vars

    def parse(self, json_object):
        results = [(k, getattr(self, k).getValue(json_object), isinstance(getattr(self, k), ListValue)) for k in
                   self.values]
        listval_count = None
        for name, value_result, is_listvalue in results:
            if not is_listvalue and len(value_result) != 1:
                raise ValueError(
                    "Json is not matching the definition. More than one element in a non-ListValue %s: %s" % (name,
                                                                                                               value_result))
            elif is_listvalue:
                if not listval_count:
                    listval_count = len(value_result)
                elif listval_count != len(value_result):
                    raise ValueError(
                        "Json is not matching the definition. List values have different element numbers %s" %results)
        return results

    def flatten(self, json_object):
        results = self.parse(json_object)
        value_res = {non_list_values[0]: non_list_values[1][0] for non_list_values in
                     filter(lambda non_list_values: not non_list_values[2], results)}

        list_res = {list_values[0]: list_values[1] for list_values in
                     filter(lambda list_values: list_values[2], results)}
        if len(list_res) == 0:
            yield value_res
        else:
            for row in zip(*[list_res[k] for k in list_res.keys()]):
                res = dict(zip(list_res.keys(), row))
                res.update(value_res)
                yield res
