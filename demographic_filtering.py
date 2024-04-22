import pandas as pd
import numpy as np

df = pd.read_csv('articles.csv', encoding='utf-8')


q_articles = df.append()

q_articles = q_articles.sort_values('eventType', ascending=False)

output = q_articles.head(20).values.tolist()

