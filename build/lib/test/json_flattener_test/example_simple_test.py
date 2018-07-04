import unittest
from grindrpy.json_flattener.flattener import Flattener
from grindrpy.json_flattener.value import Value, DerivedValue, ListValue

class SimpleExamples(unittest.TestCase):
    test_json = {
        "firstName": "John",
        "lastName": "Smith",
        "age": 25,
        "address":
            {
                "streetAddress": "21 2nd Street",
                "city": "New York",
                "state": "NY",
                "postalCode": "10021"
            },
        "phoneNumber":
            [
                {
                    "type": "home",
                    "number": "212 555-1234"
                },
                {
                    "type": "fax",
                    "number": "646 555-4567"
                }
            ]
    }

    def filtered_view_test(self):
        class ExampleFilteredView(Flattener):
            __field_names__ = ["firstName", "lastName", "age"]

        exampleFiltereView = ExampleFilteredView()

        self.assertEqual(list(exampleFiltereView.flatten(SimpleExamples.test_json)),
                         [{"firstName": "John", "lastName": "Smith", "age": 25}])

    def renamed_test(self):
        class RenamedView(Flattener):
            __field_names__ = ["last", "first", "age"]
            last = Value("lastName", False)
            first = Value("firstName", False)

        renamedView = RenamedView()

        self.assertEqual(list(renamedView.flatten(SimpleExamples.test_json)),
                         [{"first": "John", "last": "Smith", "age": 25}])

    def derive_value_test(self):
        def concatenation(lastName, firstName):
            lastName = "" if lastName is None else lastName[0]
            firstName = "" if firstName is None else firstName[0]
            return " ".join([firstName, lastName])

        class ConcName(Flattener):
            __field_names__ = ["name", "age"]

            name = DerivedValue(concatenation,
                                dict(lastName=Value("lastName", False), firstName=Value("firstName", False)))

        concName = ConcName()

        self.assertEqual(list(concName.flatten(SimpleExamples.test_json)),
                         [{"name": "John Smith", "age": 25}])

    def nested_values_test(self):

        class Nested(Flattener):
            __field_names__ = ["firstName", "lastName", "age", "streetAddress", "city", "state", "postalCode"]

            streetAddress = Value("address.streetAddress", False)
            city = Value("address.city", False)
            state = Value("address.state", False)
            postalCode = Value("address.postalCode", False)

        nested = Nested()

        self.assertEqual(list(nested.flatten(SimpleExamples.test_json)),
                         [{"firstName": "John", "lastName": "Smith", "age": 25, "streetAddress": "21 2nd Street",
                           "city": "New York", "state": "NY", "postalCode": "10021"}])

    def list_value_test(self):

        class ListValues(Flattener):
            __field_names__ = ["firstName", "lastName", "age", "phoneNumber", "phoneType"]

            phoneNumber = ListValue(Value("phoneNumber.number", False))
            phoneType = ListValue(Value("phoneNumber.type", False))

        listValue = ListValues()

        self.assertEqual(list(listValue.flatten(SimpleExamples.test_json)),
                         [{"firstName": "John", "lastName": "Smith", "age": 25, "phoneNumber": "212 555-1234", "phoneType": "home"},
                          {"firstName": "John", "lastName": "Smith", "age": 25, "phoneNumber": "646 555-4567", "phoneType": "fax"}])


