import pandas as pd

# import data
df1 = pd.read_csv('./data-crawling/digital-supply-chain-details.csv')
df2 = pd.read_csv('./data-crawling/supply-chain-technology-details.csv')

# concat data frames
frames = pd.concat([df1, df2], ignore_index=True)

# remove column '_id'
frames = frames.drop(['_id'], axis=1)

# remove duplicated rows
frames = frames.drop_duplicates()

# reset index
frames = frames.reset_index(drop=True)

# export to csv
frames.to_csv('./data-crawling/raw-data.csv', index=False)