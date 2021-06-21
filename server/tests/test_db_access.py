from unittest import TestCase
from db_access import DBAccess


class TestDBAccess(TestCase):
    def setUp(self):
        self.database = DBAccess.getInstance()
        self.database.database = self.database.mongo_client.test_db
        self.database.db_name = "test_db"

        self.program1 = {"disease_funds": "Cystic Fibrosis Treatments",
                         "treatments_covered": "Accuneb, Acetylcysteine Sol",
                         "status": "Open",
                         "max_award_level": "$15,000"}
        self.program2 = {"disease_funds": "Cutaneous T-Cell Lymphoma",
                         "treatments_covered": "Alferon, Aristocort",
                         "status": "Closed",
                         "max_award_level": "$4,800"}

        self.database.insert_programs([self.program1, self.program2])

    def test_insert_programs(self):
        programs = self.database.fetch_programs()
        programs[0].pop('_id', None)
        programs[1].pop('_id', None)
        self.assertDictEqual({"disease_funds": "Cystic Fibrosis Treatments",
                              "treatments_covered": "Accuneb, Acetylcysteine Sol",
                              "status": "Open",
                              "max_award_level": "$15,000"}, programs[0])
        self.assertDictEqual({"disease_funds": "Cutaneous T-Cell Lymphoma",
                              "treatments_covered": "Alferon, Aristocort",
                              "status": "Closed",
                              "max_award_level": "$4,800"}, programs[1])

    def test_fetch_programs(self):
        programs = self.database.fetch_programs()
        programs[0].pop('_id', None)
        programs[1].pop('_id', None)
        self.assertDictEqual({"disease_funds": "Cystic Fibrosis Treatments",
                              "treatments_covered": "Accuneb, Acetylcysteine Sol",
                              "status": "Open",
                              "max_award_level": "$15,000"}, programs[0])
        self.assertDictEqual({"disease_funds": "Cutaneous T-Cell Lymphoma",
                              "treatments_covered": "Alferon, Aristocort",
                              "status": "Closed",
                              "max_award_level": "$4,800"}, programs[1])

    def test_update_program(self):
        self.database.update_program({'disease_funds': "Cystic Fibrosis Treatments"},
                                     {"status": "Closed",
                                      "max_award_level": "$18,500"}
                                     )
        updated_program = self.database.fetch_programs()[0]
        self.assertDictEqual({"disease_funds": "Cystic Fibrosis Treatments",
                              "treatments_covered": "Accuneb, Acetylcysteine Sol",
                              "status": "Closed",
                              "max_award_level": "$18,500"}, updated_program)

    def tearDown(self) -> None:
        self.database.drop_db()
