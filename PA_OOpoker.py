import random

suits = 'CDHS'
ranks = '23456789TJQKA'

from abc import ABCMeta, abstractmethod

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()

class PKCard(Card):
    def value(self):
        list_value = list(self.card)
        if(self.card[0]=='J'):
            return 11
        elif(self.card[0]=='T'):
            return 10
        elif(self.card[0]=='Q'):
            return 12
        elif(self.card[0]=='K'):
            return 13
        elif(self.card[0]=='A'):
            return 14
        else:
            return int(self.card[0])
        
    def __init__(self, Card):
        self.card = Card 

    def __getitem__(self, index):
        return self.card[index]

class Deck:
    def __init__(self, cls):
        self.deck = [i+j for i in suits for j in ranks]
        deck_list = []
        for k in self.deck:
            deck_list.append(cls(k))
        self.deck = deck_list

    def __str__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, index):
        return self.deck[index]

    def shuffle(self):
        random.shuffle(self.deck)

    def pop(self):
        return self.deck.pop()

class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.hands = []
        for i in cards:
            self.hands.append(PKCard(i))
        self.hands = sorted(self.hands, reverse=True)


    def is_flush(self):  
        if(self.hands[0][1]==self.hands[1][1]==self.hands[2][1]==self.hands[3][1]==self.hands[4][1]):
            return True
        else:
            return False

    def is_straight(self): 
        rank_list = []
        for i in self.hands:
            rank_list.append(i.value())
        rank_list = list(reversed(list(set(rank_list))))
        if(len(rank_list) == 5):  
            if(rank_list[0] - rank_list[4] == 4):
                return rank_list
            elif(rank_list[0]==14 and rank_list[0] - rank_list[1]==9):
                return rank_list
        return None

    def classify_by_rank(self):
        rankdic = {'A':[], 'K':[], 'Q':[], 'J':[], 'T':[], '9':[], '8':[], '7':[], '6':[], '5':[] , '4': [], '3': [], '2': []}
        rankdic2 = {}
        for i in range (5):
            rankdic[self.hands[i][0]].append([self.hands[i][0],self.hands[i][1]])
        for i in rankdic:
            if(len(rankdic[i])!=0):
                rankdic2[i] = rankdic[i]
        if(len(rankdic2)==5):
            return None
        l = sorted(rankdic2.values(), key = lambda x: len(x),reverse=True)
        sorted_l = []
        for i in l:
            for j in i:
                sorted_l.append(PKCard(j))
        self.hands = sorted_l
        return rankdic2

    def find_a_kind(self):  
        cards_by_ranks = self.classify_by_rank()
        if cards_by_ranks is None:
            return 'high'
        for i in cards_by_ranks:
            if(len(cards_by_ranks[i])==4):
                return 'four of a kind'
            elif(len(cards_by_ranks[i])==3):
                if(len(cards_by_ranks)==3):
                    return 'triple'
                return 'full house'
            elif(len(cards_by_ranks[i])==2):
                if len(cards_by_ranks)==4:
                    return 'one pair'
                elif len(cards_by_ranks) == 2:
                    return 'full house'
                return 'two pair'

    def tell_hand_ranking(self):
        f = self.is_flush()
        s = self.is_straight()

        if f is True and s is not None:
            return 'straight flush'
        elif f is True:
            return 'flush'
        elif s is not None:
            return 'straight'
        else:
            return self.find_a_kind()

    def tell_winner(self, other):
        point = {'high':0, 'one pair':1, 'two pair':2, 'triple':3, 'straight':4, 'flush':5, 'full house':6, 'four of a kind':7, 'straight flush':8}
        self_point = point[self.tell_hand_ranking()]
        other_point = point[other.tell_hand_ranking()]
        if self_point > other_point:
            return True
        elif self_point < other_point:
            return False
        else:
            if self.hands[0].value() > other.hands[0].value():
                return True
            elif self.hands[0].value() < other.hands[0].value():
                return False
            else:
                if self_point == 2 or 1:
                    if self.hands[2].value() > other.hands[2].value():
                        return True
                    elif self.hands[2].value() < other.hands[2].value():
                        return False
                    else:
                        if self.hands[3].value() > other.hands[3].value():
                            return True
                        elif self.hands[3].value() < other.hands[3].value():
                            return False
                        else:
                            if self.hands[4].value() > other.hands[4].value():
                                return True
                            elif self.hands[4].value() < other.hands[4].value():
                                return False
                return None



if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()

    my_hand = []
    your_hand = []
    for i in range(5):
        for hand in (my_hand, your_hand):
            card = deck.pop()
            hand.append(card)
    print(my_hand)
    print(your_hand)


    #Test Straight Flush
    card = ['5C','6C', '7C', '8C', '9C']
    test(Hands(card).tell_hand_ranking() == 'straight flush')
    #Test Straight
    card = ['5C', '6H', '7C', '8C', '9S']
    test(Hands(card).tell_hand_ranking() == 'straight')
    #Test flush
    card = ['5C', 'AC', 'QC', 'AC', 'TC']
    test(Hands(card).tell_hand_ranking() == 'flush')
    #Test Four card
    card = ['AC', 'AH', 'AS', 'AD', '9S']
    test(Hands(card).tell_hand_ranking() == 'four of a kind')
    #Test Full House
    card = ['2C', '2H', '2S', 'KH', 'KS']
    test(Hands(card).tell_hand_ranking() == 'full house')
    #Test Triple
    card = ['3C', '3H', '3D', 'QH', 'JD']
    test(Hands(card).tell_hand_ranking() == 'triple')
    #Test Two Pair
    card = ['3C', '3H', 'QD', 'QH', 'JD']
    test(Hands(card).tell_hand_ranking() == 'two pair')
    #Test One Pair
    card = ['AC', '7H', '3D', 'JH', 'JD']
    test(Hands(card).tell_hand_ranking() == 'one pair')
    #Test One Pair
    card = ['8C', '9H', 'AD', 'TH', 'KD']
    test(Hands(card).tell_hand_ranking() == 'high')

    #Test same rank but value is different in Straight flush
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7H', '8H', '9H'])
    test(my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in flush
    my_hand = Hands(['5C','6C', '7C', '8C', 'TC'])
    your_hand = Hands(['TH','AH', '7H', '8H', '9H'])
    test(my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in Straight
    my_hand = Hands(['5C','6H', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7D', '8H', '9H'])
    test(my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in Four card
    my_hand = Hands(['5C','5S', '5D', '5H', '9C'])
    your_hand = Hands(['2C','2S', '2D', '2H', '9H'])
    test(my_hand.tell_winner(your_hand) == True)
    #Test same rank but value is different in Full House
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7H', '8H', '9H'])
    test(my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in Triple
    my_hand = Hands(['5C','5H', '5D', '8C', '9C'])
    your_hand = Hands(['TH','TS', 'TD', '8H', '9H'])
    test(my_hand.tell_winner(your_hand) == False)
    #Test same rank first value but second value is different in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '2H', '2D', '9H'])
    test(my_hand.tell_winner(your_hand) == True)
    #Test same rank, first value and second value but last value is different in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '7D', 'TH'])
    test(my_hand.tell_winner(your_hand) == False)
    #Test same rank, all value in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '7D', '9H'])
    test(my_hand.tell_winner(your_hand) == None)
    #Test same rank, value is Difference in One Pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '6D', '9H'])
    test(my_hand.tell_winner(your_hand) == True)
    #Test same rank, value is Difference in One Pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', 'QH', '6D', '9H'])
    test(my_hand.tell_winner(your_hand) == True)
    #Test same rank in One pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', 'QH', '7D', '9H'])
    test(my_hand.tell_winner(your_hand) == None)
    #Straight Flush vs High Card
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['8C', '9H', 'AD', 'TH', 'KD'])
    test(my_hand.tell_winner(your_hand) == True)
    #if same rank and value, winner is None
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['5H','6H', '7H', '8H', '9H'])
    test(my_hand.tell_winner(your_hand) == None)