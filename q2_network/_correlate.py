import pandas as pd
from biom.table import Table
from scipy.stats import spearmanr, pearsonr, kendalltau
import networkx as nx
import numpy as np
from statsmodels.sandbox.stats.multicomp import multipletests


correl_methods = {'pearson': pearsonr, 'spearman': spearmanr, 'kendalltau': kendalltau}


def p_adjust(pvalues, method='fdr_bh'):
    res = multipletests(pvalues, method=method)
    return np.array(res[1], dtype=float)


def calculate_correlations(table: Table, corr_method: str='spearman',
                           p_adjustment_method: str='fdr_bh') -> pd.DataFrame:
    # TODO: multiprocess this
    corr_method_fun = correl_methods[corr_method]
    correls = pd.DataFrame(index=['r', 'p'])
    for (val_i, id_i, _), (val_j, id_j, _) in table.iter_pairwise(axis='observation'):
        r, p = corr_method_fun(val_i, val_j)
        correls[id_i, id_j] = r, p
    correls = correls.transpose()
    correls.index = pd.MultiIndex.from_tuples(correls.index)  # Turn tuple index into actual multiindex
    if p_adjustment_method is not None:
        correls['p_adjusted'] = p_adjust(correls.p, method=p_adjustment_method)
    correls = correls.sort_values('p')
    return correls


def build_correlation_network_r(correlation_table: pd.DataFrame, min_val: float=.75,
                                cooccur: bool=False) -> nx.Graph:
    net = nx.Graph()
    if cooccur:
        for (feature_i, feature_j), row in correlation_table.iterrows():
            if row['r'] > min_val:
                net.add_edge(feature_i, feature_j)
    else:
        for (feature_i, feature_j), row in correlation_table.iterrows():
            if row['r'] > np.abs(min_val):
                net.add_edge(feature_i, feature_j)
    return net


def build_correlation_network_p(correlation_table: pd.DataFrame, max_val: float=.05,
                                max_param: str= 'p_adjusted') -> nx.Graph:
    net = nx.Graph()
    for (feature_i, feature_j), row in correlation_table.iterrows():
        if row[max_param] < np.abs(max_val):
            net.add_edge(feature_i, feature_j)
    return net
