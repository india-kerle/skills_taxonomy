"""
Visualises clustered network on streamlit. 
"""
#####################################################################

import streamlit as st
import networkx as nx
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

from utils.utils import (
    DATA_OUTPUTS_PATH,
    CONFIG_PATH,
    get_yaml_config,
    preprocess_skills,
    add_cluster_colors,
    load_data,
    save_data)

#####################################################################

if __name__ == "__main__":

    # get config file with relevant paramenters
    config_info = get_yaml_config(CONFIG_PATH)
    clustered_skills_graph_path = config_info['clustered_skills_graph_name']
    # load network data
    G_clustered_skills = load_data(
        str(DATA_OUTPUTS_PATH) + clustered_skills_graph_path)

    st.set_page_config(layout="centered")
    st.markdown('<p style="font-family:Courier New; color:Red; font-size: 40px;"><b>Skills Taxonomy Network Tool</b></p>', unsafe_allow_html=True)
    st.markdown('<p style="font-family:Courier New; color:Red; font-size: 30px;"><i>Investigate skills in different skill areas - Select area to explore:</i></p>', unsafe_allow_html=True)

    # select from the different skills clusters
    option = st.selectbox(label='', options=list(set([skill[1] for skill in list(
        G_clustered_skills.nodes(data='cluster_subgroup0_name'))])))

    G_clustered_skills_color = add_cluster_colors(G_clustered_skills)

    nodes = []
    edges = []

    for skill in G_clustered_skills_color.nodes(data=True):
        if skill[1]['cluster_subgroup0_name'] == option:
            nodes.append(
                Node(id=skill[0], color=skill[1]['cluster_color'], size=50))

    G_clustered_skills_subgraph = G_clustered_skills_color.subgraph(
        [node.to_dict()['id'] for node in nodes])
    for skill_pair in G_clustered_skills_subgraph.edges(data=True):
        edges.append(Edge(source=skill_pair[0], target=skill_pair[1],
                     color='silver', weight=skill_pair[2]['weight']))

    config = Config(width=800, height=500, directed=False,
                    nodeHighlightBehavior=True, highlightColor="#F7A7A6", collapsible=True)

    length_of_nodes = len(list(set([node.to_dict()['id'] for node in nodes])))
    st.markdown('<p style="font-family:Courier New; color:Black; font-size: 20px;"><b>Number of Skills in Cluster:</b>' +
                str(length_of_nodes), unsafe_allow_html=True)

    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)

    st.markdown('<p style="font-family:Courier New; color:Black; font-size: 20px;"><b><i>Cluster Subgroups:</i></b></p>',
                unsafe_allow_html=True)
    subgroups1 = dict()
    for skill in G_clustered_skills_color.nodes(data=True):
        if skill[1]['cluster_subgroup0_name'] == option:
            subgroups1[skill[1]['cluster_subgroup2_name']
                       ] = skill[1]['cluster_color']

    if len(subgroups1) > 1:
        for subgroup1_name, subgroup1_color in subgroups1.items():
            st.markdown(
                f'<p style="font-family:Courier New;color:{subgroup1_color}";><b>{subgroup1_name}</b></p>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<p style="font-family:Courier New;color:{list(subgroups1.values())[0]}";><b>{list(subgroups1.keys())[0]}</b></p>', unsafe_allow_html=True)
