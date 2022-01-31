# Recurse Application: Building a Skills Taxonomy

## Introduction

This repo contains source code for generating a skills taxonomy, using data from the [European Commission's ECSO](https://ec.europa.eu/esco/portal/home), a multilingual classification of European Skills, Competences, Qualifications and Occupations. 

An overview of the network analysis driven methodology, colored by three main steps, can be visualised below:

<img width="780" alt="skills-steps" src="https://user-images.githubusercontent.com/46863334/151831932-f74d5954-9035-43f4-9137-53d54baf2043.png">

There are **three ways** to get a sense of this project, to accomodate the varying degrees of technical knowledge. From most comfortable to least comfortable:
1. ***Replicate the analysis.*** Follow the **Set Up** then **Pipeline Steps** section to replicate the analysis. Comb through the central ```.py``` files to follow along the pipeline.
2. ***Read the technical report.*** If you're not keen to read code, read the ```technical_methodlogy.pdf``` to get a sense of how I went about building a skills taxonomy, including how I made sense of the problem; how I built an understanding of the data; the approach I landed on and how I assessed my solution.
3. ***Explore the skill clusters*** If reading a technical report feels like a drag, [visit the deployed streamlit app](https://share.streamlit.io/india-kerle/skills_taxonomy/main/src/visualise_network.py) to visualise the network and to get a sense of what the clusters look like.

 ![streamlitskills](https://user-images.githubusercontent.com/46863334/151831044-86c22636-7543-49e0-b6ad-1d4aeaf64645.gif)
<center>*example of how to use the streamlit app.*</center>          

## Set up 

1. Clone the git repo - ```git clone https://github.com/india-kerle/skills_taxonomy.git```
2. Create your conda environment - ```conda create --name skills_taxonomy```
3. Activate your conda environment -  ```conda activate skills_taxonomy```
4. (at the repo base) install dependencies - ```pip install -r requirements.txt```
5. Run the above scripts to replicate the analysis! Or, if you would simply like to investigate the skill clusters, visit the [deployed streamlit app](https://share.streamlit.io/india-kerle/skills_taxonomy/main/src/visualise_network.py) here to visualise the network. 

## Pipeline steps

The central steps taken are in three separate ```.py``` files in the ```src``` folder:

1. ```build_network.py``` - Builds a weighted, undirected network of essential skill pairs from occupations data. Saves network locally as pickle file. To run the script in your activated conda environment, ```python run build_network.py```. 

2. ```cluster_network.py```- Clusters and labels clusters of a weighted, undirected network of essential skill pairs from occupations data. Saves clustered network locally as pickle file. To run the script in your activated conda environment, ```python run build_network.py```

3. ```visualise_network.py```- visit the [deployed streamlit app](https://share.streamlit.io/india-kerle/skills_taxonomy/main/src/visualise_network.py) here to visualise the network. To run the script in your activated conda environment, ```streamlit run visualise_network.py```.
