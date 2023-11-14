import unittest

from api_pois.pois_all_funcs import get_facilities_and_services_from_campsite_list

class TestRulesAndRegs(unittest.TestCase):
    def test_all_data_present_type_group_st_nonelec(self):

        test_attrs = {
                "CampsiteID": "10107590",
                "FacilityID": "246096",
                "CampsiteName": "1",
                "CampsiteType": "GROUP STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107591",
                "FacilityID": "246096",
                "CampsiteName": "1A",
                "CampsiteType": "GROUP STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            }, {
                "CampsiteID": "10107592",
                "FacilityID": "246096",
                "CampsiteName": "1B",
                "CampsiteType": "GROUP STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            }
        
        result = get_facilities_and_services_from_campsite_list(test_attrs)

        self.assertEqual(
            result,
            'The campground has 3 campsites, all of which are group sites, suitable for both tents and RVs (no electric hookups provided).'
        )

    #def test_chekin_present_rest_empty(self):

if __name__ == '__main__':
    unittest.main()


campsite_data = {
                "CampsiteID": "10107590",
                "FacilityID": "246096",
                "CampsiteName": "1",
                "CampsiteType": "OOGA BOOGA",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            }, {
                "CampsiteID": "10107591",
                "FacilityID": "246096",
                "CampsiteName": "1A",
                "CampsiteType": "TENT ONLY NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            }, {
                "CampsiteID": "10107592",
                "FacilityID": "246096",
                "CampsiteName": "1B",
                "CampsiteType": "TENT ONLY NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107593",
                "FacilityID": "246096",
                "CampsiteName": "AB",
                "CampsiteType": "TENT ONLY NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107594",
                "FacilityID": "246096",
                "CampsiteName": "2",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107595",
                "FacilityID": "246096",
                "CampsiteName": "3",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107596",
                "FacilityID": "246096",
                "CampsiteName": "4",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107597",
                "FacilityID": "246096",
                "CampsiteName": "5",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": True,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107598",
                "FacilityID": "246096",
                "CampsiteName": "6",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": True,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107599",
                "FacilityID": "246096",
                "CampsiteName": "7",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107600",
                "FacilityID": "246096",
                "CampsiteName": "8",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": True,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107601",
                "FacilityID": "246096",
                "CampsiteName": "9",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": True,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107602",
                "FacilityID": "246096",
                "CampsiteName": "9A",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107603",
                "FacilityID": "246096",
                "CampsiteName": "10",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107604",
                "FacilityID": "246096",
                "CampsiteName": "11",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107605",
                "FacilityID": "246096",
                "CampsiteName": "12",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107606",
                "FacilityID": "246096",
                "CampsiteName": "13",
                "CampsiteType": "STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107607",
                "FacilityID": "246096",
                "CampsiteName": "14",
                "CampsiteType": "GROUP STANDARD NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107608",
                "FacilityID": "246096",
                "CampsiteName": "15",
                "CampsiteType": "TENT ONLY NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"
            },{
                "CampsiteID": "10107609",
                "FacilityID": "246096",
                "CampsiteName": "16",
                "CampsiteType": "TENT ONLY NONELECTRIC",
                "TypeOfUse": "Overnight",
                "Loop": "North Fork John Day",
                "CampsiteAccessible": False,
                "CampsiteLongitude": 0,
                "CampsiteLatitude": 0,
                "CreatedDate": "2021-01-12",
                "LastUpdatedDate": "2023-01-06"}
