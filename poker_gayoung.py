import random
from enum import IntEnum

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

class Ranking(IntEnum):
    high = 0
    one_pair = 1
    two_pair = 2
    triple = 3
    straight = 4
    flush = 5
    full_house = 6
    four_card = 7
    straight_flush = 8

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

    def __repr__(self):
        return self.card

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
        self.ranking = None

    def _check(self,other):
        if self.ranking is None or other.ranking is None:
            raise AttributeError('not evaluated. call eval() method')
        
    def __repr__(self):
        return repr(self.ranking)

    def __eq__(self, other):
        self._check(other)
        return (self.ranking, self.hands) == (other.ranking, other.hands)

    def __gt__(self, other):
        self._check(other)
        return (self.ranking, self.hands) > (other.ranking, other.hands)

    def __lt__(self, other):
        self._check(other)
        return (self.ranking, self.hands) < (other.ranking, other.hands)

    def __ne__(self,other): return not self.__eq__(other)
    def __le__(self,other): return not self.__gt__(other)
    def __ge__(self,other): return not self.__lt__(other)

    def eval(self):
        flush = self.is_flush()
        if flush:
            if self.is_straight():
                self.ranking = Ranking.straight_flush
            else:
                self.ranking = Ranking.flush
            return
        if self.is_straight():
            self.ranking = Ranking.straight
        else:
            ranking = self.find_a_kind()
            self.ranking = Ranking(ranking)


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
                l = []
                l.append(self.hands[1])
                l.append(self.hands[2])
                l.append(self.hands[3])
                l.append(self.hands[4])
                l.append(self.hands[0])
                self.hands = l
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
            return 0
        for i in cards_by_ranks:
            if(len(cards_by_ranks[i])==4):
                return 7
            elif(len(cards_by_ranks[i])==3):
                if(len(cards_by_ranks)==3):
                    return 3
                return 6
            elif(len(cards_by_ranks[i])==2):
                if len(cards_by_ranks)==4:
                    return 1
                elif len(cards_by_ranks) == 2:
                    return 6
                return 2

    def tell_hand_ranking(self):
        f = self.is_flush()
        s = self.is_straight()

        if f is True and s is not None:
            return 8
        elif f is True:
            return 5
        elif s is not None:
            return 4
        else:
            return self.find_a_kind()

    def tell_winner(self, other):
        self_point = self.tell_hand_ranking()
        other_point = other.tell_hand_ranking()
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
