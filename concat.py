from os import listdir, walk, getcwd
from os.path import isfile, join

import pandas as pd

mypath = join(getcwd(), "datasets/gonewildaudio")

# List of all files in the directory mypath
file_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    file_list.extend([join(dirpath, f) for f in filenames])

# Concatenation of the data
df = pd.DataFrame()
for file_name in file_list:
    dfi = pd.read_csv(file_name)
    df = pd.concat([df, dfi], ignore_index=True)

# Save dataset in CSV file
df.to_csv(join(getcwd(), "datasets", "gonewildaudio_dataset.csv"), index=False)
