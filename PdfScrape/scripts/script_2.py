# -*- coding: utf-8 -*-
"""
Created on Sun May 23 10:59:10 2021

@author: mcsha
"""
import os
import matplotlib.pyplot as plt
import nltk as nl
from itertools import compress
from glob import glob
import pandas as pd
import seaborn as sns

flatten = lambda t: [item for sublist in t for item in sublist]

def ReadPaths(path_to_docs):
    paths = glob(os.path.join(doc_holding,'*'))
    temp1 = list(map(lambda x: open(x),paths))
    txt_files_temp = list(map(lambda x: x.readlines(),temp1))

    text = [list(map(lambda x: nl.word_tokenize(x), txt_files_temp[i])) for i in range(len(txt_files_temp))]
    parts = [list(map(lambda x: nl.pos_tag(x),text[i])) for i in range(len(text))]
    parts1 = list(map(lambda x: flatten(x),parts))
    bool_ = [list(map(lambda x: x[1]=='VBP' or x[1]=='VB' or x[1]=='NN',parts1[i])) for i in range(len(parts1))]
    parts2 = flatten(list(map(lambda x,y: list(compress(x,y)),
                       parts1,bool_)))
    return(parts1,parts2)

def IsolateWord(token_list):
    parts4 = list(map(lambda x: x[0], token_list))
    bool_ =list(map(lambda x: len(x)>3,parts4))
    parts5 = list(compress(parts4,bool_))
    return(parts5)

def LowerSplitStr(key_phrase_list):
    kwds2 = list(map(lambda x: x.lower(), key_phrase_list))
    out = flatten(list(map(lambda x: x.split(' '),kwds2)))  
    return(out)

def KeyValueList(split_key_words,sent_parts_list):  
    key_values = [[x+':'] for x in split_key_words]
    for i,key in enumerate(split_key_words):
        
        bool_ = [list(map(lambda x: key in x,sent_parts_list[a])) for a in range(len(sent_parts_list))]
        bool2_ = list(map(lambda x: any(x) is True, bool_))
        idx = list(compress(sent_parts_list,bool2_))
        
        key_text_holding = list()
        for j, pdf in enumerate(idx): # these are all the pdfs with key word == key
            key_bool =  [list(map(lambda x: key in x[0],idx[a])) for a in range(len(idx))]
            key_idx = list(map(lambda x,y: list(compress(range(len(x)),y)),idx,key_bool))
            
            text_holding = list()
            for idxs in key_idx[j]:
                
                if not idxs:
                    continue
                else:
                   if idxs - 100 <=0:
                        to_start = len(pdf[:idxs])
                        to_add = pdf[idxs-to_start:idxs+100]
                        text_holding.append(to_add)
                
                   elif idxs+100>=len(pdf):
                        to_end = len(pdf[idxs::])
                        to_add = pdf[idxs-100:idxs+to_end]
                        text_holding.append(to_add)
                        
                   else: 
                        to_add = pdf[idxs-100:idxs+100]
                        text_holding.append(to_add)
                       
            key_text_holding.append(text_holding)
    
        test = flatten(flatten(key_text_holding))
        sent_parts = list(map(lambda x: x[1]=='VBP' or x[1]=='VB' or x[1]=='NN',test))
        nvbs = list(compress(test,sent_parts))
        words = list(map(lambda x: x[0],nvbs))
    
        key_values[i].append(words)
    return(key_values)

def Convert2DF(key_val_list,split_list_keys):
   # from itertools import compress
    bool_ = list(map(lambda x: len(x)>1,key_val_list))
    key_val_list = list(compress(key_val_list,bool_))
    values_series = list(map(lambda x: pd.DataFrame(pd.Series(x[1],name='value')),key_val_list))
    _nonetype = list(map(lambda x,y: x.insert(0,'key',y,allow_duplicates=False),values_series,split_list_keys))
    out = pd.concat(values_series,axis=0).reset_index().drop('index',axis=1)

    return(out)

def CreateCounts(df):
    word_count = df.groupby('value').size().reset_index()
    word_count.rename(columns={0:'WordCount'},inplace=True)
   
    merge = pd.merge(word_count,df,left_on='value',right_on='value',how='inner')
    merge.drop_duplicates(inplace=True)
   
    keycount = merge.groupby('key').size().reset_index()
    keycount.rename(columns={0:'KeyCount'},inplace=True)
    
    out  = pd.merge(merge,keycount,left_on='key',right_on='key')
    out.sort_values('KeyCount',inplace=True)
    return(out)

if __name__=='__main__':
       
    os.chdir('D:/PdfScrape/')
    
    freq_plot=True
    write_out=True

    kwrds1 = ['Silt curtain','Engineered log jam','Silt screen','ELJ','Sediment curtain','Levee setback',
              'In-water work window','Hardened bank removal','Large woody debris','Culvert replacement',
              'culvert repair','LWD','Dam removal','Bubble curtain','Placement of streambed material',
              'Marbled murrelet monitoring','Dredge spoil dispersal','Fish removal','Dredge spoil deposition',
              'Fish rescue','Placement of large wood']
    
    # Start Process ##########################################################   
    os.mkdir(os.path.join('out','docs_sent_parts'))
    os.mkdir(os.path.join('out','KeyDict'))
    os.mkdir(os.path.join('out','tidy'))
    os.mkdir(os.path.join('out','images'))
    
    doc_holding = 'out/docs/'
    sent_parts_holding = 'out/docs_sent_parts/'
    keys_doc = 'out/KeyDict/'
    key_value_df_path = 'out/tidy/'
    image_path = 'out/images/'

    parts1,parts2 = ReadPaths(doc_holding)
    parts5 = IsolateWord(parts2)
    kwds_split= LowerSplitStr(kwrds1)
    key_vals = KeyValueList(kwds_split,parts1)
    
    concat = Convert2DF(key_vals,kwds_split)
    merge1 = CreateCounts(concat)

    # Create the output plot
    fig,ax=plt.subplots()
    ax = sns.scatterplot(x='KeyCount',y='WordCount',hue='key',data=merge1,palette=sns.set_palette('cividis',n_colors=51),legend='brief')
    text_loc = merge1.KeyCount.tolist()
    ax.legend(ncol=5)
    fig.savefig(os.path.join(image_path,'Key_PseudoClustering.png'),dpi=700)
    
    # Conditional outputs
    if freq_plot:
        fig,ax = plt.subplots()
        ax = nl.FreqDist(parts5)
        ax.plot(100, cumulative=False) 
        fig.savefig(os.path.join(image_path,'FrequencyPlot.png'),dpi=700)
    else:
        pass
    
    if write_out:
        keys = [x for x in ax.keys()]
    
        with open(os.path.join(doc_holding,'FreqKeys.txt'), 'w') as filehandle:
            for listitem in keys:
                try:
                    filehandle.write('%s\n' % listitem)
                except Exception as e:
                    print(e)
                    continue
                
        for i,pdf in enumerate(parts1):
            with open(os.path.join(sent_parts_holding,'SentParts_{}.txt'.format(i)), 'w') as filehandle:
                for listitem in pdf:
                    try:
                        filehandle.write('%s ' % list(listitem)[0])
                        filehandle.write('%s\n' % list(listitem)[1])
                    except Exception as e:
                        print(e)
                        continue 
        
        for i,key_phrases in enumerate(key_vals):
            with open(os.path.join(keys_doc,'KeyDict_{}_{}.txt'.format(key_phrases[0][:-1],i)), 'w') as filehandle:
                    try:
                        filehandle.write('%s' % key_phrases[1])
                    except Exception as e:
                        print(e)
                        continue  
        merge1.to_csv(os.path.join(key_value_df_path,'KeyVal_Formatted_DF.csv'))
    else:
        pass


