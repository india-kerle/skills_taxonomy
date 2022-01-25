# Recurse Application: Building a Skills Taxonomy

## Introduction

This repo contains source code for generating a skills taxonomy, using data from the [European Commission's ECSO](https://ec.europa.eu/esco/portal/home), a multilingual classification of European Skills, Competences, Qualifications and Occupations. 

An overview of the network analysis driven methodology, colored by three main steps, can be visualised below:

## Pipeline steps

The central steps taken are in three separate .py files in the ```src``` folder:

1. ```build_network.py``` - Builds a weighted, undirected network of essential skill pairs from occupations data. Saves network locally as pickle file. To run the script in your activated conda environment, ```python run build_network.py```. 

2. ```cluster_network.py```- Clusters and labels clusters of a weighted, undirected network of essential skill pairs from occupations data. Saves clustered network locally as pickle file. To run the script in your activated conda environment, ```python run build_network.py```

3. ```visualise_network.py```- visit the [deployed streamlit app](https://share.streamlit.io/india-kerle/skills_taxonomy/main/src/visualise_network.py) here to visualise the network. 

## Set up 

1. Clone the git repo - ```git clone https://github.com/india-kerle/skills_taxonomy.git```
2. Create your conda environment - ```conda create --name skills_taxonomy```
3. Activate your conda environment -  ```conda activate skills_taxonomy```
4. (at the repo base) install dependencies - ```pip install -r requirements.txt```
5. Run the above scripts to replicate the analysis! Or, if you would simply like to investigate the skill clusters, visit the [deployed streamlit app](https://share.streamlit.io/india-kerle/skills_taxonomy/main/src/visualise_network.py) here to visualise the network. 
