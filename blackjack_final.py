# DO NOT REMOVE
from deck import print_card, draw_card, print_header, draw_starting_hand, print_end_turn_status, print_end_game_status

# User turn
# draw a starting hand for the user and store it into a variable
user_hand = draw_starting_hand("YOUR")

# allow the user to see hand value and decide to hit or stand
response = input('You have ' + str(user_hand) + '. Hit (y/n)? ')

# if the user's hand is less than 21, then they can keep deciding to hit
while user_hand < 21 and response == 'y':
    user_hand = user_hand + draw_card()
    if user_hand < 21:
        response = input('You have ' + str(user_hand) + '. Hit (y/n)? ')

# output the user's final hand and if black jack, bust or neither
print_end_turn_status(user_hand)

# Dealer turn
# draw a starting hand for the dealer and store it into a variable
dealer_hand = draw_starting_hand("DEALER")

# per dealer rules, as long as the dealer hand is 17 or less, they keep drawing cards
while dealer_hand <= 17:
    dealer_hand += draw_card()

# output dealer's final hand and if black jack, bust or neither
print_end_turn_status(dealer_hand)

# compare user's and dealer's final hand and who won, lost, or tied
print_end_game_status(user_hand, dealer_hand)