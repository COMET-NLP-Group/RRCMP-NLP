# Reducing Redundancy in Coastal Management Using Natural Language Processing

A Python natural language processing program for identifying key words and phrases in conservation management plans.

## The Driving Questions
1. Can we identify common themes / conservation measures among management plans?
2. Can we capture values and interests of plans’ authors?

## Approach

The PdfScrape program processes PDFs hosted online into various analysis ready data, and performs some initial, exploratory visualizations of common words and their connections. 


## Project Status

Initial development focused on coastal management plans for the state of Washington. 

Contained within this repository are:

+ A [complied list of URLs](https://raw.githubusercontent.com/COMET-NLP-Group/Repository/main/PdfScrape/inputs/management-plan-urls.txt) for the management plans.

+ Various (analysis ready versions)[https://github.com/COMET-NLP-Group/Repository/tree/main/PdfScrape/FWLS_Data] of Fish & Wildlife Species Recovery Plans PDFs

+ Exploratory visualizations of common words and their connections (see below)

+ The PdfScrape program & video tutorial explaining how to use the program for your own list of PDF URLs.

## Example visualizations

#### Frequency plots of most common verbs and nouns

![FrequencyPlotNounsVerbs](https://raw.githubusercontent.com/COMET-NLP-Group/Repository/main/PdfScrape/examples/FishWildLife_ALL_Pdf_FreqNounsVerbs_1.png)

#### Pseudo-clustering

For user-specified key words, the pseudo-clustering plot shows the relationship between the word count for each key word (`KeyCount`) and the word count for the words surrounding / co-occurring with the key word (`WordCount`). Further details provided in the [PdfScrape README](https://github.com/COMET-NLP-Group/Repository/tree/main/PdfScrape)


![pseudocluster](https://raw.githubusercontent.com/COMET-NLP-Group/Repository/main/PdfScrape/examples/KeyWordCount_PseudoClustering_1.png)

#### TSNE (t-distributed stochastic neighbor embedding)

Visually analyze text clustering patterns from the input PDFs

![tsne](https://raw.githubusercontent.com/COMET-NLP-Group/Repository/main/PdfScrape/examples/TSNE_Perp30_4xKeyPhrases.png)
