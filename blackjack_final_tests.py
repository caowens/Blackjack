from importlib import reload
from unittest import TestCase, main
from unittest.mock import patch
import io
import sys

def print_value(question, answer):
    print(question + answer)
    return answer

def run_test(user_cards, answers, dealer_cards, randint_mock, input_mock, imported):
    """
    Mocks randint and runs function with mock

    Args:
      randint_mock - patched random.randint()
      cards - desired input for random.randint()
      input_mock - patched bultins.input()
      answers - desired input for builtins.input()
      imported - whether module was imported already; always pass in True for your tests
    """
    answers.reverse() # reverses answers so can pop off list
    randint_mock.side_effect = user_cards + dealer_cards # set randint calls to cards
    input_mock.side_effect = \
        lambda question: print_value(question, answers.pop()) # print input question along with given answer

    # Save printed output into variable so can return it to compare in test
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    import blackjack_final
    if imported:
        reload(blackjack_final)
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    return output # return printed statements in student-run code

class BlackjackPart6Test(TestCase):

    @patch('random.randint')
    @patch('builtins.input')
    def test_0_example(self, input_mock, randint_mock):
        '''
        Both the dealer and user receive cards that end up with a hand less than 21.
        The dealer wins by having a higher hand than the user.

        This does not count as one of your tests.
        '''

        # Pass in True as the last argument in all your tests
        output = run_test([3, 5, 8], ['y', 'n'], [3, 5, 10], randint_mock, input_mock, False)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 3\n" \
                   "Drew a 5\n" \
                   "You have 8. Hit (y/n)? y\n" \
                   "Drew a 8\n" \
                   "You have 16. Hit (y/n)? n\n" \
                   "Final hand: 16.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 3\n" \
                   "Drew a 5\n" \
                   "Drew a 10\n" \
                   "Final hand: 18.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Dealer wins!\n"
        self.assertEqual(output, expected)

    # WRITE ALL YOUR TESTS BELOW. Do not delete this line.
    
    @patch('random.randint')
    @patch('builtins.input')
    def test_user_win(self, input_mock, randint_mock):
        # if user and dealer gets under 21 and user is higher
        output = run_test([7, 1], ['n'], [6, 1, 2], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 7\n" \
                   "Drew a Ace\n" \
                   "You have 18. Hit (y/n)? n\n" \
                   "Final hand: 18.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 6\n" \
                   "Drew a Ace\n" \
                   "Drew a 2\n" \
                   "Final hand: 19.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Dealer wins!\n"
        self.assertEqual(output, expected)
        
        # if user gets black jack and dealer busts
        output = run_test([1, 2, 8], ['y', 'n'], [2, 2, 10, 11], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a Ace\n" \
                   "Drew a 2\n" \
                   "You have 13. Hit (y/n)? y\n" \
                   "Drew a 8\n" \
                   "Final hand: 21.\n" \
                   "BLACKJACK!\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 2\n" \
                   "Drew a 2\n" \
                   "Drew a 10\n" \
                   "Drew a Jack\n" \
                   "Final hand: 24.\n" \
                   "BUST.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "You win!\n"
        self.assertEqual(output, expected)
        
        # if user gets under 21 and dealer busts
        output = run_test([7, 9], ['n'], [1, 2, 11], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 7\n" \
                   "Drew a 9\n" \
                   "You have 16. Hit (y/n)? n\n" \
                   "Final hand: 16.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a Ace\n" \
                   "Drew a 2\n" \
                   "Drew a Jack\n" \
                   "Final hand: 23.\n" \
                   "BUST.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "You win!\n"
        self.assertEqual(output, expected)

        # if user gets blackjack and dealer under
        output = run_test([10, 1], ['n'], [6, 10, 2], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 10\n" \
                   "Drew a Ace\n" \
                   "You have 21. Hit (y/n)? n\n" \
                   "Final hand: 21.\n" \
                   "BLACKJACK!\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 6\n" \
                   "Drew a 10\n" \
                   "Drew a 2\n" \
                   "Final hand: 18.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "You win!\n"
        self.assertEqual(output, expected)
        
    @patch('random.randint')
    @patch('builtins.input')
    def test_dealer_win(self, input_mock, randint_mock):
        # dealer gets highest score but both under 21
        output = run_test([7, 12], ['n'], [6, 11, 4], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 7\n" \
                   "Drew a Queen\n" \
                   "You have 17. Hit (y/n)? n\n" \
                   "Final hand: 17.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 6\n" \
                   "Drew a Jack\n" \
                   "Drew a 4\n" \
                   "Final hand: 20.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Dealer wins!\n"
        self.assertEqual(output, expected)
        
        # dealer gets blackjack and user gets less than 21 
        output = run_test([9, 4], ['n'], [1, 10], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 9\n" \
                   "Drew a 4\n" \
                   "You have 13. Hit (y/n)? n\n" \
                   "Final hand: 13.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a Ace\n" \
                   "Drew a 10\n" \
                   "Final hand: 21.\n" \
                   "BLACKJACK!\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Dealer wins!\n"
        self.assertEqual(output, expected)
        
        # user busts but dealer doesn't
        output = run_test([2, 10, 2, 13], ['y', 'y'], [9, 7, 2], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 2\n" \
                   "Drew a 10\n" \
                   "You have 12. Hit (y/n)? y\n" \
                   "Drew a 2\n" \
                   "You have 14. Hit (y/n)? y\n" \
                   "Drew a King\n" \
                   "Final hand: 24.\n" \
                   "BUST.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 9\n" \
                   "Drew a 7\n" \
                   "Drew a 2\n" \
                   "Final hand: 18.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Dealer wins!\n"
        self.assertEqual(output, expected)

        #Dealer blackjack and user busts
        output = run_test([9, 4, 10], ['y'], [1, 10], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 9\n" \
                   "Drew a 4\n" \
                   "You have 13. Hit (y/n)? y\n" \
                   "Drew a 10\n" \
                   "Final hand: 23.\n" \
                   "BUST.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a Ace\n" \
                   "Drew a 10\n" \
                   "Final hand: 21.\n" \
                   "BLACKJACK!\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Dealer wins!\n"
        self.assertEqual(output, expected)
        
    @patch('random.randint')
    @patch('builtins.input')
    def test_tie(self, input_mock, randint_mock):
        # both user and dealer busts
        output = run_test([7, 9, 13], ['y'], [5, 8, 12], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a 7\n" \
                   "Drew a 9\n" \
                   "You have 16. Hit (y/n)? y\n" \
                   "Drew a King\n" \
                   "Final hand: 26.\n" \
                   "BUST.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a 5\n" \
                   "Drew a 8\n" \
                   "Drew a Queen\n" \
                   "Final hand: 23.\n" \
                   "BUST.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Tie.\n"
        self.assertEqual(output, expected)
        
        # both user and dealer blackjack
        output = run_test([1, 13], ['n'], [13, 1], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a Ace\n" \
                   "Drew a King\n" \
                   "You have 21. Hit (y/n)? n\n" \
                   "Final hand: 21.\n" \
                   "BLACKJACK!\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a King\n" \
                   "Drew a Ace\n" \
                   "Final hand: 21.\n" \
                   "BLACKJACK!\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Tie.\n"
        self.assertEqual(output, expected)
        
        # both user and dealer get the same value under 21
        output = run_test([11, 12], ['n'], [12, 11], randint_mock, input_mock, True)
        expected = "-----------\n" \
                   "YOUR TURN\n" \
                   "-----------\n" \
                   "Drew a Jack\n" \
                   "Drew a Queen\n" \
                   "You have 20. Hit (y/n)? n\n" \
                   "Final hand: 20.\n" \
                   "-----------\n" \
                   "DEALER TURN\n" \
                   "-----------\n" \
                   "Drew a Queen\n" \
                   "Drew a Jack\n" \
                   "Final hand: 20.\n" \
                   "-----------\n" \
                   "GAME RESULT\n" \
                   "-----------\n" \
                   "Tie.\n"
        self.assertEqual(output, expected)
        
    # Make sure all your test functions start with test_ 
    # Follow indentation of test_example

    # Write all your tests above this. Do not delete this line.

if __name__ == '__main__':
    main()
