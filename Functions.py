# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:03:31 2021

@author: Velez
"""

from Setters import *
from sklearn.model_selection import KFold

def ShuffleEpidemics(deck,amount):
    kf=KFold(n_splits=amount)
    fulldeck=[]
    for rest, chunk in kf.split(deck):
        epidemic=Card('Epidemic '+str(amount),'Epidemic')
        amount-=1
        pdchunk=deck[chunk[0]:chunk[-1]+1]
        pdchunk.append(epidemic)
        random.shuffle(pdchunk)
        fulldeck.extend(pdchunk)
    return fulldeck

def Choose(options='AllCities'):
    global Board
    if options=='AllCities':
        while True:
            choice=input('Type the name of the city: ')
            if choice in Board.index:
                return choice
            else:
                print('Invalid input')
    else:
        for i in range(len(options)):
            print('('+str(i)+') '+options[i])
        while True:
            try:
                choice=int(input('Input the number of your choice: '))
            except ValueError:
                print("That is not an integer. Try again!")
                continue
            else:
                if choice in range(len(options)):
                    return options[choice]
                else:
                    print('Invalid input')
                        
def PlaceDC(location,color,outbreaks):
    #DC stands for disease counter
    global Board, GameState
    cond1= not (GameState[color]=='Erradicated')
    cond2= not Board.loc[location,'Quarantine']
    cond3= not (Board.loc[location,'Medic'] and (GameState[color]=='Cured'))
    cond4= not (location in outbreaks)
    if Board.loc[location,'Quarantine']:
        print(location+' is under quarantine; no disease counters were placed.')
    if Board.loc[location,'Medic'] and (GameState[color]=='Cured'):
        print('The Medic is in '+location+' and the disease is cured. No counters were placed.')
    if GameState[color]=='Erradicated':
        print('The '+color+' disease is erradicated; no counters were placed in '+location+'.')
    if cond1 and cond2 and cond3 and cond4:
        if Board.loc[location,color]<3:
            if GameState[color+'Cubes']==0:
                GameState['Loss']=True
            Board.loc[location,color]+=1
            GameState[color+'Cubes']-=1
        else:
            print('Outbreak in '+location+'!')
            GameState['Outbreaks']+=1
            if GameState['Outbreaks']==8:
                GameState['Loss']=True
            outbreaks.append(location)
            for city in Board.loc[location,'Adjacency']:
                PlaceDC(location=city,color=color,outbreaks=outbreaks)
                
def AvailableEvents():
    heldevents=[card for card in Events if card.holder!='']
    availableevents=pd.DataFrame(columns=['Function','Action','Type','Description'])
    for i in range(len(heldevents)):
        eventname=heldevents[i].name
        cond1 = (eventname=='Government Grant' and GameState['AvailableRS']>0)
        cond2 = (eventname=='Resilient Population' and len(IDD)>0)
        cond3 = (eventname!='Government Grant' and eventname!='Resilient Population')
        if cond1 or cond2 or cond3:
            availableevents.loc[eventname]=[heldevents[i].holder.PlayEvent,
                                            eventname,
                                            'Event',
                                            heldevents[i].description]
    return availableevents

def Infect(counters=1):
    global ID,IDD
    card=ID[-1]
    ID.remove(card)
    IDD.append(card)
    print('Infection in '+card.name+': '+str(counters)+' counters.')
    for i in range(counters):
        PlaceDC(location=card.name,color=card.color,outbreaks=[])
    
