# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:38:44 2021

@author: Velez
"""

class Card():
    def __init__(self,Name,CardType):
        self.name=Name
        self.cardtype=CardType
    def Info(self):
        print(self.name,self.cardtype)
        
class CityCard(Card):
    def __init__(self,Name,Color):
        super().__init__(Name,'City')
        self.color=Color
    def Info(self):
        super().Info()
        print(self.color)
        
class EventCard(Card):
    def __init__(self,Name,Description):
        super().__init__(Name,'Event')
        self.description=Description
        self.holder=''
        
class InfectionCard(Card):
    def __init__(self,Name,Color):
        super().__init__(Name,'Infection')
        self.color=Color
