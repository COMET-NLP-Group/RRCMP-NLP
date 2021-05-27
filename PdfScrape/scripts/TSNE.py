# -*- coding: utf-8 -*-
"""
Created on Tue May 25 13:55:33 2021

@author: mcsha
"""
import os
import sklearn.manifold as skm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def CreateTSNEdf(df,perp):
    tsne = skm.TSNE(n_components=2, init='random',
                             random_state=0, perplexity=perp)
    Y = tsne.fit_transform(df[['KeyCount','WordCount']])
    y0= pd.Series(Y[0:, 0],name='y0')
    y1= pd.Series(Y[0:, 1],name='y1')
    
    concat = pd.concat([df,y0,y1],axis=1)
    return(concat)

os.chdir('D:/PdfScrape')
perplexity = 200

kwrds1 = ['Silt curtain','Engineered log jam','Silt screen','ELJ','Sediment curtain','Levee setback',
              'In-water work window','Hardened bank removal','Large woody debris','Culvert replacement',
              'culvert repair','LWD','Dam removal','Bubble curtain','Placement of streambed material',
              'Marbled murrelet monitoring','Dredge spoil dispersal','Fish removal','Dredge spoil deposition',
              'Fish rescue','Placement of large wood']

# Read in df and create TSNE DF
input_df = pd.read_csv('out/tidy/KeyVal_Formatted_DF.csv')
concat1 = CreateTSNEdf(input_df,perplexity)
concat1.to_csv('out/tidy/TSNE_KeyValCounts_Perp{}.csv'.format(str(perplexity)))

# Group data by key phrase for color mapping
concat1['KeyGrp']='others'
concat1.loc[(concat1.key == 'silt') | (concat1.key=='curtain') | (concat1.key=='sediment') | (concat1.key=='screen')| (concat1.key=='bubble'),
            'KeyGrp']='silt curtain'
concat1.loc[(concat1.key == 'large') | (concat1.key=='woody') | (concat1.key=='debris') | (concat1.key=='lwd'),
            'KeyGrp']='large woody debris'
concat1.loc[(concat1.key == 'marbled') | (concat1.key=='murrelet') | (concat1.key=='monitoring'),
            'KeyGrp']='marbled murrelet monitoring'
concat1.loc[(concat1.key == 'hardened') | (concat1.key=='bank') | (concat1.key=='removal'),
            'KeyGrp']='hardened bank removal'

# Plot the TSNE data using key phrases to create color scheme
sns.scatterplot(x='y0',y='y1',hue='KeyGrp',data=concat1,palette='nipy_spectral')
