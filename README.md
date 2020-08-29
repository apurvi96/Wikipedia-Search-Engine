### Wikipedia-Search-Engine
A search engine query over wikipedia data dump of size ~60 GB.
Using inverted Indexing, merging and Ranking Techiniques.

### Features
- Support for Field Queries - Fields include Title, Infobox, Body, Category, Links, and References. This helps when a user is interested in searching for the movie ‘Up’ where he would like to see the page containing the word ‘Up’ in the title and the word ‘Pixar’ in the Infobox
- Index size should be less than one-fourth of the dump size

### Run Files 
1. bash index.sh <path_to_wiki_dump> <path_to_invertedindex_output> <invertedindex_stat.txt>
invertedindex_stat.txt:This file should contain two numbers on separate lines
Total number of tokens (after converting to lowercase) encountered in the dump
Total number of tokens in the inverted index

2. bash search.sh  <path_to_invertedindex_output> query_string

#### Plain query_string examples
Sachin Ramesh Tendulkar
Hogwarts

#### Field query_string examples
t:World Cup i:2019 c:Cricket
search for "World Cup" in Title, "2019" in Infobox and "Sports" in Category

t:the two towers i:1954
search for "the two towers" in Title and "1954" in Infobox 
