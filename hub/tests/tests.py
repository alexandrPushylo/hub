from django.test import TestCase

# Create your tests here.

class YourTestClass(TestCase):
    def test_1(self):
        self.assertEqual(1,1)
    # @classmethod
    # def setUpTestData(cls):
    #     print("setUpTestData: Run once to set up non-modified data for all class methods.")
    #     pass
    #
    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    # def test_false_is_false(self):
    #     print("Method: test_false_is_false.")
    #     self.assertFalse(1>2)


    # def test_false_is_true(self):
    #     print("Method: test_false_is_true.")
    #     self.assertTrue(True)
    #
    # def test_one_plus_one_equals_two(self):
    #     self.assertEqual(1 + 1, 2)

