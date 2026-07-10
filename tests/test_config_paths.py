import os
import unittest

from src.config import RECOMMENDER_DATASET, MASTER_JOBS


class ConfigPathTests(unittest.TestCase):
    def test_processed_data_files_exist(self):
        self.assertTrue(os.path.exists(RECOMMENDER_DATASET), RECOMMENDER_DATASET)
        self.assertTrue(os.path.exists(MASTER_JOBS), MASTER_JOBS)


if __name__ == "__main__":
    unittest.main()
