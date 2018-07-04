import unittest
from grindrpy.json_flattener.value import Value, DerivedValue, ListValue


class TestValue(unittest.TestCase):

    def test_one_level(self):
        test_json = {"apple": 1, "plum": 2, "peach": 3, "required": None}
        self.assertEqual(Value("apple", True).getValue(test_json), [1], "incorrect value")
        self.assertEqual(Value("apple", False).getValue(test_json), [1], "incorrect value")
        self.assertEqual(Value("pear", False).getValue(test_json), [None], "incorrect value")
        with self.assertRaises(KeyError): Value("pear", True).getValue(test_json)
        with self.assertRaises(ValueError): Value("required", True).getValue(test_json)

    def test_list_value0(self):
        test_json = {"apple": 1, "plum": [1, 2, 3], "peach": 234}
        value_path = "plum"
        self.assertEqual(Value(value_path, True).getValue(test_json), [1,2,3], "incorrect result")

        test_json2 = {"apple": 1, "plum": [{"a": 1}, {"a": 2}, {"a": 3}], "peach": 234}
        value_path="plum.a"
        self.assertEqual(Value(value_path, True).getValue(test_json2), [1, 2, 3], "incorrect result")

    def test_list_value(self):
        test_json = {"apple": 1, "plum": [1, 2, 3], "peach": 234}
        value_path = "plum"
        self.assertEqual(ListValue(Value(value_path, True)).getValue(test_json), [1,2,3], "incorrect result")

        test_json2 = {"apple": 1, "plum": [{"a": 1}, {"a": 2}, {"a": 3}], "peach": 234}
        value_path="plum.a"
        self.assertEqual(ListValue(Value(value_path, True)).getValue(test_json2), [1, 2, 3], "incorrect result")

    def test_multi_level(self):
        test_json = {"a": {"b": 1, "c": 2, "d": {"e": 3, "f": {"g": "h"}}}}
        value_path = "a.d.f.g"
        self.assertEqual(Value(value_path, True).getValue(test_json), ["h"], "incorrect result")

    def test_complex(self):
        test_json = {"apple": 1, "plum": [{"a": {"c": 1}}, {"a": {"c": 2}}, {"a": {"c": 3}}],
                     "peach": {"newlist": {"results": [2, 3, 4]}}}
        value_path1 = "plum.a.c"
        value_path2 = "peach.newlist.results"
        self.assertEqual(Value(value_path1, True).getValue(test_json), [1, 2, 3], "incorrect result")
        self.assertEqual(Value(value_path2, True).getValue(test_json), [2, 3, 4], "incorrect result")

    def test_derived_value(self):
        test_json = {"apple": 1, "plum": [1, 2, 3], "peach": 234}

        def func(a1, a2):
            return a1[0] * sum(a2)

        self.assertEqual(DerivedValue(func, dict(a1=Value("apple", False),
                                                 a2=Value("plum", False))).getValue(test_json), [6])
