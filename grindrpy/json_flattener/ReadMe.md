# JSON Flattener and Parser

A script for parsing, flattening and transforming json data into a normalized json output with the desired key names and value types.

### Building blocks

#### Flattener Subclass

One has to define a Flattener subclass with the __field_names__ filled out as a minimum requirement if the field names match the field names in the
original json format. __field_names__ can be a list or a set with unique string elements.


#### Field names

A set of the names which should be present as a key name in the output json.

#### Value

**Input parameters: path (string), required (boolean)**

The operator gives back the value of the field defined by the path parameter. One can set it required or optional.
If the value is required the script exits with an error when the field/path is not present in the original json or it has a null value.

In default, all the elements given in the __field_names__ will be parsed as optional with a path same as the field name.

If the field name in the original json does not match the required field name in the result json or it's a required field in the original json
or it has a complex path etc., one should customize the flattener attribute. For example:

my_field_name = Value("original.path", True)

#### Path

Path reflects on the field in the json. If the desired value is in a nested structure like customer_id in the example below the path
should be "customer_ids.customer_id".

```
{
    "custom_0": "Annual",
    "customer_ids": {
        "customer_id": "123456789"
    },
    “data_conn”: “wifi”
}
```

#### DerivedValue

**Input parameters: function (function), function_parameters (dictionary)**

When one would like to perform a transformation on one or multiple values and get the result as a new field value.


#### ListValue

**Input parameters: Value or DerivedValue**

One can have multiple ListValues within one Flattener subclass, but has to make sure that the lengths of the list results are the same.
The list elements will be joined together by their order in the normalized json.


### Examples

[Simple examples](Example_simple.md)

[Complex examples](Example_complex.md)
