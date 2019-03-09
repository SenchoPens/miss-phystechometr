import os.path
import pathlib

parent_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
output_path = parent_path / 'predict_output'
