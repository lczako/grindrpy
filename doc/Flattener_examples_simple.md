# Example for simple cases

In the following examples I will use the json above as a test sample.

```
Customers:

{
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
```

## Example - Filtered view

In this example I want to have only the names of the customers. I want a result like
```
{"firstName": "John", "lastName": "Smith", "age": 25}
{"firstName": "Helga", "lastName": "Smith", "age": 12}
{"firstName": "Ingrid", "lastName": "Jones", "age": 45}
...
```

To get my desired result I only have to specify the field names in my definition, because the result field names and
the original json field names are the same. So the definiton will be the following:

```
class ExampleFilteredView(Flattener):
    __field_names__ = ["firstName", "lastName", "age"]
```

## Example - Renaming

In this example I want to rename the "firstName" field to "first" and the "lastName" to "last". I want to get a result like:
```
{"first": "John", "last": "Smith", "age": 25}
{"first": "Helga", "last": "Smith", "age": 12}
{"first": "Ingrid", "last": "Jones", "age": 45}
...
```

To reach my goal, I have to customize my result fields' values in the following way:

```
class RenamedView(Flattener):
    __field_names__ = ["last", "first", "age"]
    last = Value("lastName", False)
    first = Value("firstName", False)
```

## Example - Derived value

In this example I want to concatenate the "lastName" and "fistName" values as a result of the "name" value. I want the result
json to look like the following:
```
{"name": "John Smith", "age": 25}
{"name": "Helga Smith", "age": 12}
{"name": "Ingrid Jones", "age": 45}
...
```

To have this result I have to use DerivedValue for the customization of my "name" field and I have to define a function
which will make the concatenation happen. The definition should look like the
example below.

```
def concatenation(lastName, firstName):
    lastName = "" if lastName is None else lastName[0]
    firstName = "" if firstName is None else firstName[0]
    return " ".join([firstName, lastName])

class ConcName(Flattener):
    __field_names__ = ["name", "age"]

    name = DerivedValue(concatenation,
                        dict(lastName=Value("lastName", False), firstName=Value("firstName", False)))

```

## Example - Nested values

In this example we will se how to reach nested values. I want to collect address data for the user. I want a result leik the following:

```
{"firstName": "John", "lastName": "Smith", "age": 25, "streetAddress": "21 2nd Street",  "city": "New York", "state": "NY", "postalCode": "10021"}
{"firstName": "Helga", "lastName": "Smith", "age": 12, "streetAddress": "3406 34nd Street",  "city": "Los Angeles", "state": "CA", "postalCode": "12345"}
{"firstName": "Ingrid", "lastName": "Jones", "age": 45, "streetAddress": "6 Zsolt St",  "city": "Budapest", "state": "-", "postalCode": "1016"}
...
```

Flattener subclass should look like the following.

```
class Nested(Flattener):
    __field_names__ = ["firstName", "lastName", "age", "streetAddress", "city", "state", "postalCode"]

    streetAddress = Value("address.streetAddress", False)
    city = Value("address.city", False)
    state = Value("address.state", False)
    postalCode = Value("address.postalCode", False)

```

## Example - Getting list value

In this example I would like to collect phone numbers with their types. I want a result like the following:
```
{"firstName": "John", "lastName": "Smith", "age": 25, "phoneNumber": "212 555-1234", "phoneType": "home"}
{"firstName": "John", "lastName": "Smith", "age": 25, "phoneNumber": "646 555-4567", "phoneType": "fax"}
{"firstName": "Helga", "lastName": "Smith", "age": 12, "phoneNumber": "212 555-2222", "phoneType": "office"}
{"firstName": "Ingrid", "lastName": "Jones", "age": 45, , "phoneNumber": "444 515-2222", "phoneType": "mobile"}
{"firstName": "Ingrid", "lastName": "Jones", "age": 45, , "phoneNumber": "310 667-0089", "phoneType": "office"}
...
```

To reach my goal I have to define a list_path for my subclass.

```
class ListValues(Flattener):
    __field_names__ = ["firstName", "lastName", "age", "phoneNumber", "phoneType"]

    phoneNumber = ListValue(Value("phoneNumber.number", False))
    phoneType = ListValue(Value("phoneNumber.type", False))
```

You can try or play around with the examples in test/example_simple.py.