# PdfScrape

## Dependencies
NEED TO LIST ALL THE PYTHON LIBRARIES HERE

## Video tutorial

Check out the [screen cast video](https://github.com/COMET-NLP-Group/Repository/blob/main/PdfScrapeTutorial-2021-05-27.mp4) detailing how to set up and run the program.

## Program initialization

The program is currently set-up to run from the local path `D:\PdfScrape\`. 

Input a list of URLS into `script_1` that
you would like to scrape PDFs from. 

With no input list the program will use the `Plans.html`
file to scrape the table located at https://ecos.fws.gov/ecp/report/species-with-recovery-plans.

All outputs from this program are written to a `out` directory.

## Script descriptions

### `script_1`

**Input:**
1. A list of urls
2. User must click 'download' from the nltk dialogue box that opens up and exit the dialogue box after it finishes
   before the program will continue to run

This script will take the input urls and scrape any PDF found at that location. The PDF is read in and text 
extracted. Once the text is extracted stops words, punctuation, and digits are stripped from the file.
Script_1 automatically executes script_2.

**Output:**

The cleaned PDF(s) is/are then written to an output directory located in the program folder called 'docs'.
This is the raw text from the PDF minus extraneous sentence parts. 

### `script_2`

**Input:**
1. Boolean - indicate if user would like a frequency plot of the nouns and verbs isolated from 'docs' created and written to file
2. Boolean - indicate if user would like intermediate files to be written out for further analysis. We recommend write_out=True if
	     user wishes to conduct more analysis or use the TSNE script.
3. Key Phrases - a string or list of strings containing key phrases to focus the analysis on

Uses the output generated in `script_1`. Text files from `docs` and are read in as a list of strings. Elements
in the text files (individual words) are tokenized and assigned a tag indicating what part of speech i.e. verb or noun
the word is. A new list is created using verbs and nouns that are extracted from the tokenized lists. Key phrases are
split into individual words which are used to create 'keys'. For example the key phrase 'silt curtain' would be partitioned
into 'silt' and 'curtain'. The PDFs are then iteratively searched for every occurance of a key i.e. 'silt'. When a key is 
identified in a sentence of a PDF we use the key index to extract 200 words surrounding the key creating a 'key word set'.
Each 'key word set' is added to a dictionary like list which holds the text surrounding every instance of a key within
a group of PDFs. Once the PDFs have been searched for all key words and all the associated text has been extracted we count
how many individual words are associated with each key. This number is called 'KeyCount'. Then for each key we count the
number of times unique words within the 'key word set' appear. For example, 'silt' may have a total of 1000 words (KeyCount) 
and of that 1000 words there may be 200 unique words. We count how many times each unique word within a 'key word set' is used
this is called 'WordCount'. A scatter plot is then created; X=KeyCount Y=WordCount. Each point on the scatterplot represents a
word in a 'key word set'. A point's placement along the Y-axis indicates how many times that word was used within a key group and
the placement of a point along the X-axis indicates which key group it belongs to. 

**Output:**
1. Text files: Three directories are created which hold output text files `doc_sent_parts`, `KeyDict`, and `tidy`. 
	+ `doc_sent_parts` - Parts of speech from the text of each PDF are extracted and written to a text file in the 
			   form of (`word`,`part of speech`) i.e. (`go`,`VB`) 
	+ `KeyDict` 	 - Contains a text file of all the words associated with a key. Text files are created for every instance
		    	   of a key found in a PDF. File names contain the key word and the file contains the words from the PDF
		    	   that surrounded the key.
	+ `tidy` 		 - Contains formatted csvs that are analysis ready. `KeyVal_Formatted_DF.csv` contains 4 columns; `key`,
			   `value`, `KeyCount`, `WordCount`. The column `key` indicates the key word used to search PDFs. The column
			   `value` contains individual words that were associated with a given `key`. `KeyCount` is the total number
			   of entries in `value` that have the same `key`. `WordCount` is the number of times `value` appears in `key`

2. Plots: Two plots are generated from `script_2`.
	
	`Key_PseudoClustering.png` - 	A grouped scatter plot created from `KeyCounts` and `WordCount`. Each set of points stacked vertically
					represents all the words associated with a `key`. Each point in a vertically stacked set represents an
					individual word. The location of a point on the Y-axis indicates the number of times that word appeared.
					`KeyCount` is plotted in ascending order allowing the user to identify which `key(s)` is/are the most frequently 
					used across all PDFs. Key groups and words in key groups can be further analyzed using the data frame 
					`KeyVal_Formatted_DF.csv`.

	`FrequencyPlot.png`	   -	A word frequency plot that uses only the verbs and nouns pulled from the input PDFs. 	

### `TSNE`

**Input:**

perplexity: 			The perplexity to use for the TSNE. Perplexity can be loosely associated with number of neighbors for an individual point.

`KeyVal_Formatted_DF.csv`: 	The data frame generated in `script_2` and found in the `tidy` directory

User defined variables:		The user can choose to map colors onto the TSNE using key word phrases in order to see sub-clustering patterns

This script allows the user to visually analyze text clustering patterns from the input PDFs. The input data frame `KeyVal_Formatted_DF.csv` is used to 
generate component arrays, which are then rejoined to the corresponding key-value pair in `KeyVal_Formatted_DF.csv`. The resulting data frame (concat1) is written
out to the `tidy` directory using the perplexity score in the file header. If the user wishes to further understand the clustering patterns observed from the TSNE
there is the option to add a new column to `concat1` which combines keys back into their original phrasing. This column is then used to color code the data points
on the TSNE. 

**Output:**
	
The output TSNE scatterplot shows the clustering pattern of PDF text along two dimensions: keys and words. Each point on the plot is a word which is 
			associated with key. Group membership for any given point on the plot is determined by the key therefore there may be multiple points on 
			the plot with the same value. For example if there were ten points on the scatterplot there might be 5 points all with the value 'go'. 
			However, each instance of 'go' is associated with a different key word i.e. 'silt', 'curtain', 'engineering', 'dam', 'culvert'. The user
			can choose to map colors to the key group or to the individual words by entering the appropriate information into lines 38-46. It is important
			to remember that the TSNE algorithm clustered the data based on the counts - or the frequency of use - of keys and words the color mapping shows
			how key groups/words were clustered by the TSNE. In the 'examples' folder contained in the program directory you will find example TSNE plots generated 
			using ~1500 PDFs from the fish and wildlife services. Key groups that are clustered together indicate similarities in terms of frequency and content. This
			allows the user to understand how often keys appeared in the text and what other keys appear with similar frequency. Isolating these groups allows contextual
			understanding of key phrases and the similarities in the content surrounding each key. Combined with the data and plot from the pseudo-clustering in script_2
			thematic analysis of text can be conducted.

## Examples

**Plots:**	

This folder contains example output plots from each step of the processing. The TSNE plots are depicted with two different perplexity scores 30 and 200. For each perplexity score there is a second plot that depicts a zoomed in area of the larger plot.

