# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:25:48 2021

@author: Velez
"""

from Functions import *

class Player():
    
    def __init__(self,name,initialhand=7):
        global Board,GameState
        self.Name=name
        self.Location='Atlanta'
        self.Hand=[]
        self.Citiesinhand=[]
        self.Actions=0
        for i in range(initialhand):
            self.Draw()
        Board.loc['Atlanta','Players'].append(self)
        GameState['Players'].append(self)
    
    def StartTurn(self):
        global GameState
        self.Actions=4
        GameState['SkipInfection']=False
        print('\nThe active character is the '+self.Name)
        
    def ChangeLocation(self,newlocation):
        global Board
        Board.loc[self.Location,'Players'].remove(self)
        self.Location=newlocation
        Board.loc[self.Location,'Players'].append(self)
    
    def Discard(self,cardname):
        global PDD,HeldEvents
        card=self.Hand[[card.name for card in self.Hand].index(cardname)]
        self.Hand.remove(card)
        PDD.append(card)
        if card.cardtype=='Event':
            card.holder=''
        if card.cardtype=='City':
            self.Citiesinhand.remove(cardname)
    
    def GiveCard(self,otherplayer,cardname):
        card=self.Hand[[card.name for card in self.Hand].index(cardname)]
        self.Hand.remove(card)
        self.Citiesinhand.remove(cardname)
        otherplayer.Hand.append(card)
        otherplayer.Citiesinhand.append(cardname)
        otherplayer.CheckHandSize()
    
    def Draw(self):
        global PD,PDD,ID,IDD,GameState,Board,Events,HeldEvents
        topcard=PD[-1]
        PD.remove(topcard)
        if topcard.cardtype=='Epidemic':
            PDD.append(topcard)
            GameState['Epidemic']+=1
            GameState['Rate']=2+int((GameState['Epidemic']-1)/2)
            infectioncard=ID[0]
            ID.remove(infectioncard)
            IDD.append(infectioncard)
            print('Epidemic in '+infectioncard.name+'!')
            print('The infection rate is '+str(GameState['Rate'])+'.')
            counters=min(3,4-Board.loc[infectioncard.name,infectioncard.color])
            for i in range(counters):
                PlaceDC(location=infectioncard.name,color=infectioncard.color,outbreaks=[])
            HeldEvents=[card for card in Events if card.holder!='']
            if len(HeldEvents)>0:
                print('Do you want to play an event?')
                selection=Choose(options=['Yes','No'])
                if selection=='Yes':
                    print('Select an event:')
                    eventselection=Choose(options=[card.name for card in HeldEvents])
                    event=HeldEvents[[card.name for card in HeldEvents].index(eventselection)]
                    event.holder.PlayEvent(event.name)
            random.shuffle(IDD)
            ID.extend(IDD)
            IDD=[]
        else:
            if topcard.cardtype=='Event':
                topcard.holder=self
            if topcard.cardtype=='City':
                self.Citiesinhand.append(topcard.name)
            self.Hand.append(topcard)
            print('The '+self.Name+' drew the \"'+topcard.name+'\" card.')
            self.CheckHandSize()
            
    def CheckHandSize(self):
        if len(self.Hand)==8:
            print('There are more than seven cards in the hand of the '+self.Name)
            eventsinhand=[card.name for card in self.Hand if card.cardtype=='Event']
            choice='Discard a card'
            if len(eventsinhand)>0:
                print('The '+self.Name+' can play an event or discard a card:')
                choice=Choose(options=['Play an event','Discard a card'])
            if choice=='Discard a card':
                print('Choose a card to discard:')
                selection=Choose(options=[card.name for card in self.Hand])
                self.Discard(selection)
            else:
                print('Choose an event to play:')
                selection=Choose(options=eventsinhand)
                self.PlayEvent(selection)
            
    def PlayEvent(self,eventname):
        global ID,IDD,GameState,Board
        print('The '+self.Name+' used the \"'+eventname+'\" event')
        self.Discard(eventname)
        if eventname=='Airlift':
            print('Which character will change locations?')
            names=[Pl.Name for Pl in GameState['Players']]
            charname=Choose(options=names)
            char=GameState['Players'][names.index(charname)]
            print('Choose the new location of the character:')
            cityselection=Choose()
            char.ChangeLocation(cityselection)
            
        elif eventname=='Forecast':
            top6=ID[-6:]
            for i in range(6):
                ID.remove(top6[i])
            for i in range(5):
                print('These are the cards at the top of the infection deck, choose which one to return now:')
                selection=Choose(options=[card.name for card in top6])
                selectedcard=top6[[card.name for card in top6].index(selection)]
                top6.remove(selectedcard)
                ID.append(selectedcard)
            ID.append(top6[0])
            
        elif eventname=='Government Grant':
            if GameState['AvailableRS']==0:
                print('There are no available research stations. The card was discarded.')
            else:
                print('You can build a research station in any city:')
                while True:
                    selection=Choose()
                    if Board.loc[selection,'RS']:
                        print('That city already has a research station')
                    else:
                        Board.loc[selection,'RS']=True
                        GameState['AvailableRS']-=1
                        break
                    
        elif eventname=='One Quiet Night':
            print('You will skip the next infection step')
            GameState['SkipInfection']=True
            
        elif eventname=='Resilient Population':
            print('Choose a card to remove from the infection discard deck:')
            selection=Choose(options=[card.name for card in IDD])
            selectedcard=IDD[[card.name for card in IDD].index(selection)]
            IDD.remove(selectedcard)
                
    def Drive(self):
        global Board
        print('The '+self.Name+' can drive to the following cities:')
        selection=Choose(options=Board.loc[self.Location,'Adjacency'])
        self.ChangeLocation(selection)
        self.Actions-=1
                    
    def DirectFlight(self):
        availablecities=[city for city in self.Citiesinhand if city!=self.Location]
        print('The '+self.Name+' can fly to the following cities:')
        selection=Choose(options=availablecities)
        self.Discard(selection)
        self.ChangeLocation(selection)
        self.Actions-=1
                        
    def CharterFlight(self):
        print('The '+self.Name+' discards the \"'+self.Location+'\" card to fly to any city:')
        self.Discard(self.Location)
        selection=Choose()
        self.ChangeLocation(selection)
        self.Actions-=1
    
    def ShuttleFlight(self):
        citieswithRS=(Board[Board['RS']].index).tolist()
        citieswithRS.remove(self.Location)
        print('The '+self.Name+' can take a shuttle to the following cities:')
        selection=Choose(options=citieswithRS)
        self.ChangeLocation(selection)
        self.Actions-=1
            
    def BuildRS(self):
        print('The '+self.Name+' discarded the \"'+self.Location+'\" card to build a research station')
        self.Discard(self.Location)
        Board.loc[self.Location,'RS']=True
        GameState['AvailableRS']-=1
        self.Actions-=1
    
    def TreatDisease(self):
        colors=Board.loc[self.Location,['Blue','Red','Yellow','Black']]
        colors=colors[colors>0].index.tolist()
        selection=colors[0]
        if len(colors)>1:
            print('Choose which disease to treat:')
            selection=Choose(options=colors)
        if GameState[selection]=='Not cured':
            GameState[selection+'Cubes']+=1
            Board.loc[self.Location,selection]-=1
            print('The '+self.Name+' removed one '+selection+' counter from '+self.Location+'.')
        else:
            GameState[selection+'Cubes']+=Board.loc[self.Location,selection]
            Board.loc[self.Location,selection]=0
            print('The '+self.Name+' removed all '+selection+' counters from '+self.Location+'.')
            if GameState[selection+'Cubes']==24:
                GameState[selection]='Erradicated'
        self.Actions-=1
            
    def GiveKnowledge(self):
        availableplayers=[item for item in Board.loc[self.Location,'Players']]
        availableplayers.remove(self)
        names=[Pl.Name for Pl in availableplayers]
        if len(names)==1:
            print('The '+self.Name+' gives the \"'+self.Location+'\" card to the '+names[0])
            self.GiveCard(availableplayers[0],self.Location)
        else:
            print('The '+self.Name+' can give the \"'+self.Location+'\" card to the following players:')
            charname=Choose(options=names)
            self.GiveCard(availableplayers[names.index(charname)],self.Location)
        self.Actions-=1
                            
    def GetKnowledge(self):
        availableplayers=[item for item in Board.loc[self.Location,'Players']]
        availableplayers.remove(self)
        for Pl in availableplayers:
            if self.Location in Pl.Hand.index:
                print('The '+Pl.Name+' gave the '+self.Location+' card to the '+self.Name)
                Pl.GiveCard(self,self.Location)
        self.Actions-=1
    
    def GetKnowledgeRes(self):
        researcher=[Pl for Pl in Board.loc[self.Location,'Players'] if Pl.Name=='Researcher'][0]
        availablecards=[card.name for card in researcher.Hand if card.cardtype=='City']
        print('What card will the Researcher give to the '+self.Name+'?')
        selection=Choose(options=availablecards)
        print('The Researcher gave the \"'+selection+'\" card to the '+self.Name)
        researcher.GiveCard(self,selection)
        self.Actions-=1
        
    def DiscoverCure(self):
        citycardsinhand=[card for card in self.Hand if card.cardtype=='City']
        handcolors=list(set([card.color for card in citycardsinhand]))
        for disease in handcolors:
            if len([card for card in citycardsinhand if card.color==disease])>=5:
                color=disease
                break
        print('The '+self.Name+' can discover the cure for the '+color+' disease discarding 5 cards of that color')
        cards=[card.name for card in citycardsinhand if card.color==color]
        for i in range(len(cards)-5):
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
            
    def CheckDirectFlight(self):
        availablecities=[city for city in self.Citiesinhand if city!=self.Location]
        if len(availablecities)>0:
            return True
        return False
    
    def CheckCharterFlight(self):
        if self.Location in self.Citiesinhand:
            return True
        return False
        
    def CheckShuttleFlight(self):
        citieswithRS=Board[Board['RS']].index
        if self.Location in citieswithRS and len(citieswithRS)>1:
            return True
        return False
    
    def CheckBuildRS(self):
        cond1=self.Location in self.Citiesinhand
        cond2=Board.loc[self.Location,'RS']==False
        cond3=GameState['AvailableRS']>0
        if cond1 and cond2 and cond3:
            return True
        return False
    
    def CheckTreatDisease(self):
        colors=Board.loc[self.Location,['Blue','Red','Yellow','Black']]
        colors=colors[colors>0]
        if len(colors)>0:
            return True
        return False
    
    def CheckGiveKnowledge(self):
        if self.Location in self.Citiesinhand and len(Board.loc[self.Location,'Players'])>1:
            return True
        return False
    
    def CheckGetKnowledge(self):
        availableplayers=[Pl for Pl in Board.loc[self.Location,'Players']]
        availableplayers.remove(self)
        for Pl in availableplayers:
            if self.Location in Pl.Citiesinhand:
                return True
        return False
    
    def CheckGetKnowledgeRes(self):
        availableplayers=[Pl for Pl in Board.loc[self.Location,'Players']]
        names=[Pl.Name for Pl in availableplayers]
        if 'Researcher' in names:
            researcher=availableplayers[names.index('Researcher')]
            if len(researcher.Citiesinhand)>0:
                return True
            return False
        return False
    
    def CheckDiscoverCure(self):
        if Board.loc[self.Location,'RS']:
            color=''
            citycardsinhand=[card for card in self.Hand if card.cardtype=='City']
            colors=list(set([card.color for card in citycardsinhand]))
            for disease in colors:
                if len([card for card in citycardsinhand if card.color==disease])>=5:
                    color=disease
                    break
            if color!='' and GameState[color]=='Not cured':
                return True
            return False
        return False
    
    def AvailableActions(self):
        availableactions=pd.DataFrame(columns=['Function','Action','Type','Description'])
        availableactions.loc['Drive']=[self.Drive,'Drive/Ferry','Player Action','The '+self.Name+
                                             ' can move to any city adjacent to their location.']
        if self.CheckDirectFlight():
            availableactions.loc['DirectFlight']=[self.DirectFlight,'Direct flight','Player Action',
                                                  'The '+self.Name+' can discard a city card to move to that location.']
        if self.CheckCharterFlight():
            availableactions.loc['CharterFlight']=[self.CharterFlight,'Charter flight','Player Action',
                                                   'The '+self.Name+' can discard the city card of '+
                                                   'their location to move to any city.']
        if self.CheckShuttleFlight():
            availableactions.loc['ShuttleFlight']=[self.ShuttleFlight,'Shuttle flight','Player Action','The '+self.Name+
                                                   ' can move to any other city with a research station.']
        if self.CheckBuildRS():
            availableactions.loc['BuildRS']=[self.BuildRS,'Build a research station','Player Action',
                                             'The '+self.Name+' can discard the city card of their location to '+
                                             'build a research station in there.']
        if self.CheckTreatDisease():
            availableactions.loc['TreatDisease']=[self.TreatDisease,'Treat disease','Player Action',
                                                  'The '+self.Name+' can remove one disease counter from their '+
                                                  'location. If the chosen disease is cured, remove all the counters of '+
                                                  'that color.']
        if self.CheckGetKnowledge():
            availableactions.loc['GetKnowledge']=[self.GetKnowledge,'Get knowledge','Player Action',
                                                  'The '+self.Name+' can get the city '+
                                                  'card of their location from other player in that location.']
        if self.CheckGetKnowledgeRes():
            availableactions.loc['GetKnowledgeRes']=[self.GetKnowledgeRes,'Get knowledge from the researcher','Class Action',
                                                     'The '+self.Name+' can get any city card from the researcher.']
        if self.CheckGiveKnowledge():
            availableactions.loc['GiveKnowledge']=[self.GiveKnowledge,'Give knowledge','Player Action',
                                                   'The '+self.Name+' can give the '+
                                                   'city card of their location to other player in that location.']
        if self.CheckDiscoverCure():
            availableactions.loc['DiscoverCure']=[self.DiscoverCure,'Discover a cure','Player Action','The '+self.Name+' can discover the'+
                                                  ' cure of a disease by discarding 5 cards of that color.']
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