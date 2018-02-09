"""
Shared methods across scripts
"""
import boto3
import yaml 

def read_config(path_to_config):
    """ Build configuration from YAML file """
    with open(path_to_config, 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config