from app import app
import unittest

class RubixTests(unittest.TestCase):

  # init logic for rest of test suite declared in test module
  # code that is execeuted before all tests in one test run
  @classmethod
  def setUpClass(cls):
    pass

  # clean up logic for test suite delcared in the test module
  # code that is executed after all tests in one test run
  @classmethod
  def tearDownClass(cls):
    pass

  # init logic
  # code that is executed before each test
  def setUp(self):
    pass

  # clean up logic
  # code that is executed after each test
  def tearDown(self):
    pass

  # test method
  def test_home_status_code(self):
    # sends HTTP GET request to the application
    # on the specified path
    result = self.app.get('/')

    # assert the status code of the response
    self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
  unittest.main()