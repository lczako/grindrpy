# Complex examples

In the following examples will cover more complex parsing use cases.

## Example - nested lists

In this example let's assume, that we have a database which contains the daily movement of the users by collecting the main stop points
as it shown by the example json below.

```
{
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
```

I want to normalize the data by flattening the coordinates list and get only one x-y coordinate pair by row.
I want a result like the following.

```
{"user": "jytfghtdrthfb", "date": "2017-08-22", "x_coord": 2.23456, "y_coord": 11.87676564}
{"user": "jytfghtdrthfb", "date": "2017-08-22", "x_coord": 2.656546, "y_coord": 11.9878776}
...
```

In this example we define a list_path which will act just as a marker and define the coordinate fields with a DerivedValue.

```
def get_x(coordinates): return [coordinates[0][0], coordinates[1][0]]

def get_y(coordinates): return [coordinates[0][1], coordinates[1][1]]

class NestedList(Flattener):
    __field_names__ = ["user", "date", "x_coord", "y_coord"]

    x_coord = ListValue(DerivedValue(get_x, dict(coordinates=Value("daily_movement.coordinates", False))))
    y_coord = ListValue(DerivedValue(get_y, dict(coordinates=Value("daily_movement.coordinates", False))))

```


## Example - flattening with multiple lists

```
{
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
        ]
}
```

I want to create food and possible drink pairing result. I want to have the product of the food and drink choices in the result as the following:

```
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "ceasar salad", "drink": "water"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "ceasar salad", "drink": "cappuccino"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "coconut soup", "drink": "water"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "coconut soup", "drink": "cappuccino"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "fried chicken, s rice", "drink": "water"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "fried chicken, s rice", "drink": "cappuccino"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "tiramisu", "drink": "water"}
{"user": "iuhjfb", "timestamp": "2078-08-11 13:48:09", "food": "tiramisu", "drink": "cappuccino"}
```

I use DerivedValue getter and a fake path_list value as a marker for the lists.

```
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

```

You can try or play around with the complex examples in the test/example_complex.py.
