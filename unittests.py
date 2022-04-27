import json
import unittest

import main


class MyTestCase(unittest.TestCase):
    def test_db_connectivity(self):
        with main.api.app_context():
            result = main.display_node()
            self.assertEqual(result.status_code, 200, "error connecting to db")

    def test_engineer_query_not_existing_taskId(self):
        with main.api.app_context():
            result = main.disting_engineer_lvl("taskNotExisitng")
            self.assertEqual(result.status_code, 404, "error connecting to db")

    def test_engineer_query_correct_result(self):
        with main.api.app_context():
            result = main.disting_engineer_lvl("TASK1001")
            correctRes = [{"engineer_skill_level": 3}, {"engineer_skill_level": 1}, {"engineer_skill_level": 5}]
            obj = json.loads(result.data)
            self.assertEqual(obj['result'], correctRes, "error connecting to db")


if __name__ == '__main__':
    unittest.main()
