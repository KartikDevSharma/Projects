import unittest
from src.preprocessing.code_preprocessor import CodePreprocessor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessor = CodePreprocessor()

    def test_remove_comments_python(self):
        code = """
        # This is a comment
        def func():
            '''This is a docstring'''
            return True  # inline comment
        """
        processed = self.preprocessor.remove_comments_python(code)
        self.assertNotIn('#', processed)
        self.assertNotIn("'''", processed)

    def test_standardize_variables_python(self):
        code = "def func(a, b):\n    c = a + b\n    return c"
        processed = self.preprocessor.standardize_variables_python(code)
        self.assertIn('var1', processed)
        self.assertIn('var2', processed)
        self.assertIn('var3', processed)

    def test_remove_whitespace(self):
        code = "def  func( ):\n    return  True"
        processed = self.preprocessor.remove_whitespace(code)
        self.assertEqual(processed, "def func(): return True")

if __name__ == '__main__':
    unittest.main()