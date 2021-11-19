import unittest
from pathlib import Path
import os, sys
import src.compile_word_counts as cwc
import src.compute_pony_lang as cpl
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
    def test_task1(self):
        print("\nRUNNING TEST 1 FOR TASK 1")
        print("Ensure word count output matches true word count")
        # Clean the data
        data, words = cwc.clean(self.mock_dialog, threshold=1)
        # Count the words
        pony_word_count = cwc.word_count(data, words)
        # Load true count as dictionary
        with open(self.true_word_counts, 'r') as f:
            true_count = json.loads(f.read())
        
        self.assertDictEqual(pony_word_count, true_count)
        print("OK")

    def test_task2(self):
        print("\nRUNNING TEST 2 FOR TASK 2")
        print('Ensure pony langugage output matches true pony language')
        # Compute tf_idf scores, returns the json format output
        outputs = cpl.compute_score(self.true_word_counts, 2)

        # Load true tf_idf from file
        with open(self.true_tf_idfs, 'r') as f:
            true_outputs = json.load(f)

        self.assertDictEqual(true_outputs, outputs)
        print("OK")
    
if __name__ == '__main__':
    unittest.main()
