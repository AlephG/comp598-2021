import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.clean import load_json, verify_title, standardize_dt, verify_author, cast_totalcount, parse_tags
import json

class CleanTest(unittest.TestCase):
    def setUp(self):
        self.entries = []
        for i in range(6):
            self.entries.append(os.path.join(parentdir, 'test','fixtures', f'test_{i+1}.json'))
   
    # Test 6
    def test_6(self):
        print('\nRunning test 6: Verify that tags are parsed correctly')
        data = load_json(self.entries[5])
        entry = parse_tags(data[0])
        self.assertEqual(len(entry['tags']), 4)
        print('OK')

    # Test 5
    def test_5(self):
         print('\nRunning test 5: Remove entries for which \'total_count\' cannot be cast to int')
         data = load_json(self.entries[4])
         entry = cast_totalcount(data[0])
         self.assertIsNone(entry)
         print('OK')

    # Test 4
    def test_4(self):
        print('\nRunning test 4: Remove entries with inppropriate \'author\' field')
        data = load_json(self.entries[3])
        entry = verify_author(data[0])
        self.assertIsNone(entry)
        print('OK')


    # Test 3
    def test_3(self):
        print('\nRunning test 3: Validate JSON entries')
        data = load_json(self.entries[2])
        self.assertFalse(data)
        print('OK')

    # Test 2
    def test_2(self):
        print('\nRunning test 2: Verify that entries with non-ISO compliant datetimes are removed')
        data = load_json(self.entries[1])
        entry = standardize_dt(data[0])
        self.assertIsNone(entry)
        print('OK')


    # Test 1
    def test_1(self):
        print('\nRunning test 1: Verify that entries with missing \'title\' or \'title_text\' fields are removed')
        data = load_json(self.entries[0])
        entry = verify_title(data[0])
        self.assertIsNone(entry)
        print('OK')

if __name__ == '__main__':
    unittest.main()
