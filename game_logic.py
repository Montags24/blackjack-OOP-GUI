import os
from random import choice


# Dictionary that links cards to their value
card_dict = {
    "1": 10, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "J": 10, "Q": 10, "K": 10, "A": 11, "r": 0
}


class Deck:
    """Simulates a deck of cards that can deal"""
    def __init__(self, n_of_decks):
        # Create a deck list based off .png names in cards folder.
        self.deck = []
        deck_list = os.listdir("./cards")
        for i in range(n_of_decks):
            self.deck.extend(deck_list)

    def deal_card(self):
        # Function that removes a card from the deck and returns it, simulating a dealt card.
        card = choice(self.deck)
        while card == "reverse.png":
            card = choice(self.deck)
        self.deck.remove(card)
        return card


def get_value(card):
    # Returns the value of the card
    return card_dict[card[0]]


class Dealer:
    """Simulates a dealer"""
    def __init__(self):
        self.cards = []
        self.score = 0
        self.aces = 0
        self.result = 0

    def update(self, card):
        # Updates the hand of the player/dealer and amends their score.
        self.cards.append(card)
        self.score += get_value(card)

    def is_bust(self):
        aces = 0
        # Check if player goes bust
        if self.score > 21:
            for card in self.cards:
                if card == "AC.png" or card == "AD.png" or card == "AS.png" or card == "AH.png":
                    aces += 1
                    for i in range(aces-self.aces):
                        self.score -= 10
                        self.aces += 1
                        return False
            return True

    def is_blackjack(self):
        # Function that returns true if player has blackjack
        total = get_value(self.cards[0]) + get_value(self.cards[1])
        if total == 21:
            self.result = 1.5
            return True

    def win_status(self, dealer_score, player_score):
        # Function that updates self.result based on outcome of game
        if player_score < dealer_score <= 21:
            self.result = 0
            return "Player loses!"
        elif dealer_score >= 17 and dealer_score == player_score:
            self.result = 1
            return "It's a draw!"
        else:
            return "Player Wins!"

    def reset(self):
        # Function that resets cards in hand and score
        self.cards = []
        self.score = 0

    def hit(self, card):
        # Function that updates card in hand and checks if player busts
        self.update(card)
        if self.is_bust():
            return True

    def flip_card(self, card):
        # Function that replaces the first instance of reverse.png in game cards to dealt card
        if "reverse.png" in self.cards:
            index = self.cards.index("reverse.png")
            self.cards[index] = card
        return self.cards

    def check_double_ace(self):
        # Function that checks for double ace in hand
        count = 0
        for card in self.cards:
            if card == "AC.png" or card == "AD.png" or card == "AS.png" or card == "AH.png":
                count += 1
        if count == 2:
            return True


class Player(Dealer):
    """Player class that inherits attributes from dealer"""
    def __init__(self):
        super().__init__()
        self.bet = 0
        self.bank = 200

    def bet_money(self, bet):
        # Function that allows user to bet money in the game
        if self.bank <= 0:
            pass
        else:
            self.bet += bet
            self.bank -= bet

    def update_bank(self):
        # Function that updates bank based on the outcome of the game
        result = (self.result * self.bet)
        self.bank += result
