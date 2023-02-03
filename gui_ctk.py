import customtkinter
from tkinter import *
from game_logic import Deck, Player, Dealer

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# Game constants
TABLE_COLOUR = "#2C6E49"
CLOTH_COLOUR = "#d68c45"
DARK_COLOUR = "#f77f00"
FONT = ("Arial", 15, "bold")
CARD_PATH = "./cards/"


class GuiCtk(customtkinter.CTk):
    """This class activates the GUI in which the game blackjack will be played"""
    def __init__(self):
        super().__init__()

        self.title("Black Jack")
        self.config(padx=20, pady=20, bg=TABLE_COLOUR, highlightthickness=0)

        # Initialise game objects
        self.player = Player()
        self.dealer = Dealer()
        self.game = Dealer()
        self.deck = Deck(1)
        self.result = ""

        # Initialise labels
        self.player_bank_label = Label(text=f"Bet: £{self.player.bet}\n\nBank: £{self.player.bank}", bg=TABLE_COLOUR,
                                       font=FONT, width=10)
        self.game_over_label = Label(text=f"GAME OVER\n{self.player.win_status(self.dealer.score, self.player.score)}",
                                     font=FONT, bg=TABLE_COLOUR)

        self.player_label = Label(text=f"Dealer Score: {self.dealer.score}", font=FONT, bg=TABLE_COLOUR)
        self.dealer_label = Label(text=f"Player Score: {self.player.score}", font=FONT, bg=TABLE_COLOUR)

        # Place label
        self.player_bank_label.grid(column=0, row=5)

        # Initialise buttons
        self.bet_button = customtkinter.CTkButton(master=self, text="Bet £10", command=self.bet,
                                                  hover_color=DARK_COLOUR, width=100)
        self.deal_button = customtkinter.CTkButton(master=self, text="Deal",
                                                   command=self.deal_cards, hover_color=DARK_COLOUR, width=100)
        self.hit_button = customtkinter.CTkButton(master=self, text="Hit",
                                                  command=self.hit, hover_color=DARK_COLOUR, width=100)
        self.play_again_button = customtkinter.CTkButton(master=self, text="Play Again", command=self.reset_game,
                                                         hover_color=DARK_COLOUR, width=100)
        self.stand_button = customtkinter.CTkButton(master=self, text="Stand",
                                                    command=self.stand, hover_color=DARK_COLOUR, width=100)

        # Place buttons
        self.bet_button.grid(column=1, row=5)
        self.deal_button.grid(column=2, row=5)

        # Initialise image holders for cards - p for player, d for dealer, g for game
        self.p1 = None
        self.p2 = None
        self.d1 = None
        self.d2 = None
        self.g1 = None
        self.g2 = None
        self.g3 = None
        self.g4 = None

        self.reset_game()

    def deal_cards(self):
        # Activate labels and buttons
        self.dealer_label.grid(column=1, row=1, columnspan=2)
        self.player_label.grid(column=1, row=3, columnspan=2)
        self.player_bank_label.grid(column=0, row=4)
        self.hit_button.grid(column=1, row=5)
        self.stand_button.grid(column=2, row=5)

        # Remove bet button
        self.bet_button.grid_forget()
        self.deal_button.grid_forget()

        self.initialise_game()

    def initialise_game(self):
        # Deal initial cards to player and dealer
        [player_cards, dealer_cards, game_cards] = self.initial_deal()

        # Check if player has double ace
        if self.player.check_double_ace():
            self.player.score = 12

        self.update_table(player_cards, dealer_cards, game_cards)

    def bet(self):
        # Command for the bet button
        self.player.bet_money(10)
        self.player_bank_label.config(text=f"Bet: £{self.player.bet}\n\nBank: £{self.player.bank}")

    def hit(self):
        # Command for the hit button
        card = self.deck.deal_card()
        # Show game result if player busts
        is_bust = self.player.hit(card)
        if is_bust:
            self.player.result = 0
            self.play_again()
            self.game_over_label.config(text="GAME OVER\nPlayer busts!")
            self.game_over_label.grid(column=3, row=4)
        # Add card to middle of board
        self.game.cards.append(self.game.flip_card(card))
        self.update_table(self.player.cards, self.dealer.cards, self.game.cards)

    def play_again(self):
        # Activate play again button
        self.play_again_button.grid(column=3, row=5)
        # Disable hit and stand buttons
        self.hit_button.grid_forget()
        self.stand_button.grid_forget()

    def stand(self):
        # Dealer reveals their card, and then hits until game has a result
        self.play_again()
        # Set middle cards face down
        for i in range(4):
            self.game.cards[i] = "reverse.png"

        # Reveal face down card of dealer
        self.dealer.cards.remove("reverse.png")
        self.dealer.update(self.deck.deal_card())

        # Check double ace for dealer
        if self.dealer.check_double_ace():
            self.dealer.score = 12

        # Update table after 1000ms
        self.after(1000, self.update_table(self.player.cards, self.dealer.cards, self.game.cards))

        # Check for blackjack
        if self.player.is_blackjack():
            if self.dealer.is_blackjack():
                self.game_over_label.config(text=f"GAME OVER\nIt's a draw!")
                self.game_over_label.grid(column=3, row=4)
            else:
                self.game_over_label.config(text=f"GAME OVER\nPlayer has Blackjack!")
                self.game_over_label.grid(column=3, row=4)
                self.result = 1.5
        elif self.dealer.is_blackjack():
            self.game_over_label.config(text=f"GAME OVER\nDealer has Blackjack!")
            self.game_over_label.grid(column=3, row=4)
            self.player.result = 0
        else:
            # Deal cards to dealer
            while self.dealer.score < 17 and self.dealer.score <= self.player.score:
                card = self.deck.deal_card()
                index = self.game.cards.index("reverse.png")
                self.game.cards[index] = card
                self.dealer.update(card)
                self.dealer.is_bust()
                self.update_table(self.player.cards, self.dealer.cards, self.game.cards)
            # Reveal match result
            result = self.player.win_status(self.dealer.score, self.player.score)
            self.game_over_label.config(text=f"GAME OVER\n{result}")
            self.game_over_label.grid(column=3, row=4)

    def reset_game(self):
        # Reset game objects
        self.player.update_bank()
        self.dealer.reset()
        self.player.reset()
        self.game.reset()
        # Remove game result label
        self.game_over_label.grid_forget()
        # Update bank label
        self.player.bet = 0
        self.player_bank_label.config(text=f"Bet: £{self.player.bet}\n\nBank: £{self.player.bank}")
        # Deal player, dealer and game face down cards
        for _ in range(2):
            self.player.update("reverse.png")
            self.dealer.update("reverse.png")
        for _ in range(4):
            self.game.update("reverse.png")
        self.update_table(self.player.cards, self.dealer.cards, self.game.cards)
        # Activate bet and deal buttons
        self.bet_button.grid(column=1, row=5)
        self.deal_button.grid(column=2, row=5)
        # Deactivate play again button
        self.play_again_button.grid_forget()

    def initial_deal(self):
        # Function that deals 2 cards to player, 1 card and 1 face down card to dealer and 4 face down cards to table
        self.player.cards = []
        self.game.cards = []
        self.dealer.cards = []
        # Deal player cards
        for _ in range(2):
            self.player.update(self.deck.deal_card())
        # Deal dealer cards
        self.dealer.update(self.deck.deal_card())
        self.dealer.update("reverse.png")
        # Deal game cards
        for _ in range(4):
            self.game.cards.append("reverse.png")
        return [self.player.cards, self.dealer.cards, self.game.cards]

    def update_table(self, player_cards, dealer_cards, game_cards):
        # Update dealer cards
        d_card_1 = dealer_cards[0]
        card_canvas = Canvas(width=140, height=100, bg=TABLE_COLOUR, highlightthickness=0)
        self.d1 = PhotoImage(file=f"./cards/{d_card_1}").subsample(4, 4)
        card_canvas.create_image(70, 120, image=self.d1)
        card_canvas.grid(column=1, row=0, padx=2, pady=2, sticky="nsew")
        d_card_2 = dealer_cards[1]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.d2 = PhotoImage(file=f"./cards/{d_card_2}").subsample(4, 4)
        card_canvas.create_image(70, 120, image=self.d2)
        card_canvas.grid(column=2, row=0, padx=2, pady=2, sticky="nsew")
        # Update player and dealer score
        self.dealer_label.config(text=f"Dealer score: {self.dealer.score}")
        self.player_label.config(text=f"Player score: {self.player.score}")
        # Update player cards
        p_card_1 = player_cards[0]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.p1 = PhotoImage(file=f"./cards/{p_card_1}").subsample(4, 4)
        card_canvas.create_image(70, 100, image=self.p1)
        card_canvas.grid(column=1, row=4, padx=2, pady=2, sticky="nsew")
        p_card_2 = player_cards[1]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.p2 = PhotoImage(file=f"./cards/{p_card_2}").subsample(4, 4)
        card_canvas.create_image(70, 100, image=self.p2)
        card_canvas.grid(column=2, row=4, padx=2, pady=2, sticky="nsew")
        # Update game cards
        g_card_1 = game_cards[0]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.g1 = PhotoImage(file=f"./cards/{g_card_1}").subsample(4, 4)
        card_canvas.create_image(70, 110, image=self.g1)
        card_canvas.grid(column=0, row=2, sticky="nsew")
        g_card_2 = game_cards[1]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.g2 = PhotoImage(file=f"./cards/{g_card_2}").subsample(4, 4)
        card_canvas.create_image(70, 110, image=self.g2)
        card_canvas.grid(column=1, row=2, sticky="nsew")
        g_card_3 = game_cards[2]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.g3 = PhotoImage(file=f"./cards/{g_card_3}").subsample(4, 4)
        card_canvas.create_image(70, 110, image=self.g3)
        card_canvas.grid(column=2, row=2, sticky="nsew")
        g_card_4 = game_cards[3]
        card_canvas = Canvas(width=140, height=240, bg=TABLE_COLOUR, highlightthickness=0)
        self.g4 = PhotoImage(file=f"./cards/{g_card_4}").subsample(4, 4)
        card_canvas.create_image(70, 110, image=self.g4)
        card_canvas.grid(column=3, row=2, sticky="nsew")


if __name__ == "__main__":
    app = GuiCtk()
    app.mainloop()
