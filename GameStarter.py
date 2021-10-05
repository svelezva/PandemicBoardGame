# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:40:27 2021

@author: Velez
"""

from Roles import *

def SetGame():
    global Board, GameState,PD,PDD,ID,IDD,Events
    GameState['AvailableRS']=5
    Board.loc['Atlanta','RS']=True
    for i in range(9):
        Infect(counters=int((11-i)/3))
        
    classes=[ContingencyPlanner,Dispatcher,Medic,OperationsExpert,QuarantineSpecialist,Researcher,Scientist]
    while True:
        try:
            numberofplayers=int(input('Input the number of players (2-4): '))
        except ValueError:
            print("That is not an integer. Try again!")
            continue
        else:
            if numberofplayers in range(2,5):
                break
            else:
                print('Invalid input')
    activeclasses=random.sample(classes,numberofplayers)
    #print('The current players are:')
    for i in range(numberofplayers):
        activeclasses[i](initialhand=6-numberofplayers)
        #print(GameState['Players'][i].Name)
        
    while True:
        try:
            difficulty=int(input('Input the number of epidemics (4-6): '))
        except ValueError:
            print("That is not an integer. Try again!")
            continue
        else:
            if difficulty in range(4,7):
                break
            else:
                print('Invalid input')
    PD=ShuffleEpidemics(PD,difficulty)
    
def RunGame():
    global Board, GameState,PD,PDD,ID,IDD,Events
    SetGame()
    turncounter=0
    
    while True:
        #display(InfectionDiscardDeck)
        print('\n')
        for card in IDD:
            print(card.name)
        print('\n')
        #display(Board)
        print('\n'+Board[['Disease',
                          'RS',
                          'Blue',
                          'Red',
                          'Yellow',
                          'Black',
                          'Quarantine',
                          'Medic']].to_string()+'\n')
        for Pl in GameState['Players']:
            Pl.Info()
            
        
        activeplayer=GameState['Players'][turncounter]
        activeplayer.StartTurn()
        while activeplayer.Actions>0:
            activeplayer.Info()
            allactions=activeplayer.AvailableActions().copy()
            allactions=allactions.append(AvailableEvents())
            listofactions=allactions['Action'].tolist()
            print('Select an action:')
            selection=Choose(options=listofactions)
            selectionindex=listofactions.index(selection)
            if allactions.iloc[selectionindex]['Type']=='Event':
                allactions.iloc[selectionindex]['Function'](allactions.index[selectionindex])
            else:
                allactions.iloc[selectionindex]['Function']()
            if GameState['AmountCured']==4:
                GameState['Win']=True
                break
        if GameState['Win']:
            finalmessage='You cured all diseases and won the game.'
            break
        turncounter=(turncounter+1)%len(GameState['Players'])
        
        cardsdrawn=0
        while cardsdrawn<2:
            allactions=pd.DataFrame([[activeplayer.Draw,'Draw','Draw','Draw a card from the player deck.']],
                                    columns=['Function','Action','Type','Description'],
                                    index=['Draw'])
            allactions=allactions.append(AvailableEvents())
            listofactions=allactions['Action'].tolist()
            print('Select an action:')
            selection=Choose(options=listofactions)
            selectionindex=listofactions.index(selection)
            if allactions.iloc[selectionindex]['Type']=='Event':
                allactions.iloc[selectionindex]['Function'](allactions.index[selectionindex])
            elif len(PD)==0:
                GameState['Loss']=True
                break
            else:
                allactions.iloc[selectionindex]['Function']()
                cardsdrawn+=1
        if GameState['Loss']:
            finalmessage='The player deck ran out of cards. You lost.'
            break
        
        citiesinfected=0
        while citiesinfected<GameState['Rate']:
            if GameState['SkipInfection']:
                break
            allactions=pd.DataFrame([[Infect,'Infect','Infect a city','Draw a card from the infection deck. Infect that city.']],
                                    columns=['Function','Action','Type','Description'],
                                    index=['Infect'])
            allactions=allactions.append(AvailableEvents())
            listofactions=allactions['Action'].tolist()
            print('Select an action:')
            selection=Choose(options=listofactions)
            selectionindex=listofactions.index(selection)
            if allactions.iloc[selectionindex]['Type']=='Event':
                allactions.iloc[selectionindex]['Function'](allactions.index[selectionindex])
            else:
                allactions.iloc[selectionindex]['Function']()
                citiesinfected+=1
                if GameState['Loss']:
                    break
        if GameState['Loss']:
            finalmessage='You ran out of disease counters. You lost.'
            break
        finish=input('Continue to next turn.')
    print(finalmessage)
    
def main():
    global Board, GameState,PD,PDD,ID,IDD,Events
    while True:
        RunGame()
        print('Do you want to play again?')
        selection=Choose(options=['Yes','No'])
        if selection=='No':
            break
main()