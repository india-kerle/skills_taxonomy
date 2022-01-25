"""
Clusters and labels clusters of a weighted, undirected network of 
essential skill pairs from occupations data.

Saves clustered network locally as pickle file.  

In activated conda environment, run python cluster_network.py 
"""
#####################################################################

from community import community_louvain
from collections import Counter
import itertools
import networkx as nx

from utils.utils import (
    DATA_OUTPUTS_PATH,
    CONFIG_PATH,
    get_yaml_config,
    preprocess_skills,
    load_data,
    save_data)

#####################################################################


def detect_skills_communities(G):
    """Hierarchically clusters undirected, weighted network of 
    essential skill pairs using a louvain community detection 
    algorithm. 

    Args:
        G (graph): An undirected, weighted networkx graph.   

    Returns: 
        G (graph): An undirected, weighted networkx graph with 
        'cluster group', 'cluster_subgroup0', 'cluster_subgroup1',
        'cluster_subgroup2' node attributes.

        node_attributes (dict): A dictionary of node attributes 
        associated to each node.

    """

    # run community detection algorithm on network
    dendo = community_louvain.generate_dendrogram(
        G, random_state=42, resolution=1)

    dendo_cluster_dict = {}
    all_skills = list(G.nodes())

    for skill in all_skills:
        cluster_id = ''
        for level in range(len(dendo)):
            cluster_id_at_level = community_louvain.partition_at_level(dendo, level)[
                skill]
            cluster_id = cluster_id + '-' + str(cluster_id_at_level)

        # flip hierarchy to largest cluster first
        hierarchy = cluster_id[1:]
        reverse_hierarchy = "-".join(hierarchy.split('-')[::-1])

        dendo_cluster_dict[skill] = {'cluster_group': reverse_hierarchy,
                                     'cluster_subgroup0': reverse_hierarchy.split('-')[0],
                                     'cluster_subgroup1': reverse_hierarchy.split('-')[1],
                                     'cluster_subgroup2': reverse_hierarchy.split('-')[2]

                                     }

    for node, node_attributes in dendo_cluster_dict.items():
        G.nodes[node]['cluster_group'] = node_attributes['cluster_group']
        G.nodes[node]['cluster_subgroup0'] = node_attributes['cluster_subgroup0']
        G.nodes[node]['cluster_subgroup1'] = node_attributes['cluster_subgroup1']
        G.nodes[node]['cluster_subgroup2'] = node_attributes['cluster_subgroup2']

    # returns both network and node attributes per node
    node_attributes = {key for nodes in dendo_cluster_dict.values()
                       for key in nodes}

    return G, node_attributes


def label_skills_communities(G, cluster_granularity, top_n):
    """Labels clusters per cluster granularity based on top n terms.  

    Args:
        G (graph): An undirected, weighted networkx graph with cluster
        group node attributes.   
        cluster_granularity (str): cluster granularity to label i.e. 'cluster_subgroup0'.  
        top_n (int): top n terms i.e. 5. 

    Returns: 
        G (graph): An undirected, weighted networkx graph with cluster
        group and cluster group name node attributes. 

    """
    unique_cluster_ids = list(
        set([node[1] for node in G.nodes(data=cluster_granularity)]))
    cluster_names = {}

    for cluster_id in unique_cluster_ids:
        cluster_words = [node[0] for node in G.nodes(
            data=cluster_granularity) if node[1] == cluster_id]
        token_list = preprocess_skills(cluster_words)
        flat_list = list(itertools.chain(*token_list))
        word_counts = Counter(flat_list).most_common()
        top_n_words = [x[0] for x in word_counts[0:top_n]]
        cluster_description = " | ".join(top_n_words)
        cluster_names[cluster_id] = cluster_description

    node_cluster_names = dict(zip(list(G.nodes()),
                                  [cluster_names[G.nodes[n][cluster_granularity]] for n in G.nodes]))

    nx.set_node_attributes(G, node_cluster_names,
                           cluster_granularity + '_name')

    return G


def evaluate_skills_communities(G, cluster_granularity):
    """Calculates and prints overall graph and cluster modularity.   

    Args:
        G (graph): An undirected, weighted networkx graph with cluster
        group and cluster group name node attributes.   
        cluster_granularity (str): cluster granularity to label i.e. 'cluster_subgroup0'.  
    """

    # calculate overall modularity at the highest level
    partition = dict(G.nodes(data=cluster_granularity))

    modularity = community_louvain.modularity(partition, G, weight='weight')
    print('overall network modularity: ', round(modularity, 2))

    # calculate modularity per for subgroup and print modularity if modularity not 0
    unique_clusters = list(
        set(list(dict(G.nodes(data='cluster_subgroup0')).values())))

    for unique_cluster in unique_clusters:
        nodes = {node: data['cluster_group'] for node, data in G.nodes(
            data=True) if data.get('cluster_subgroup0') == unique_cluster}
        G_subgroup = G.subgraph(list(nodes.keys()))
        modularity = community_louvain.modularity(
            nodes, G_subgroup, weight='weight')
        if modularity != 0:
            print("cluster id: ", unique_cluster,
                  "modularity: ", round(modularity, 2))


if __name__ == "__main__":

    # get config file with relevant paramenters
    config_info = get_yaml_config(CONFIG_PATH)

    skills_graph_path = config_info["skills_graph_name"]
    top_n = config_info['top_cluster_top_names']
    clustered_skills_graph_path = config_info['clustered_skills_graph_name']
    top_cluster_granularity = config_info['cluster_granularity']

    # load network data
    G_skills = load_data(str(DATA_OUTPUTS_PATH) + skills_graph_path)

    # hierarchically cluster skills network
    G_skills_clustered, cluster_granularities = detect_skills_communities(
        G_skills)

    # add cluster labels per cluster granularity
    for cluster_granularity in cluster_granularities:
        label_skills_communities(
            G_skills_clustered, cluster_granularity, top_n)

    # evaluate skill communities
    evaluate_skills_communities(G_skills_clustered, top_cluster_granularity)

    # save clustered network locally
    save_data(G_skills_clustered, str(
        DATA_OUTPUTS_PATH) + clustered_skills_graph_path)
