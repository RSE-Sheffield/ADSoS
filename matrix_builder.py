""" Produces the cartesian product of the supplied inputs """
import itertools
from typing import Dict, List

def build_matrix(inputs: Dict[str, List]) -> Dict:
    """ Produces the cartesian product of the supplied inputs """
    return _dictionary_product(inputs)

def _dictionary_product(inputs):
    return (list(dict(zip(inputs.keys(), x)) for x in itertools.product(*inputs.values())))
