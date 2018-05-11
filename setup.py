from setuptools import find_packages, setup


setup(
    name='q2-network',
    license='BSD-3-Clause',
    packages=find_packages(),
    author="Michael Shaffer",
    author_email="michael.shaffer@ucdenver.edu",
    description=(
        "QIIME2 plugin for building and analyzing networks."),
    url="https://github.com/shafferm/q2-network",
    entry_points={
        'qiime2.plugins':
        ['q2-network=q2_network.plugin_setup:plugin']
    }
)