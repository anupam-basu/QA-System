import unittest
from qa1 import *  # Replace with your actual module name

class TestYourFunctions(unittest.TestCase):

    def test_convert_to_past_tense(self):
        self.assertEqual(convert_to_past_tense('rise'), 'rose')
        self.assertEqual(convert_to_past_tense('fall'), 'fell')
        self.assertEqual(convert_to_past_tense('open'), 'opened')
        # Add more test cases for other verbs

    def test_get_synoym_list(self):
        self.assertEqual(get_synoym_list('rise'), ["up", "risen", "rise", "rose", "climb", "climbed", "soar", "soared"])
        self.assertEqual(get_synoym_list('drop'), ["drop", "fall", "down", "plummet", "decline", "plunged", "fell"])
        self.assertEqual(get_synoym_list('close'), ["closed", "close"])
        self.assertEqual(get_synoym_list('open'), ["open", "opened"])
        self.assertFalse(get_synoym_list('nonexistent_word'))

    def test_q_type(self):
        passage = "Your passage is here."  # Replace with an actual passage
        # Test cases for question types
        question_1 = "Did it rise?"
        question_2 = "What is the value?"
        question_3 = "Invalid question"
        
        # You can create more test cases for different question types and scenarios
        
        # Mocking stdout to capture printed output
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            q_type(question_1, passage)
        self.assertIn("Expected Output Text", f.getvalue())  # Replace with expected output
        
        # You can check other aspects of the output as well
        
    # Add more test cases for other functions as needed

if __name__ == '__main__':
    unittest.main()
