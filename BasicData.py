# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 20:29:05 2021

@author: Velez
"""

import pandas as pd
coords=pd.DataFrame([['San Francisco',-122.3,37.8,'Blue'],
                    ['Chicago',-87.8,41.9,'Blue'],
                    ['Atlanta',-84.5,33.8,'Blue'],
                    ['Montreal',-73.7,45.5,'Blue'],
                    ['Washington',-77.2,38.9,'Blue'],
                    ['New York',-74.1,40.7,'Blue'],
                    ['Madrid',-3.8,40.4,'Blue'],
                    ['London',-0.3,51.5,'Blue'],
                    ['Paris',2.2,48.9,'Blue'],
                    ['Essen',7.1,51.5,'Blue'],
                    ['Milan',9.2,45.5,'Blue'],
                    ['St. Petersburg',30.3,59.9,'Blue'],
                    ['Beijing',116.2,39.9,'Red'],
                    ['Seoul',126.8,37.6,'Red'],
                    ['Shanghai',121.2,31.3,'Red'],
                    ['Tokyo',139,36,'Red'],
                    ['Bangkok',100.2,13.7,'Red'],
                    ['Hong Kong',114,22.3,'Red'],
                    ['Taipei',121.4,25,'Red'],
                    ['Osaka',136,34,'Red'],
                    ['Jakarta',106.6,-6.2,'Red'],
                    ['Ho Chi Minh City',106.5,10.8,'Red'],
                    ['Manila',121.2,14.5,'Red'],
                    ['Sidney',151,-33.9,'Red'],
                    ['Los Angeles',-118,34,'Yellow'],
                    ['Mexico City',-99,19.4,'Yellow'],
                    ['Miami',-80.4,25.8,'Yellow'],
                    ['Bogota',-73.9,4.7,'Yellow'],
                    ['Lima',-76.8,-12.1,'Yellow'],
                    ['Sao Paulo',-46.4,-23.5,'Yellow'],
                    ['Santiago',-70.5,-33.5,'Yellow'],
                    ['Buenos Aires',-58.5,-34.6,'Yellow'],
                    ['Lagos',3.3,6.5,'Yellow'],
                    ['Khartoum',32.8,15.5,'Yellow'],
                    ['Kinshasa',15.1,-4.4,'Yellow'],
                    ['Johannesburg',28,-26.2,'Yellow'],
                    ['Moscow',37.4,55.8,'Black'],
                    ['Istanbul',28.9,41,'Black'],
                    ['Tehran',51.2,35.7,'Black'],
                    ['Algiers',2.9,36.7,'Black'],
                    ['Cairo',31.1,30.1,'Black'],
                    ['Baghdad',44.3,33.3,'Black'],
                    ['Karachi',66.9,24.9,'Black'],
                    ['Delhi',77.2,28.6,'Black'],
                    ['Kolkata',88.3,22.6,'Black'],
                    ['Riyadh',46.6,24.7,'Black'],
                    ['Mumbai',72.8,19.1,'Black'],
                    ['Chennai',80.2,13.1,'Black']],
                    columns=['City','Lon','Lat','Disease'])
coords.to_csv(r'C:/Users/gantz/OneDrive/Desktop/Pandemic/Improved Pandemic/coords.csv',index=False)

Adjacency=pd.DataFrame(columns=range(48),index=range(48))
Adjacency.fillna(0,inplace=True)

#We put the ones in the upper half of the matrix
Adjacency.loc[0,1]=1
Adjacency.loc[0,15]=1
Adjacency.loc[0,22]=1
Adjacency.loc[0,24]=1

Adjacency.loc[1,2]=1
Adjacency.loc[1,3]=1
Adjacency.loc[1,24]=1
Adjacency.loc[1,25]=1

Adjacency.loc[2,4]=1
Adjacency.loc[2,26]=1

Adjacency.loc[3,4]=1
Adjacency.loc[3,5]=1

Adjacency.loc[4,5]=1
Adjacency.loc[4,26]=1

Adjacency.loc[5,6]=1
Adjacency.loc[5,7]=1

Adjacency.loc[6,7]=1
Adjacency.loc[6,8]=1
Adjacency.loc[6,29]=1
Adjacency.loc[6,39]=1

Adjacency.loc[7,8]=1
Adjacency.loc[7,9]=1

Adjacency.loc[8,9]=1
Adjacency.loc[8,10]=1
Adjacency.loc[8,39]=1

Adjacency.loc[9,10]=1
Adjacency.loc[9,11]=1

Adjacency.loc[10,37]=1

Adjacency.loc[11,36]=1
Adjacency.loc[11,37]=1

Adjacency.loc[12,13]=1
Adjacency.loc[12,14]=1

Adjacency.loc[13,14]=1
Adjacency.loc[13,15]=1

Adjacency.loc[14,15]=1
Adjacency.loc[14,17]=1
Adjacency.loc[14,18]=1

Adjacency.loc[15,19]=1

Adjacency.loc[16,17]=1
Adjacency.loc[16,20]=1
Adjacency.loc[16,21]=1
Adjacency.loc[16,44]=1
Adjacency.loc[16,47]=1

Adjacency.loc[17,18]=1
Adjacency.loc[17,21]=1
Adjacency.loc[17,22]=1
Adjacency.loc[17,44]=1

Adjacency.loc[18,19]=1
Adjacency.loc[18,22]=1

Adjacency.loc[20,21]=1
Adjacency.loc[20,23]=1
Adjacency.loc[20,47]=1

Adjacency.loc[21,22]=1

Adjacency.loc[22,23]=1

Adjacency.loc[23,24]=1

Adjacency.loc[24,25]=1

Adjacency.loc[25,26]=1
Adjacency.loc[25,27]=1
Adjacency.loc[25,28]=1

Adjacency.loc[26,27]=1

Adjacency.loc[27,28]=1
Adjacency.loc[27,29]=1
Adjacency.loc[27,31]=1

Adjacency.loc[28,30]=1

Adjacency.loc[29,31]=1
Adjacency.loc[29,32]=1

Adjacency.loc[32,33]=1
Adjacency.loc[32,34]=1

Adjacency.loc[33,34]=1
Adjacency.loc[33,35]=1
Adjacency.loc[33,42]=1

Adjacency.loc[34,35]=1

Adjacency.loc[36,37]=1
Adjacency.loc[36,38]=1

Adjacency.loc[37,39]=1
Adjacency.loc[37,40]=1
Adjacency.loc[37,41]=1

Adjacency.loc[38,41]=1
Adjacency.loc[38,42]=1
Adjacency.loc[38,43]=1

Adjacency.loc[39,40]=1

Adjacency.loc[40,41]=1
Adjacency.loc[40,45]=1

Adjacency.loc[41,42]=1
Adjacency.loc[41,45]=1

Adjacency.loc[42,43]=1
Adjacency.loc[42,45]=1
Adjacency.loc[42,46]=1

Adjacency.loc[43,44]=1
Adjacency.loc[43,46]=1
Adjacency.loc[43,47]=1

Adjacency.loc[44,47]=1

Adjacency.loc[46,47]=1

#We make the matrix symmetric.
for i in range(48):
    for j in range(i+1):
        Adjacency.loc[i,j]=Adjacency.loc[j,i]

Adjacency.columns=coords['City']
Adjacency.index=coords['City']
Adjacency.to_csv(r'C:/Users/gantz/OneDrive/Desktop/Pandemic/Improved Pandemic/adjacency.csv')

Ev=pd.DataFrame([['Airlift','Move one player to any city.'],
                 ['Forecast','Look at the top 6 cards of the infection deck, rearrange them and put them back on top.'],
                 ['Government Grant','Build a research station in any city.'],
                 ['One Quiet Night','Skip the next infection step.'],
                 ['Resilient Population','Remove one card in the infection discard pile from the game.']],
                columns=['Name','Description'])
Ev.to_csv(r'C:/Users/gantz/OneDrive/Desktop/Pandemic/Improved Pandemic/events.csv')