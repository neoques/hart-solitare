import random
import pprint as pp
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import List


class Card:
    card_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    suit = {
        "spade": "♠",
        "club": "♣",
        "heart": "♥",
        "diamond": "♦",
    }

    def __init__(self, suit: str, value):
        self.suit = suit
        self.value = value

    def is_next_card(self, higher_card) -> bool:
        if self.suit != higher_card.suit:
            return False
        if self.card_values.index(self.value) == self.card_values.index(higher_card.value) - 1:
            return True
        return False

    def __str__(self):
        a_str = "{}{}".format(self.suit, str(self.value))
        return "{a_str: <4}".format(a_str=a_str)

    @staticmethod
    def empty_card_str():
        return " " * 4


class Solitaire:
    card_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    suit = {
        "spade": "♠",
        "club": "♣",
        "heart": "♥",
        "diamond": "♦",
    }

    def __init__(self):
        self.moves = []
        self.visible = []
        self.hidden = []
        self.finished_piles = {suit: Card(suit, 0) for suit_name, suit in self.suit.items()}

    def discard(self):
        for a_column in self.visible:
            while len(a_column) > 0 and self.can_discard_a_card(a_column[-1]):
                self.finished_piles[a_column[-1].suit] = a_column[-1]
                a_column.pop()
                self.reveal()

    def can_discard_a_card(self, a_card: Card):
        return self.finished_piles[a_card.suit].is_next_card(a_card)

    def get_piles(self) -> str:
        pile_strings = []
        for a_suit, a_card in self.finished_piles.items():
            pile_strings.append(str(a_card))
        return "      " + "".join(pile_strings) + "\n"

    def get_deck(self) -> str:
        curr_str = ""
        for hidden_cards in self.hidden:
            curr_str += " {}  ".format(str(len(hidden_cards)))
        curr_str += "\n"
        max_len = 0
        for a_column in self.visible:
            max_len = max(len(a_column), max_len)
        for curr_depth in range(max_len):
            for visible_column in self.visible:
                if len(visible_column) > curr_depth:
                    curr_str += str(visible_column[curr_depth])
                else:
                    curr_str += Card.empty_card_str()
            curr_str += "\n"
        return curr_str

    def deal(self):
        # Reset the columns
        self.visible = []
        self.hidden = []

        all_cards = []
        for a_suit_name, a_suit in self.suit.items():
            for a_card_value in self.card_values:
                all_cards.append(Card(a_suit, a_card_value))
        random.shuffle(all_cards)

        # Deal out the cards
        visible_cards = [7, 6, 5, 4, 4, 3, 2]
        hidden_cards = [0, 1, 2, 3, 4, 5, 6]
        for hidden_card_count in hidden_cards:
            self.hidden.append(all_cards[:hidden_card_count])
            all_cards = all_cards[hidden_card_count:]
        for visible_card_count in visible_cards:
            self.visible.append(all_cards[:visible_card_count])
            all_cards = all_cards[visible_card_count:]

    def __str__(self):
        return self.get_piles() + self.get_deck()

    def reveal(self):
        for i, visible_column in enumerate(self.visible):
            if len(visible_column) == 0 and len(self.hidden[i]) > 0:
                visible_column.append(self.hidden[i].pop())
                self.discard()

    def find_legal_moves(self, verbose = True):
        self.moves = []
        for column_to_move_to, a_column in enumerate(self.visible):
            if len(a_column) > 0:
                card_to_be_moved_to = a_column[-1]
                for card_to_be_moved_column, a_column_2 in enumerate(self.visible):
                    for card_to_be_moved_depth, a_card in enumerate(a_column_2):
                        if a_card.is_next_card(card_to_be_moved_to) and card_to_be_moved_column != column_to_move_to:
                            self.moves.append((card_to_be_moved_depth, card_to_be_moved_column, column_to_move_to))
            else:
                for card_to_be_moved_column, a_column_2 in enumerate(self.visible):
                    for card_to_be_moved_depth, a_card in enumerate(a_column_2):
                        if a_card.value == "K":
                            if card_to_be_moved_depth == 0 and len(self.hidden[card_to_be_moved_column]) == 0:
                                continue
                            self.moves.append((card_to_be_moved_depth, card_to_be_moved_column, column_to_move_to))
        if verbose:
            self.display_legal_moves()

    def do_move(self, a_move):
        self.visible[a_move[2]].extend(self.visible[a_move[1]][a_move[0]:])
        self.visible[a_move[1]][a_move[0]:] = []
        self.reveal()

    def display_legal_moves(self):
        for i, a_move in enumerate(self.moves):
            print("Choose {}: Move the card {} in column {} to column {}".format(i, self.visible[a_move[1]][a_move[0]],
                                                                      a_move[1],
                                                                      a_move[2]))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    victory_count = 0
    play_count = 1000
    for i in range(play_count):
        curr_game = Solitaire()
        curr_game.deal()
        curr_game.find_legal_moves(verbose=False)
        curr_game.discard()

        while len(curr_game.moves) > 0:
            print(curr_game)
            curr_game.find_legal_moves()
            has_move_choice = False
            while not has_move_choice:
                move_number = input()
                if move_number.isdigit() and int(move_number) < len(curr_game.moves):
                    curr_game.do_move(curr_game.moves[int(move_number)])
                    has_move_choice = True
            curr_game.find_legal_moves(verbose=False)
            curr_game.discard()
            # random.shuffle(curr_game.moves)
            # curr_game.do_move(curr_game.moves[0])

        if len(sum(curr_game.hidden, [])) == 0 and len(sum(curr_game.visible, [])) == 0:
            victory_count += 1
            print("\n------------------ Victory! ------------------------\n")
        else:
            print("\n------------------ You Lose ------------------------\n")
        print()
        # print(curr_game)
    print(victory_count/play_count)
