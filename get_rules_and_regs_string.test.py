import unittest

from api_pois.pois_all_funcs import format_rules_and_regs


class TestRulesAndRegs(unittest.TestCase):
    def test_all_attributes_present(self):
        test_attrs = {
            "CampfireAllowed": "Yes",
            "CampsiteSize": "Single",
            "CheckIn": "12:00 PM",
            "CheckOut": "12:00 PM",
            "MaxPeople": "6",
            "MaxVehicles": "2"
        }

        result = format_rules_and_regs(test_attrs)

        self.assertEqual(
            result,
            'Check-in time is 12:00 PM, check-out is at 12:00 PM. The maximum number of people is 6 per Single campsite. The maximum number of vehicles is 2 per Single campsite.'
        )

    def test_chekin_present_rest_empty(self):
        test_attrs = {
            "CampfireAllowed": "",
            "CampsiteSize": "",
            "CheckIn": "12:00 PM",
            "CheckOut": "12:00 PM"
        }

        result = format_rules_and_regs(test_attrs)

        self.assertEqual(
            result,
            'Check-in time is 12:00 PM, check-out is at 12:00 PM.'
        
        )

if __name__ == '__main__':
    unittest.main()
