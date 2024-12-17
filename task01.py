import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.full_name = self.value + " of " + self.suit
    
    def __str__(self):
        return f"{self.full_name}"
        
class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        pass

class Game:
    def __init__(self, num_of_decks, num_of_players):
        self.num_of_decks = num_of_decks
        self.suits = ["H", "S", "D", "C"]
        self.values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        self.card_index_list = []
        self.num_of_players = num_of_players
        
    def fill(self):
        for i in range(0, 52*self.num_of_decks):
            self.card_index_list.append(i)

    def get_card_by_index(sefl, card_index):
        card_index = card_index % 52
        suit_index = card_index // 13
        value_index = card_index % 13
        card_result = Card(sefl.suits[suit_index], sefl.values[value_index])
        return card_result
    
    def shuffle_by_index(self):
        index_list = random.sample(self.card_index_list, 5*self.num_of_players)
        return index_list

    def shuffle_to_players(self):
        index_list = self.shuffle_by_index()
        card_list = []
        for i in index_list:
            card_list.append(self.get_card_by_index(i).full_name)
        #for j in card_list:
        #    print(j)
        index_for_player = {}
        for i in range(self.num_of_players):
            index_for_player[i] = card_list[i*5:i*5+5]
        return index_for_player


def main():
    g = Game(4, 3)
    g.fill()
    ca = g.get_card_by_index(59)
    print(ca.full_name)
    #p = g.shuffle_by_index()
    #print(p)
    print(g.shuffle_to_players())
    k = g.shuffle_to_players()
    #for i, l in k:
    #    print(f"{i}, {l}")

if __name__=="__main__":
    main()