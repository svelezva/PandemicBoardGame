# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 19:49:58 2021

@author: Velez
"""

import pandas as pd
import random
from CardClasses import *

Coords=pd.read_csv('coords.csv')
Adjacency=pd.read_csv('adjacency.csv',index_col='City')
EventsInfo=pd.read_csv('events.csv',index_col=0)

def get_adjacent(row):
    liste=[]
    for city in Coords['City']:
        if Adjacency.loc[row['City'],city]==1:
            liste.append(city)
    return liste

def set_board():
    Bd=pd.DataFrame()
    Bd[['City','Disease']]=Coords[['City','Disease']]
    Bd['Adjacency']=Bd.apply(get_adjacent,axis=1)
    
    #Does the city have a research station:
    Bd['RS']=False
    
    #Counters for every disease
    Bd['Blue']=0
    Bd['Red']=0
    Bd['Yellow']=0
    Bd['Black']=0
    
    #List of players in each city
    Bd['Players']=[[] for i in range(48)]
    
    # Is the city under quarantine? (from the quarantine specialist).
    Bd['Quarantine']=False
    
    # Is the medic in this city?
    Bd['Medic']=False
    
    Bd.set_index('City',inplace=True)
    return Bd

def set_gamestate():
    # Possible values for the diseases are 'Active', 'Cured' and 'Erradicated'.
    GS=pd.Series({'Win':False,
                  'Loss':False,
                  'Players':[],
                  'Outbreaks':0,
                  'Rate':2,
                  'Blue':'Not cured',
                  'Red':'Not cured',
                  'Yellow':'Not cured',
                  'Black':'Not cured',
                  'AmountCured':0,
                  'BlueCubes':24,
                  'RedCubes':24,
                  'YellowCubes':24,
                  'BlackCubes':24,
                  'AvailableRS':6,
                  'Epidemic':0,
                  'SkipInfection':False})
    return GS


def set_ID():
    #ID stands for infection deck
    #IDD stands for infection discard deck
    
    ID=[]
    for i in range(48):
        ID.append(InfectionCard(Coords.loc[i,'City'],Coords.loc[i,'Disease']))
    random.shuffle(ID)
    IDD=[]
    return (ID,IDD)


def set_PD():
    #PD stands for player deck
    #PDD stands for player discard deck
    PD=[]
    PDD=[]
    Events=[]
    for i in range(48):
        PD.append(CityCard(Coords.loc[i,'City'],Coords.loc[i,'Disease']))
    for i in range(5):
        card=EventCard(EventsInfo.loc[i,'Name'],EventsInfo.loc[i,'Description'])
        PD.append(card)
        Events.append(card)
    random.shuffle(PD)
    return (PD,PDD,Events)

Board=set_board()
GameState=set_gamestate()
PD,PDD,Events=set_PD()
ID,IDD=set_ID()