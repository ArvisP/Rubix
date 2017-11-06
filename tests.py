from app import app
import unittest

class RubixTestCase(unittest.TestCase):

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
  def test_index(self):

    # Ensure that flask was set up correctly
    def test_index(self):
      tester = app.test_client(self)
      response = tester.get('/login', content_type='html/text')
      self.assertEqual(response.status_code, 200)


  # def test_home_status_code(self):
  #   # sends HTTP GET request to the application
  #   # on the specified path
  #   result = self.app.get('/')

  #   # assert the status code of the response
  #   self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
  unittest.main()