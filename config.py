import os.path
import pathlib

parent_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
output_path = parent_path / 'predict_output'

VK_API_VERSION = "5.92"
MIPT_UNIVERSITY_ID = 297
