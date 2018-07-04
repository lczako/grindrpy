from grindrpy.json_flattener.flattener import Flattener
from grindrpy.json_flattener.value import Value, DerivedValue, ListValue
import unittest

class TestComplexExamples(unittest.TestCase):

    def test_nested_list(self):
        test_json = {
                        "user": "jytfghtdrthfb",
                        "date": "2017-08-22",
                        "daily_movement": {
                            "coordinates": [
                                [2.23456, 11.87676564],
                                [2.656546, 11.9878776]
                            ],
                            "type": "point"
                            },
                        "user_type": "commuter"
                    }

        def get_x(coordinates): return [coordinates[0][0], coordinates[1][0]]

        def get_y(coordinates): return [coordinates[0][1], coordinates[1][1]]

        class NestedList(Flattener):
            __field_names__ = ["user", "date", "x_coord", "y_coord"]

            x_coord = ListValue(DerivedValue(get_x, dict(coordinates=Value("daily_movement.coordinates", False))))
            y_coord = ListValue(DerivedValue(get_y, dict(coordinates=Value("daily_movement.coordinates", False))))

        nested_list = NestedList()

        self.assertEqual(list(nested_list.flatten(test_json)),
                         [{"user": "jytfghtdrthfb", "date": "2017-08-22", "x_coord": 2.23456, "y_coord": 11.87676564},
                          {"user": "jytfghtdrthfb", "date": "2017-08-22", "x_coord": 2.656546, "y_coord": 11.9878776}])

    def test_multiple_list(self):

        test_json = {
                        "user": "iuhjfb",
                        "timestamp": "2078-08-11 13:48:09",
                        "food_order": [
                                "ceasar salad",
                                "coconut soup",
                                "fried chicken, s rice",
                                "tiramisu"
                                ],
                        "drink_order": [
                                "water",
                                "cappuccino"
                        ]}

        def get_f(food_order, drink_order, type):
            if type == "drink":
                return drink_order * len(food_order)
            else:
                result = []
                for fo in food_order:
                    result.extend([fo] * len(drink_order))
                return result

        def get_food(food_order, drink_order):
            return get_f(food_order, drink_order, type="food")

        def get_drink(food_order, drink_order):
            return get_f(food_order, drink_order, type="drink")

        class MultipleLists(Flattener):
            __field_names__ = ["user", "timestamp", "food", "drink"]

            food = ListValue(DerivedValue(get_food,
                                dict(food_order=Value("food_order", True), drink_order=Value("drink_order", True))))
            drink = ListValue(DerivedValue(get_drink,
                                 dict(food_order=Value("food_order", True), drink_order=Value("drink_order", True))))

        multiple_lists = MultipleLists()
        self.assertEqual(list(multiple_lists.flatten(test_json)), [
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "ceasar salad", "drink": "water"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "ceasar salad", "drink": "cappuccino"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "coconut soup", "drink": "water"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "coconut soup", "drink": "cappuccino"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "fried chicken, s rice", "drink": "water"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "fried chicken, s rice", "drink": "cappuccino"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "tiramisu", "drink": "water"},
                {"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "tiramisu", "drink": "cappuccino"}
                ])

