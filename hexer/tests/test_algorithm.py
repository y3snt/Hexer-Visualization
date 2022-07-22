import pytest
from os import listdir
from os.path import isfile, join, dirname

from hexer.algorithms.algorithm import algorithm, initialize
from hexer.data import Data

dir_path = dirname(__file__)
def get_path(dir_name, filename=''):
    return join(dir_path, dir_name, filename)

input_paths = sorted([get_path('input', f) for f in listdir(get_path('input')) if isfile(get_path('input', f))])
output_paths = sorted([get_path('output', f) for f in listdir(get_path('output')) if isfile(get_path('output', f))])

@pytest.mark.parametrize('input_path, output_path', zip(input_paths, output_paths)) 
def test_algorithm(input_path, output_path):
    data = Data()
    with open(input_path) as f:
        data.read_data(f)
    
    initialize(data)
    result = algorithm()

    with open(output_path) as f:
        expected = int(f.read()[:-1])

    assert result == expected

    
