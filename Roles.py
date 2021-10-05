# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:36:08 2021

@author: Velez
"""

from PlayerClass import *

class QuarantineSpecialist(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Quarantine Specialist',initialhand)
        Board.loc[self.Location,'Quarantine']=True
        Board.loc[Board.loc[self.Location,'Adjacency'],'Quarantine']=True
    
    def ChangeLocation(self,newlocation):
        Board.loc[self.Location,'Quarantine']=False
        Board.loc[Board.loc[self.Location,'Adjacency'],'Quarantine']=False
        super().ChangeLocation(newlocation)
        Board.loc[self.Location,'Quarantine']=True
        Board.loc[Board.loc[self.Location,'Adjacency'],'Quarantine']=True
        
class Scientist(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Scientist',initialhand)
    
    def DiscoverCure(self):
        citycardsinhand=[card for card in self.Hand if card.cardtype=='City']
        handcolors=list(set([card.color for card in citycardsinhand]))
        for disease in handcolors:
            if len([card for card in citycardsinhand if card.color==disease])>=4:
                color=disease
                break
        print('The '+self.Name+' can discover the cure for the '+color+' disease discarding 4 cards of that color')
        cards=[card.name for card in citycardsinhand if card.color==color]
        for i in range(len(cards)-4):
            print('Choose card(s) to keep:')
            selection=Choose(options=cards)
            cards.remove(selection)
        for name in cards:
            self.Discard(name)
        GameState['AmountCured']+=1
        if GameState[color+'Cubes']==24:
            GameState[color]='Erradicated'
            print('The '+color+' disease has been erradicated.')
        else:
            GameState[color]='Cured'
            print('You have a cure for the '+color+' disease.')
        locationofmedic=Board[Board['Medic']]
        if len(locationofmedic)>0:
            if locationofmedic[color]>0:
                print('The Medic removed all the '+color+' counters from '+locationofmedic.index[0]+'.')
                GameState[color+'Cubes']+=locationofmedic[color]
                Board.loc[locationofmedic.index[0],color]=0
        self.Actions-=1
        
    def CheckDiscoverCure(self):
        if Board.loc[self.Location,'RS']:
            color=''
            citycardsinhand=[card for card in self.Hand if card.cardtype=='City']
            colors=list(set([card.color for card in citycardsinhand]))
            for disease in colors:
                if len([card for card in citycardsinhand if card.color==disease])>=4:
                    color=disease
                    break
            if color!='' and GameState[color]=='Not cured':
                return True
            return False
        return False
    
    def AvailableActions(self):
        availableactions=super().AvailableActions()
        if 'DiscoverCure' in availableactions.index:
            description='The Scientist can discover the cure of a disease by discarding 4 cards of that color.'
            availableactions.loc['DiscoverCure','Description']=description
        return availableactions

class Researcher(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Researcher',initialhand)
    
    def GiveKnowledge(self):
        availableplayers=[item for item in Board.loc[self.Location,'Players']]
        availableplayers.remove(self)
        names=[Pl.Name for Pl in availableplayers]
        print('Choose a player:')
        playername=Choose(options=names)
        player=availableplayers[names.index(playername)]
        print('Choose a card to give:')
        cardname=Choose(options=self.Citiesinhand)
        print('The Researcher gave the \"'+cardname+'\" card to the '+player.Name)
        self.GiveCard(player,cardname)
        self.Actions-=1
                
    def CheckGiveKnowledge(self):
        if len(self.Citiesinhand)>0 and len(Board.loc[self.Location,'Players'])>1:
            return True
        return False
                
    def CheckGetKnowledgeRes(self):
        return False
    
    def AvailableActions(self):
        availableactions=super().AvailableActions()
        if 'GiveKnowledge' in availableactions.index:
            description='The Researcher can give any of her city cards to any other player in her location.'
            availableactions.loc['GiveKnowledge','Description']=description
            availableactions.loc['GiveKnowledge','Type']='Class Action'
        return availableactions

class Medic(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Medic',initialhand)
        Board.loc['Atlanta','Medic']=True
    
    def ChangeLocation(self,newlocation):
        Board.loc[self.Location,'Medic']=False
        super().ChangeLocation(newlocation)
        Board.loc[self.Location,'Medic']=True
        curedcolors=GameState[GameState=='Cured'].index
        if len(curedcolors)>0:
            for color in curedcolors:
                GameState[color+'Cubes']+=Board.loc[self.Location,color]
                Board.loc[self.Location,color]=0
                print('The '+self.Name+' removed all the '+color+' counters from '+self.Location+'.')
                if GameState[color+'Cubes']==24:
                    print('The '+color+' disease is erradicated.')
                    GameState[color]='Erradicated'
                
    def TreatDisease(self):
        colors=Board.loc[self.Location,['Blue','Red','Yellow','Black']]
        colors=colors[colors>0].index.tolist()
        selection=colors[0]
        if len(colors)>1:
            print('Choose which disease to treat:')
            selection=Choose(options=colors)
        GameState[selection+'Cubes']+=Board.loc[self.Location,selection]
        Board.loc[self.Location,selection]=0
        print('The Medic removed all '+selection+' counters from '+self.Location+'.')
        self.Actions-=1
        
    def AvailableActions(self):
        availableactions=super().AvailableActions()
        if 'TreatDisease' in availableactions.index:
            description='The Medic can remove all the disease counters of a single color in his location.'
            availableactions.loc['TreatDisease','Description']=description
        return availableactions
       
            
class OperationsExpert(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Operations Expert',initialhand)
        self.CanFly=True
    
    def StartTurn(self):
        super().StartTurn()
        self.CanFly=True
        
    def BuildRS(self):
        print('The '+self.Name+' built a research station in '+self.Location)
        Board.loc[self.Location,'RS']=True
        GameState['AvailableRS']-=1
        self.Actions-=1
        
    
    def OperationsFlight(self):
        print('Choose a card to discard:')
        card=Choose(options=self.Citiesinhand)
        self.Discard(card)
        print('Choose a city to relocate the '+self.Name+':')
        city=Choose()
        self.ChangeLocation(city)
        self.CanFly=False
        self.Actions-=1
            
    def CheckBuildRS(self):
        cond1=Board.loc[self.Location,'RS']==False
        cond2=GameState['AvailableRS']>0
        if cond1 and cond2:
            return True
        return False
    
    def CheckOperationsFlight(self):
        if len(self.Citiesinhand)>0 and Board.loc[self.Location,'RS']and self.CanFly:
            return True
        return False
    
    def AvailableActions(self):
        availableactions=super().AvailableActions()
        if 'BuildRS' in availableactions.index:
            description='The Operations Expert can build a research station without discarding.'
            availableactions.loc['BuildRS','Description']=description
        if self.CheckOperationsFlight():
            availableactions.loc['OperationsFlight']=[self.OperationsFlight,'Operations flight','Class Action',
                                                      'Once per turn, the '+
                                                      'Operations Expert can discard any city card to move to any city.']
        return availableactions

class ContingencyPlanner(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Contingency Planner',initialhand)
        self.StoredEvent=''
    
    def StoreEvent(self):
        if self.StoredEvent!='':
            print('The '+self.Name+' will replace the event card currently in store.',
                  'The current card will be removed from the game.')
            self.StoredEvent.holder=''
        print('The '+self.Name+' can store one of the following events:')
        discardedevents=[card for card in PDD if card.cardtype=='Event']
        selection=Choose(options=[card.name for card in discardedevents])
        selectedcard=discardedevents[[card.name for card in discardedevents].index(selection)]
        PDD.remove(selectedcard)
        self.StoredEvent=selectedcard
        selectedcard.holder=self
        self.Actions-=1
    
    def PlayEvent(self,eventname):
        if self.StoredEvent=='' or eventname!=self.StoredEvent.name:
            super().PlayEvent(eventname)
        else:
            self.Hand.append(self.StoredEvent)
            super().PlayEvent(eventname)
            PDD.remove(self.StoredEvent)
            self.StoredEvent=''
            
    
    def CheckStoreEvent(self):
        discardedevents=[card for card in PDD if card.cardtype=='Event']
        if len(discardedevents)>0:
            return True
        return False
    
    def AvailableActions(self):
        availableactions=super().AvailableActions()
        if self.CheckStoreEvent():
            availableactions.loc['StoreEvent']=[self.StoreEvent,'Store event','Class Action',
                                                'The Contingency Planner can '+
                                                ' store an event from the discard deck.']
        return availableactions
    
    def Info(self):
        print('\n')
        print('Role:',self.Name)
        print('Location:',self.Location)
        print('Number of Actions:',self.Actions)
        print('\nHand:')
        HandDF=[[card.name,card.color,card.cardtype] for card in self.Hand 
                if card.cardtype=='City']
        HandDF.extend([[card.name,'',card.cardtype] for card in self.Hand 
                       if card.cardtype=='Event'])
        HandDF=pd.DataFrame(HandDF,columns=['Name','Color','Type'])
        HandDF.set_index('Name',inplace=True)
        display(HandDF)
        if self.StoredEvent!='':
            print('\nStored Event: '+self.StoredEvent.name+'.')
        print('\n')
        
class Dispatcher(Player):
    
    def __init__(self,initialhand=7):
        super().__init__('Dispatcher',initialhand)
        
    def SelectPlayer(self):
        names=[Pl.Name for Pl in GameState['Players']]
        print('Select a player to move:')
        charname=Choose(options=names)
        return GameState['Players'][names.index(charname)]
    
    def Dispatch(self):
        char=self.SelectPlayer()
        locations=[Pl.Location for Pl in GameState['Players'] if Pl.Location!=char.Location]
        print('Select the new location of the '+char.Name)
        newloc=Choose(options=locations)
        char.ChangeLocation(newloc)
        self.Actions-=1
    
    def Drive(self):
        char=self.SelectPlayer()
        print('The '+char.Name+' can drive to the following cities:')
        selection=Choose(options=Board.loc[char.Location,'Adjacency'])
        char.ChangeLocation(selection)
        self.Actions-=1
                    
    def DirectFlight(self):
        char=self.SelectPlayer()
        availablecities=[city for city in self.Citiesinhand]
        print('The '+self.Name+' can fly to the following cities:')
        selection=Choose(options=availablecities)
        self.Discard(selection)
        char.ChangeLocation(selection)
        self.Actions-=1
                        
    def CharterFlight(self):
        players=[Pl for Pl in GameState['Players'] if Pl.Location in self.Citiesinhand]
        names=[Pl.Name for Pl in players]
        print('The following players can take charter flights with the city cards in the Dispatcher\'s hand:')
        charname=Choose(options=names)
        char=players[names.index(charname)]
        print('The '+self.Name+' discards the \"'+char.Location+'\" card. The '+char.Name+' can fly to any city:')
        self.Discard(char.Location)
        selection=Choose()
        char.ChangeLocation(selection)
        self.Actions-=1
    
    def ShuttleFlight(self):
        CitieswithRS=Board[Board['RS']].index.tolist()
        players=[Pl for Pl in GameState['Players'] if Pl.Location in CitieswithRS]
        names=[Pl.Name for Pl in players]
        print('The following players can take shuttle flights:')
        charname=Choose(options=names)
        char=players[names.index(charname)]
        print('The '+char.Name+' can take a shuttle to the following cities:')
        CitieswithRS.remove(char.Location)
        selection=Choose(options=CitieswithRS)
        char.ChangeLocation(selection)
        self.Actions-=1
            
    def CheckDispatch(self):
        locations=[Pl.Location for Pl in GameState['Players']]
        locations=list(set(locations))
        if len(locations)>1:
            return True
        return False
    
    def CheckDirectFlight(self):
        locations=[Pl.Location for Pl in GameState['Players']]
        locations=set(locations)
        if not set(self.Citiesinhand).issubset(locations):
            return True
        return False
    
    def CheckCharterFlight(self):
        players=[Pl for Pl in GameState['Players'] if Pl.Location in self.Citiesinhand]
        if len(players)>0:
            return True
        return False
    
    def CheckShuttleFlight(self):
        citieswithRS=Board[Board['RS']].index
        players=[Pl for Pl in GameState['Players'] if Pl.Location in citieswithRS]
        if len(citieswithRS)>1 and len(players)>0:
            return True
        return False
    
    def AvailableActions(self):
        availableactions=super().AvailableActions()
        description='The Dispatcher can move any player to a city adjacent to that player\'s location.'
        availableactions.loc['Drive','Description']=description
        if 'DirectFlight' in availableactions.index:
            description='The Dispatcher can discard a city card to move any player to that location.'
            availableactions.loc['DirectFlight','Description']=description
        if 'CharterFlight' in availableactions.index:
            description='The Dispatcher can discard the city card of any player\'s location to move that player to any city.'
            availableactions.loc['CharterFlight','Description']=description
        if 'ShuttleFlight' in availableactions.index:
            description='The Dispatcher can move any player in a city with a research station to any other city with a research station.'
            availableactions.loc['ShuttleFlight','Description']=description
        if self.CheckDispatch():
            availableactions.loc['Dispatch']=[self.Dispatch,'Dispatch','Class Action',
                                              'The Dispatcher can move any player to the location of any '+
                                                'other player.']
        return availableactions