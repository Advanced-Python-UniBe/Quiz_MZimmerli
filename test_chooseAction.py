from Quiz import *
import unittest
from unittest.mock import patch

class TestAction(unittest.TestCase):
    ''' Since it is hard to make an assertion for a function without a returnvalue, i made use of the mock library so i could check if any of the action-functions has been called '''
    @patch('Quiz.add_questions')
    @patch('Quiz.print_questions')
    @patch('Quiz.take_quiz')
    @patch('Quiz.review_answers')
    @patch('Quiz.plot_scores')
    @patch('Quiz.logOut')
    def test_action_chosen(self, mock_logOut, mock_plot_scores, mock_review_answers, mock_take_quiz, mock_print_questions,mock_add_questions):
        self.assertFalse(mock_add_questions.called)
        chooseAction('0',action_functions = [mock_add_questions, mock_print_questions, mock_take_quiz,mock_review_answers, mock_plot_scores, mock_logOut])
        self.assertTrue(mock_add_questions.called)

        self.assertFalse(mock_print_questions.called)
        chooseAction('1',action_functions = [mock_add_questions, mock_print_questions, mock_take_quiz,mock_review_answers, mock_plot_scores, mock_logOut])
        self.assertTrue(mock_print_questions.called)

        self.assertFalse(mock_take_quiz.called)
        chooseAction('2',action_functions = [mock_add_questions, mock_print_questions, mock_take_quiz,mock_review_answers, mock_plot_scores, mock_logOut])
        self.assertTrue(mock_take_quiz.called)

        self.assertFalse(mock_review_answers.called)
        chooseAction('3',action_functions = [mock_add_questions, mock_print_questions, mock_take_quiz,mock_review_answers, mock_plot_scores, mock_logOut])
        self.assertTrue(mock_review_answers.called)

        self.assertFalse(mock_plot_scores.called)
        chooseAction('4',action_functions = [mock_add_questions, mock_print_questions, mock_take_quiz,mock_review_answers, mock_plot_scores, mock_logOut])
        self.assertTrue(mock_plot_scores.called)

        self.assertFalse(mock_logOut.called)
        chooseAction('5',action_functions = [mock_add_questions, mock_print_questions, mock_take_quiz,mock_review_answers, mock_plot_scores, mock_logOut])
        self.assertTrue(mock_logOut.called)

    def test_input_value(self):
        self.assertRaises(TypeError, chooseAction,'4.4')
        self.assertRaises(TypeError, chooseAction,'hello')
        self.assertRaises(TypeError, chooseAction,'-3')
        self.assertRaises(TypeError, chooseAction,'')

    def test_valid_action(self):
        self.assertRaises(IndexError, chooseAction, '6')
        
           
if __name__ == '__main__':
    unittest.main()