# pumping-lemma-calculator

This projects provides a calculator for formal language regularity, based on randomizing the pumping lemma's variables.

## Contents
* graphs/ - ellbow and cluster graphs for the inputs in the repo
* .gitignore
* Makefile
* Pumping_Lemma_Calculator.pdf - paper
* README.md
* clustering.py - clustering module
* conditions.g4 - antlr4 grammar for language conditions
* csv_sort.py - csv sorting module
* data_gatherer.py - data gathering module
* inputs - 59 languages on which the paper is based
* main.py - the calculator
* parser.py - parser interface used by the calculator
* scss.pptx - presentation support in Romanian for UPB's 2020 Students' Scientific Communications Session

## How to use
### Calculator
```
python3 main.py
```
You will then need to provide a language to be evaluated.
It is important that you do not leave spaces. Make sure that alphabet symbols are lower case and variables are upper case.
E.g.: 
* a^N|.
* a^N|N<5.
* a\^Nb^M|N>M,M>5.

The output will serve for tracking the process and will, at the end, give the answer.
If you wish, you can chose from the 3 possible configurations by setting the conf variable.
By default, the second configuration is used, which provides balanced results.

### Data gathering
```
python3 data_gatherer.py
```
The module will take a file describing languages, such as the included ```inputs``` file and run the calculator on each language a number of times. The results will be averaged and written to a csv file.
The csv file will have the following columns:
* language description
* number of characters
* number of variables
* number of conditions
* value of *k* when the calculator stops
* number of words *w* tried when the calculator stops
* result: regular/non-regular, 0/1
* correct response: regular/non-regular, 0/1

### Sorting the csv file
This step is not necessary, but if you want to order your languages based on a particular characteristic, you can.
```
python3 csv_sort.py
```


### Clustering
```
python3 clustering.py
```
k-means will be run on the specified columns of the csv input file.


### Parser
This is used by the calculator for checking the conditions and should not be interacted with directly.


## Dependencies
The project was developed in Python 3.6.9 with the corresponding antlr4 version for parsing of the conditions.


