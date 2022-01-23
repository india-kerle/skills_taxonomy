from pathlib import Path
from typing import Optional
import yaml
from fnmatch import fnmatch
import json
import networkx as nx
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pickle
import random
import zipfile

# Define project base directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

#Define config file path
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config/base.yaml"

#Define data outputs path
DATA_OUTPUTS_PATH = Path(__file__).resolve().parents[1] / "data/outputs/"


def get_yaml_config(file_path: str) -> Optional[dict]:
    """Fetch yaml config and return as dict if it exists."""
    if file_path:
        with open(file_path, "rt") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)

def load_data(file_path: str):
    if fnmatch(file_path, "*.json.zip"):
        with zipfile.ZipFile(file_path, "r") as z:
            filename = '.'.join(file_path.split('/')[len(file_path.split('/')) - 1].split('.')[:2])
            with z.open(filename) as f:
                data = f.read() 
                return json.loads(data.decode("utf-8"))
    elif fnmatch(file_path, "*.pickle"):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        print(f'{file_path} does not have a supported file extension.')

def save_data(obj, file_name):
    """saves objects to data/outputs."""
    if fnmatch(file_name, "*.pickle"):
        with open(file_name, 'wb') as f:
            return pickle.dump(obj, f)

def get_lemma(word):
    """lemmatise word."""
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def preprocess_skills(word_list):  
    # preprocess terms
    stopwords = nltk.corpus.stopwords.words('english')
    punct = string.punctuation
   
    word_list = [x.lower() for x in word_list] #to lowercase
    word_list = [x.replace(r'\S*\d+\S*', '') for x in word_list] #remove numbers
    token_list = [x.split(" ") for x in word_list]
    token_list = [[y for y in x if y not in punct] for x in token_list]
    token_list = [[y for y in x if y not in stopwords] for x in token_list]
    token_list = [[get_lemma(y) for y in x] for x in token_list]
    
    return token_list    

def add_cluster_colors(G):
    
    cluster_groups = list(set([skill[1] for skill in list(G.nodes(data='cluster_group'))]))
    hex_colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(cluster_groups))]
    
    cluster_colors = dict(zip(cluster_groups, hex_colors))

    node_cluster_colors = dict(zip(list(G.nodes()), 
                                  [cluster_colors[G.nodes[n]['cluster_group']] for n in G.nodes]))
    
    nx.set_node_attributes(G, node_cluster_colors, 'cluster_color')
    
    return G

