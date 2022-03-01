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
            tags_frequency[t] = int(row['score'])
        else:
            tags_frequency[t] += int(row['score'])

# Delete unwanted tags
gender = ['F', 'M', 'TM', 'TF', 'NB', 'A']
gender_list = list()
gender_df = pd.DataFrame()
for speaker in gender:
    for listener in gender:
        gender_list.append('4'.join([speaker, listener]))

for g in gender_list:
    tags_frequency.pop(g, None)

tags_frequency.pop("Script Fill", None)
tags_frequency.pop("Script Offer", None)
tags_frequency.pop("deleted by user", None)

# Word Cloud
mask = np.array(Image.open("./img/gwa.png"))

cloud = WordCloud(width=2048, height=1080, max_font_size=500, max_words=5000, 
        background_color="black", colormap="RdPu", mask=mask).generate_from_frequencies(tags_frequency)
plt.figure(figsize=(60,30))
plt.imshow(cloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('word_cloud.png', facecolor='k', bbox_inches='tight')
