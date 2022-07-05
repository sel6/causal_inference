
import os
import sys
import unittest
import pandas as pd

sys.path.append(os.path.abspath(os.path.join('../scripts')))

class TestFiles(unittest.TestCase):

  def test_read_csv(self):
    df = US.read_csv('test.csv')
    df1 = pd.read_csv('test.csv')
    self.assertEqual(df.shape, df1.shape)
    
    
if __name__ == '__main__':
  unittest.main()
