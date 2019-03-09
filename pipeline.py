import argparse
import os

import pandas as pd

from parse_igram import get_igram_photos
from beauty_predict import beauty_predict

parser = argparse.ArgumentParser()
parser.add_argument('model_path', default="model-ldl-resnet.h5")
parser.add_argument('contestants_csv', default="contestants.csv")

args = parser.parse_args()

# argparse -> read csv -> load instagram -> run through neural net -> write to file

# name | instagram
contestants = pd.read_csv(args.contestants_csv)

if __name__ == "__main__":
    pass