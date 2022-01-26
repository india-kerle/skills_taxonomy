"""
Builds a weighted, undirected network of essential skill pairs 
from occupations data. Saves network locally as pickle file. 

In activated conda environment, run python build_network.py 
"""
#####################################################################

import itertools
from collections import Counter
import networkx as nx
import pandas as pd

from utils.utils import (
    PROJECT_DIR,
    CONFIG_PATH,
    DATA_OUTPUTS_PATH,
    get_yaml_config,
    save_data,
    load_data)

#####################################################################


def build_skills_network(occupations_data, edgeweight_prune_threshold):
    """Builds undirected, weighted network of essential skill pairs
    from occupations data.

    Args:
        occupations_data (dict): A dictionary of ESCO occupations 
        and skills data. 
        edgeweight_prune_threshold (int): the minimum number of job titles
        the skills cooccur in.  

    Returns:
        An undirected, weighted networkx graph. 

    """
    occupations = list(occupations_data.keys())
    all_pairs = []

    for occupation in occupations:
        job = occupations_data[occupation]
        if "hasEssentialSkill" in job['_links'].keys():
            required_skills = [x['title']
                               for x in job['_links']['hasEssentialSkill']]
            sorted(required_skills)
            pairs = list(itertools.combinations(required_skills, 2))
            all_pairs.append(pairs)
        else:
            print("skills that have no hasEssentialSkill: ", occupation)

    all_pairs = Counter(itertools.chain(*all_pairs)).most_common()

    # create dataframe for network

    skill_pairs = [(record[0][0], record[0][1], record[1])
                   for record in all_pairs]
    skill_df = pd.DataFrame(skill_pairs, columns=['node1', 'node2', 'weight'])

    # hacky way to deal with directionality issues - add the weights together
    skill_df_copy = skill_df.copy()
    node1list = skill_df['node1']
    node2list = skill_df['node2']
    skill_df_copy['node1'] = node2list
    skill_df_copy['node2'] = node1list

    skill_df_final = skill_df_copy.append(skill_df)
    skill_df_final = skill_df_final.groupby(['node1', 'node2']).sum().reset_index()

    # skills that cooccur in at least n job titles
    skill_df_pruned = skill_df_final[skill_df_final['weight'] > edgeweight_prune_threshold]

    # create weighted network with data
    G = nx.from_pandas_edgelist(skill_df_pruned, source='node1',
                                target='node2',
                                edge_attr='weight')

    return G


def prune_skills_network(G, bad_coefs):
    """Prunes undirected, weighted network of essential skill pairs
    based on clustering coefficients. Removes nodes with low clustering
    coefficients i.e. highly transversal skills.  

    Args:
        G (graph): An undirected, weighted networkx graph.   
        bad_coefs (int): a low clustering coefficient threshold, based
        on clustering coefficient histogram.  

    Returns:
        An undirected, weighted networkx graph. 

    """
    clustering_coefs = nx.clustering(G)

    # subset clusterng coefs based on being v low i.e. highly transversal skills
    nodes = list(clustering_coefs.keys())
    # graph clustering coef values to choose bad_coef
    pd.DataFrame(list(clustering_coefs.values())).plot.hist()

    clustering_coefs_to_get_rid_of = []
    for node in nodes:
        if clustering_coefs[node] < bad_coefs:  # based on plot
            clustering_coefs_to_get_rid_of.append(
                {node: clustering_coefs[node]})

    clustering_coefs_to_get_rid_of = {
        k: v for el in clustering_coefs_to_get_rid_of for k, v in el.items()}
    
    print(f'removing {len(clustering_coefs_to_get_rid_of)} nodes based on clustering coef')

    # remove skill nodes based on clustering coef
    bad_skills = list(clustering_coefs_to_get_rid_of.keys())
    G.remove_nodes_from(bad_skills)

    return G

if __name__ == "__main__":

    # get config file with relevant paramenters
    config_info = get_yaml_config(CONFIG_PATH)
    # path for occupation data
    data_path = config_info['occupations_data_path']
    # threshold for edge weight
    edgeweight_threshold = config_info['edgeweight_prunethreshold']
    # bad coefs based on graph
    bad_coefs = config_info["bad_coefs"]
    # graph file name
    skills_graph_name = config_info["skills_graph_name"]

    occupations_data = load_data(str(PROJECT_DIR) + data_path)
    skills_network = build_skills_network(
        occupations_data, edgeweight_threshold)
    pruned_skills_network = prune_skills_network(skills_network, bad_coefs)

    # save pruned graph locally
    save_data(pruned_skills_network, str(
        DATA_OUTPUTS_PATH) + skills_graph_name)
