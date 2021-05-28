# -*- coding: utf-8 -*-
"""
Created on Wed May 19 08:47:39 2021

@author: mcsha
"""

import os
import nltk as nl
import PyPDF2 
import urllib.request
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from itertools import compress
from datetime import datetime

flatten = lambda t: [item for sublist in t for item in sublist]
def ScrapeRead(url):
            response =  urllib.request.urlopen(path)
            response.decode_content = True
            html = response.read()
            file = open('Test1' + ".pdf", 'wb')
            file.write(html)
            file.close()
            
            pdfFileObj = open('Test1' + ".pdf", 'rb') 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
            out = list(map(lambda x: pdfReader.getPage(x),range(pdfReader.numPages)))
            exclist = string.punctuation + string.digits
            pdf_text = list()
            for i,page in enumerate(out):
                text = page.extractText()
                tokens = [t for t in text.split()]
                clean_tokens = tokens[:]
                for token in tokens:
                    if token in stopwords.words('english') or token in exclist:
                        clean_tokens.remove(token)
                        
                pdf_text.append(clean_tokens)
           
            out1 = flatten(pdf_text)
            pdfFileObj.close()
            return(out1)
            
def ExtractUrls(html_file):
    with(open(html_file,'r')) as plans_file:
        plans_text = BeautifulSoup(plans_file,'html.parser')
        url_tags = plans_text.find_all(href=True)
        urls_0 = list(map(lambda x: x.attrs['href'],url_tags))
        # Isolate the urls ending .pdf
        urls_1 = list(map(lambda x: '.pdf' in x, urls_0))
        urls = list(compress(urls_0,urls_1))
        
    return(urls)

def Strip(pdf_words):
    exclist = string.punctuation + string.digits
    stop_words = stopwords.words('english')
    temp1 = list(map(lambda x: x.lower(),pdf_words))
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = list(map(lambda x: lemmatizer.lemmatize(x), temp1))
    temp2 = list(map(lambda x: x.strip(exclist),lemmatized_words))
    temp3 =  [item for item in temp2 if item != 'et' or item != 'al']
    temp4 = [item for item in temp3 if item not in stop_words]
    return(temp4)

if __name__=='__main__':
   
    os.chdir('D:/PdfScrape')
    
    input_urls = None# ENTER LIST OF URL(S) HERE
    nl.download() # USER INTERFACE REQUIRED TO CONTINUE
    
    # START PROCESS ##########################################################
    os.mkdir('out')
    os.mkdir(os.path.join('out','docs'))
    
    out_docs_path = 'out/docs/'
    if input_urls is not None:
        urls = input_urls
    else:
        html_file = 'inputs/Plans.html' # this will scrape the fish and wild life service WA site
        urls = ExtractUrls(html_file)
    
    big_pdf = list()
    for i,path in enumerate(urls):
        start_url = datetime.now()
        try:
            pages = ScrapeRead(path)
            big_pdf.append(pages)
        except Exception as e:
            print('{}:{}'.format(path,e))
            print(datetime.now()-start_url)
            continue
        print('Time to Process URL {}: {}'.format(i,datetime.now()-start_url))
            
    pdf_list = list(map(lambda x: Strip(x),big_pdf))
    for i,pdf in enumerate(pdf_list):
        with open(os.path.join(out_docs_path,'PDF_{}.txt'.format(i)), 'w') as filehandle:
            for listitem in pdf:
                try:
                    filehandle.write('%s\n' % listitem)
                except Exception as e:
                    print(e)
                    continue
    
    next_script = 'scripts/script_2.py'
    exec(open(next_script).read())




