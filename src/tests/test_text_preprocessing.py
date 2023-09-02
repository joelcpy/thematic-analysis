import unittest
from nltk.corpus import stopwords

from preprocessing import *
stop_words = stopwords.words('english')

# Define the tests for preprocessing.py
class TestPreprocessingFunctions(unittest.TestCase):

    def test_remove_stopwords(self):
        # Define a sample token list with stopwords and expected output
        token_list = ["this", "is", "a", "sample", "text"]
        expected_output = ["sample", "text"]
        
        # Call the function from preprocessing.py
        result = remove_stopwords(token_list)
        
        # Assert if the result matches the expected output
        self.assertEqual(result, expected_output)

    # Test for the make_bigrams function
    def test_make_bigrams(self):
        # Define a sample token list and expected output
        token_list = ["this", "is", "sample", "text","lender", "placed"]
        expected_output= ["this", "is", "sample", "text","lender_placed"]
        # Call the function from preprocessing.py
        result = make_bigrams(token_list)
        
        # Assert if the result is a list
        self.assertIsInstance(result, list), f"Expected list, but got {type(result)}"
        # Assert if the result matches the expected output
        self.assertEqual(result, expected_output)

    # Test for the lemmatization function
    def test_lemmatization(self):
        # Define a sample token list and expected output
        token_list = ["running", "faster"]
        expected_output= ['run', 'fast']

        # Call the function from preprocessing.py
        result = lemmatization(token_list)
        
        # Assert if the result matches the expected output
        self.assertEqual(result, expected_output)
    
    # Test for the preprocessing_text function
    def test_preprocessing_text(self):
        # Define a sample text and expected output
        text = "<html>This is a sample text! With punctuations and numbers 123.</html>"
        expected_output = ['text', 'punctuation', 'number', 'html']

        # Call the function from preprocessing.py
        result = preprocessing_text(text)
        
        # Assert if the result matches the expected output
        self.assertEqual(result, expected_output)
        # Assert if the result is a list
        self.assertIsInstance(result, list), f"Expected list, but got {type(result)}"
