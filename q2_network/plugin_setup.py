import importlib

from qiime2.plugin import (Str, Plugin, Choices, Float, Range, Bool)
from q2_types.feature_table import FeatureTable, Frequency

from ._type import Network, PairwiseFeatureData
from ._format import GraphModelingLanguageFormat, GraphModelingLanguageDirectoryFormat, PairwiseFeatureDataFormat, \
                     PairwiseFeatureDataDirectoryFormat
from ._correlate import calculate_correlations, build_correlation_network_r, build_correlation_network_p

import q2_network

plugin = Plugin(
    name='network',
    version=q2_network.__version__,
    website="https://github.com/shafferm/q2-network",
    package='q2_network',
    description=(
        'This QIIME 2 plugin supports methods for analysis of netwoks '
        'generated from correlations or other sources and provides '
        'rudimentary network statistics.'),
    short_description='Plugin for network analysis.',
)

plugin.register_semantic_types(Network)
plugin.register_semantic_types(PairwiseFeatureData)

plugin.register_formats(GraphModelingLanguageFormat)
plugin.register_formats(GraphModelingLanguageDirectoryFormat)
plugin.register_formats(PairwiseFeatureDataFormat)
plugin.register_formats(PairwiseFeatureDataDirectoryFormat)

plugin.register_semantic_type_to_format(Network, artifact_format=GraphModelingLanguageDirectoryFormat)
plugin.register_semantic_type_to_format(PairwiseFeatureData, artifact_format=PairwiseFeatureDataDirectoryFormat)


plugin.methods.register_function(
    function=calculate_correlations,
    inputs={'table': FeatureTable[Frequency]},  # TODO: Generalize, don't require frequency
    parameters={'corr_method': Str % Choices(["kendall", "pearson", "spearman"]),
                'p_adjustment_method': Str},
    outputs=[('correlation_table', PairwiseFeatureData)],
    input_descriptions={'table': (
        'Normalized and filtered feature table to use for microbial interdependence test.')},
    parameter_descriptions={
        'corr_method': 'The correlation test to be applied.',
        'p_adjustment_method': 'The method for p-value adjustment to be applied. '
                               'This can be selected from the list of methods in '
                               'statsmodels multipletests'},
    output_descriptions={'correlation_table': 'The resulting table of pairwise correlations with R and p-value.'},
    name='Build pairwise correlations between observations',
    description=(
        'Build pairwise correlations between all observations in feature table'),
)


plugin.methods.register_function(
    function=build_correlation_network_r,
    inputs={'correlation_table': PairwiseFeatureData},
    parameters={'min_val': Float % Range(0, 1, inclusive_end=True),
                'cooccur': Bool},
    outputs=[('correlation_network', Network)],
    input_descriptions={'correlation_table': (
        'Pairwise feature data table of correlations with r value.')},
    parameter_descriptions={
        'min_val': 'The minimum r value to say an edge should exist.',
        'cooccur': 'Whether or not to constrain the network to only positive edges.'
    },
    output_descriptions={'correlation_network': 'The resulting network.'},
    name='Build a correlation network based on an r value cutoff',
    description=(
        'Build a correlation network where nodes are features and edges '
        'are correlations are stronger than the provided min_val.'),
)


plugin.methods.register_function(
    function=build_correlation_network_p,
    inputs={'correlation_table': PairwiseFeatureData},
    parameters={'max_val': Float % Range(0, 1, inclusive_end=True),
                'max_param': Str},
    outputs=[('correlation_network', Network)],
    input_descriptions={'correlation_table': (
        'Pairwise feature data table of correlations with .')},
    parameter_descriptions={
        'max_val': 'The maximum p value to say an edge should exist.',
        'max_param': 'The name of the column to use (p or p_adjusted).'
    },
    output_descriptions={'correlation_network': 'The resulting network.'},
    name='Build a correlation network based on a p value cutoff',
    description=(
        'Build a correlation network where nodes are features and edges '
        'are correlations with a p-value (or adjusted p-value) less than '
        'the max_val.'),
)


importlib.import_module('q2_network._transformer')
