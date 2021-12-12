from Quiz import *
import unittest
from unittest.mock import patch

class TestAction(unittest.TestCase):
    ''' Since it is hard to make an assertion for a function without a returnvalue, i made use of the mock library so i could check if any of the action-functions has been called '''
    @patch('Quiz.add_questions')
    @patch('Quiz.print_questions')
    @patch('Quiz.take_quiz')
    @patch('Quiz.quit')
    def test_action_chosen(self, mock_quit,mock_take_quiz,mock_print_questions,mock_add_questions):
        self.assertFalse(mock_add_questions.called)
        chooseAction('0')
        self.assertTrue(mock_add_questions.called)

        self.assertFalse(mock_print_questions.called)
        chooseAction('1')
        self.assertTrue(mock_print_questions.called)

        self.assertFalse(mock_take_quiz.called)
        chooseAction('2')
        self.assertTrue(mock_take_quiz.called)

        self.assertFalse(mock_quit.called)
        chooseAction('3')
        self.assertTrue(mock_quit.called)

    def test_input_value(self):
        self.assertRaises(TypeError, chooseAction,'4.4')
        self.assertRaises(TypeError, chooseAction,'hello')
        self.assertRaises(TypeError, chooseAction,'-3')
        self.assertRaises(TypeError, chooseAction,'')

    def test_valid_action(self):
        self.assertRaises(IndexError, chooseAction, '4')
        
           
if __name__ == '__main__':
    unittest.main()