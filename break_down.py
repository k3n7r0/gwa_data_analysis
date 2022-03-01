import pandas as pd
import numpy as np
import re
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# Read dataset
df = pd.read_csv("./datasets/gonewildaudio_dataset.csv")

# Obtain tags
df['tags'] = [re.findall(r'\[(.*?)\]', x) for x in df['title']]

# Tag frequency based on upvotes
tags_frequency = dict()
for index, row in df[['tags', 'score']].iterrows():
    for t in row['tags']:
        if t not in tags_frequency:
            tags_frequency[t] = dict()
            tags_frequency[t]['upvotes'] = int(row['score'])
            tags_frequency[t]['post_number'] = 1
        else:
            tags_frequency[t]['upvotes'] += int(row['score'])
            tags_frequency[t]['post_number'] += 1

sortedDict = sorted(tags_frequency.items(), key=lambda x: x[1]['upvotes'], reverse=True)

f = open("break_down.txt", "w")
for index, (tag, dictionary) in enumerate(sortedDict):
    f.write(str(index+1)+" ["+tag+"]\n")
    f.write("\t[Upvotes] "+str(dictionary["upvotes"])+"\n")
    f.write("\t[Number of Posts] "+str(dictionary["post_number"])+"\n")
f.close()
    
