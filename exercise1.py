from random import randint, choice

def add_players(players, players_count):
    for i in range(1, players_count + 1):
        players.append(input(f"Enter name of the player {i}: "))

def generate_single_card():
    value_of_cards = randint(2, 14)

    if value_of_cards == 11:
        value_of_cards = 'J'
    elif value_of_cards == 12:
        value_of_cards = 'Q'
    elif value_of_cards == 13:
        value_of_cards = 'K'
    elif value_of_cards == 14:
        value_of_cards = 'A'
    else:
        value_of_cards = str(value_of_cards)    

    color_of_cards = choice(['Spade', 'Heart', 'Diamond', 'Club'])

    return f"{value_of_cards} {color_of_cards}"  


def dealing_cards(players, cards_per_player):
    all_cards = []        
    card_for_players = {player: [] for player in players}
    dealing_total_cards = len(players) * cards_per_player
    counter = 0
    
    while len(all_cards) < dealing_total_cards:
        card = generate_single_card()
        if all_cards.count(card) >= 4:
            continue
        all_cards.append(card)

        current_player = players[counter % len(players)]
        card_for_players[current_player].append(card)
        counter += 1
        
    #to check problematic cases    
    #put while loop in comment
    #and run with the following lines
    """
    if len(players) == 3:    
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("Q Spade")
        
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("Q Heart")
        card_for_players[players[1]].append("Q Heart")

        card_for_players[players[2]].append("A Club")
        card_for_players[players[2]].append("A Club")
        card_for_players[players[2]].append("A Club")
        card_for_players[players[2]].append("Q Club")
        card_for_players[players[2]].append("Q Club")

    if len(players) == 2:    
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("A Spade")
        card_for_players[players[0]].append("Q Spade")
        
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("A Heart")
        card_for_players[players[1]].append("Q Heart")
    """
    return card_for_players    


def swap_one_card(cards_for_players):
    all_cards = [card for cards in cards_for_players.values() for card in cards]

    for player, cards in cards_for_players.items():
        while True:
            swap_or_not = input(f"Do you want to swap a card, {player}? Y/N: ").strip().upper()
            if swap_or_not in {'Y', 'N'}:
                break 
            else:
                print("Invalid input. Please choose Y or N.")

        if swap_or_not == 'Y':
            choose_one_card = {index: card for index, card in enumerate(cards, start=1)}

            print(f"{player}'s current cards:")
            for index, card in choose_one_card.items():
                print(f"{index}. {card}")

            while True:
                try:
                    choice = int(input(f"{player}, select the number of the card you want to swap: "))
                    if choice in choose_one_card:
                        card_to_swap = choose_one_card[choice]
                        new_card = generate_single_card()

                        while all_cards.count(new_card) >= 4:
                            new_card = generate_single_card()

                        cards[cards.index(card_to_swap)] = new_card
                        all_cards.append(new_card)
                        all_cards.remove(card_to_swap)

                        print(f"{player} swapped {card_to_swap} for {new_card}.\n")
                        break 
                    else:
                        print("Invalid choice. Please select a valid card number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    return cards_for_players

def counting_points(cards_for_players):
    points = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20
    }

    player_points = {}

    for player, cards in cards_for_players.items():
        total_points = 0 
        for card in cards:
            card_value = card.split()[0]
            total_points += points.get(card_value, 0)
        player_points[player] = total_points

    return player_points    

def display_hands(cards_for_players):
    for player, cards in cards_for_players.items():
        print(f"Card of {player}")
        print("\n".join(cards))
        print("-" * 50)     

def display_points(player_points):
    for player, points in player_points.items():
        print(f"Total points for {player}: {points}")
        print("-" * 50) 

#compares points and eliminates player if necessary
def compare_points(player_points, cards_for_players, players):
    min_points = min(player_points.values())
    lowest_players = [player for player, points in player_points.items() if points == min_points]

    if len(lowest_players) == 1:
        eliminated_player = lowest_players[0]
        players.remove(eliminated_player)
        del player_points[eliminated_player]
        del cards_for_players[eliminated_player]
        print(f"{eliminated_player} has been eliminated based on points.\n")
    else:       #when last two players have equal points not considering suits and values, only points are equal
        min_suit_count = float('inf')
        lowest_suit_players = []

        for player in lowest_players:
            suit_count = {'Spade': 0, 'Heart': 0, 'Diamond': 0, 'Club': 0}
            for card in cards_for_players[player]:
                value, suit = card.split() 
                suit_count[suit] += 1

            most_frequent_suit_count = max(suit_count.values())

            fewest_in_most_frequent_suit = suit_count.get(
                [suit for suit, count in suit_count.items() if count == most_frequent_suit_count][0], 0)

            if fewest_in_most_frequent_suit < min_suit_count:
                min_suit_count = fewest_in_most_frequent_suit
                lowest_suit_players = [player]
            elif fewest_in_most_frequent_suit == min_suit_count:
                lowest_suit_players.append(player)

        if len(lowest_suit_players) == 1:
            eliminated_player = lowest_suit_players[0]
            players.remove(eliminated_player)
            del player_points[eliminated_player]
            del cards_for_players[eliminated_player]
            print(f"{eliminated_player} has been eliminated based on suit count.\n")
        else:       #couldn't determine by suits either, now check equal values
            min_card_value = float('inf')
            lowest_value_players = [] 

            for player in lowest_suit_players:
                value_count = {}
                for card in cards_for_players[player]:
                    value, suit = card.split()
                    value_count[value] = value_count.get(value, 0) + 1

                fewest_same_value_cards = min(value_count.values())

                if fewest_same_value_cards < min_card_value:
                    min_card_value = fewest_same_value_cards
                    lowest_value_players = [player]
                elif fewest_same_value_cards == min_card_value:
                    lowest_value_players.append(player)

            if len(lowest_value_players) == 1:
                eliminated_player = lowest_value_players[0]
                players.remove(eliminated_player)
                del player_points[eliminated_player]
                del cards_for_players[eliminated_player]
                print(f"{eliminated_player} has been eliminated based on the fewest same-value cards.\n")  
            else:       #everything is equal, nobody got eliminated
                print("Nobody got eliminated, re-dealing cards...\n") 
                  

def main():
    players = []
    cards_per_player = 5
    players_count = 3
    add_players(players, players_count)

    while len(players) > 1:
        cards_for_players = dealing_cards(players, cards_per_player)
        display_hands(cards_for_players)
        swap_one_card(cards_for_players)    
        player_points = counting_points(cards_for_players)
        display_points(player_points)
        compare_points(player_points, cards_for_players, players)
    
    winner = players[0]    
    print(f"The winner is: {winner}")
   
if __name__ == "__main__":
    main()

