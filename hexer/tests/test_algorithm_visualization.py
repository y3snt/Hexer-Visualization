import pytest
import io
from os import listdir
from os.path import isfile, join, dirname
from contextlib import redirect_stdout
from re import findall

from hexer.algorithms.algorithm_visualization import algorithm, initialize, reset_visualization_values
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
    with io.StringIO() as buffer:
        with redirect_stdout(buffer):
            algorithm()

        buffer_val = buffer.getvalue()
        result = findall('[0-9]+', buffer_val)[1] if  buffer_val else '-1'

    with open(output_path) as f:
        expected = f.read()[:-1]

    assert result == expected

    reset_visualization_values()






