import unittest
import json
from grindrpy.json_flattener.flattener import Flattener
from grindrpy.json_flattener.value import Value, DerivedValue, ListValue


class FlattenerTest(unittest.TestCase):

    def test_simple_json_flattening(self):
        test_json = dict(id="XXXXX",
                         name="XYZ",
                         address="2020 45th St",
                         zip="99999")

        class SimpleJsonFlattener(Flattener):
            __field_names__ = {"id", "name", "zip"}

        self.assertEqual(list(SimpleJsonFlattener().flatten(test_json)),
                         [{"id": "XXXXX", "name": "XYZ", "zip": "99999"}])

    def test_renaming_fields(self):
        test_json = dict(id="XXXXX",
                         name="XYZ",
                         address="2020 45th St",
                         zip="99999")

        class SimpleJsonFlattener(Flattener):
            __field_names__ = {"id", "name", "zip"}

            id = Value("name", False)
            name = Value("id", False)

        self.assertEqual(list(SimpleJsonFlattener().flatten(test_json)),
                         [{"name": "XXXXX", "id": "XYZ", "zip": "99999"}])

    def test_list_flattening(self):
        test_json = dict(id="XXXXX",
                         name="XYZ",
                         address="2020 45th St",
                         zip="99999",
                         results=[1, 2],
                         other_list=[3, 4, 5])

        class ListJsonFlattener(Flattener):
            __field_names__ = {"id", "name", "zip", "results"}

            results = ListValue(Value("results", False))

        self.assertEqual(list(ListJsonFlattener().flatten(test_json)),
                         [{"id": "XXXXX", "name": "XYZ", "zip": "99999", "results": 1},
                          {"id": "XXXXX", "name": "XYZ", "zip": "99999", "results": 2}])

    def test_failing_mutilist_flattening(self):
        test_json = dict(id="XXXXX",
                         name="XYZ",
                         address="2020 45th St",
                         zip="99999",
                         results=[1, 2],
                         other_list=[3, 4, 5])

        class ListJsonFlattener(Flattener):
            __field_names__ = ["id", "name", "zip", "results", "other_list"]

            results = ListValue(Value("results", False))

        with self.assertRaises(ValueError): list(ListJsonFlattener().flatten(test_json))

    def test_derived_flattening(self):
        test_json = dict(id="XXXXX",
                         name="XYZ",
                         address="2020 45th St",
                         zip="99999",
                         results=[1, 2, 3],
                         other_list=[3, 4, 5])

        def func(results, other_list): return [i[0] + i[1] for i in zip(results, other_list)]

        class ListJsonFlattener(Flattener):
            __field_names__ = ["id", "name", "zip", "results_other_list"]

            results_other_list = ListValue(DerivedValue(func, dict(results=Value("results", False),
                                                         other_list=Value("other_list", False))))

        self.assertEqual(list(ListJsonFlattener().flatten(test_json)),
                         [{"id": "XXXXX", "name": "XYZ", "zip": "99999", "results_other_list": 4},
                          {"id": "XXXXX", "name": "XYZ", "zip": "99999", "results_other_list": 6},
                          {"id": "XXXXX", "name": "XYZ", "zip": "99999", "results_other_list": 8}])

    def test_complex_flattening(self):

        class Lines(Flattener):
            __field_names__ = {"object", "my_field_name", "date", "plan_id", "period_start", "period_end"}

            my_field_name = Value("amount_due", False)
            plan_id = ListValue(Value("lines.data.plan.id", False))
            period_start = ListValue(Value("lines.data.period.start", False))
            period_end = ListValue(Value("lines.data.period.end", False))


        test_json = """{
          "object": "invoice",
          "amount_due": 919191919191,
          "application_fee": null,
          "attempt_count": 1,
          "attempted": true,
          "closed": true,
          "currency": "currency",
          "date": 1427412009,
          "description": null,
          "discount": null,
          "ending_balance": 0,
          "forgiven": false,
          "lines": {
            "data": [
              {
                "object": "line_item",
                "amount": 99999999,
                "currency": "currency",
                "description": null,
                "discountable": true,
                "livemode": true,
                "metadata": {
                },
                "period": {
                  "start": 1,
                  "end": 15
                },
                "plan": {
                  "id": "plan_id",
                  "object": "plan",
                  "amount": 99999999,
                  "created": 1500388587,
                  "currency": "currency",
                  "interval": "interval",
                  "interval_count": 1,
                  "livemode": false,
                  "metadata": {
                  },
                  "name": "PLAN A",
                  "statement_descriptor": null,
                  "trial_period_days": null
                },
                "proration": false,
                "quantity": 1,
                "subscription": null,
                "type": "subscription"
              },
              {
                "object": "line_item",
                "amount": 11111111,
                "currency": "currency",
                "description": null,
                "discountable": true,
                "livemode": true,
                "metadata": {
                },
                "period": {
                  "start": 1521039614,
                  "end": 1552575614
                },
                "plan": {
                  "id": "plan_id",
                  "object": "plan",
                  "amount": 999,
                  "created": 1500388587,
                  "currency": "currency",
                  "interval": "interval",
                  "interval_count": 1,
                  "livemode": false,
                  "metadata": {
                  },
                  "name": "PLAN A",
                  "statement_descriptor": null,
                  "trial_period_days": null
                },
                "proration": false,
                "quantity": 1,
                "subscription": null,
                "type": "subscription"
              }
            ],
            "total_count": 1,
            "object": "list"
          }
        }"""

        test_json = json.loads(test_json)

        self.assertEqual(list(Lines().flatten(test_json)),
                         [{"object": "invoice", "my_field_name": 919191919191, "date": 1427412009, "plan_id": "plan_id", "period_start": 1, "period_end": 15},
                          {"object": "invoice", "my_field_name": 919191919191, "date": 1427412009, "plan_id": "plan_id", "period_start": 1521039614, "period_end": 1552575614}
                          ])


