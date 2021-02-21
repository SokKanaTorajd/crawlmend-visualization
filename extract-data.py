import matplotlib.pyplot as plt
import pandas as pd
import re

def search_publisher(text):
    """get publisher's name from text"""
    publisher = []
    text = text.lower()
    items = text.split()
    for elem in items:
        if elem.isalpha():
            publisher.append(elem)
    
    return ' '.join(publisher)


def search_year(text):
    """get published year from text"""
    all_years = ['1990', '1991', '1992', '1993', '1994', '1995', 
                 '1996', '1997', '1998', '1999', '2000', '2001',
                 '2002', '2003', '2004', '2005', '2006', '2007',
                 '2008', '2009', '2010', '2011', '2012', '2013',
                 '2014', '2015', '2016', '2017', '2018', '2019',
                 '2020', '2021']
    for year in all_years:
        y = re.search(year, text)
        if y:
            return year


# import raw-data.csv
publisher = pd.read_csv('./data-crawling/raw-data.csv', usecols=['publihser'])

# extracting publisher and year
splitted_data = []
for p in publisher['publihser']:
    publish = search_publisher(p)
    year = search_year(p)
    splitted_data.append([publish, year])

# create new Data Frame based on splitted_data
df = pd.DataFrame(splitted_data, columns=['publisher', 'year_published'])

# drop NA row
df = df.dropna()

# remove empty string
df = df[df['publisher'].astype(bool)]

# reset index
df = df.reset_index(drop=True)
# print(df.info())


# ========= Trends year by year publication =========

# counting trends
year_trends = df['year_published'].value_counts().index.tolist()
value_trends = df['year_published'].value_counts().tolist()
print(df['year_published'].value_counts())

trend_dict = {}
for i in range(len(year_trends)):
    trend_dict[year_trends[i]] = value_trends[i]

# sorting from older year
trend_items = trend_dict.items()
trend_dict = sorted(trend_items)

# convert to DataFrame
td = pd.DataFrame(trend_dict, columns=['year', 'number_publications'])
# extract to csv
td.to_csv('./data-crawling/publication-year-by-year.csv', index=False)

# plotting graphic of publications by year
ax = plt.gca() #gca --> get current axis
td.plot(kind='line',x='year', y='number_publications', ax=ax)
plt.show()
plt.savefig('./images/trends-by-year.png')

# ========= End =========



# ========= Top 10 Publishers =========

# counting publishers
publisher_list = df['publisher'].value_counts()[:10].sort_values(ascending=True).index.tolist()
publisher_value = df['publisher'].value_counts()[:10].sort_values(ascending=True).tolist()

# create DataFrame
top10_dict = {}
for i in range(len(publisher_list)):
    top10_dict[publisher_list[i]] = publisher_value[i]

d = [top10_dict]
top_df = pd.DataFrame.from_dict(d)
top_df = pd.melt(top_df).rename(columns={
    'variable':'publisher',
    'value':'number_publications'
})

# # export to_csv
# top_df.to_csv('./data-crawling/top-ten-publishers.csv', index=False)

# plot top 10 publishers graphic
top_df.plot(kind='barh',x='publisher', y='number_publications')
plt.show()
plt.savefig('./images/top-ten-publishers.png')

# ========= End =========


# ========= Publications Per Year =========

all_top = []
for tp in publisher_list:
    data = df[df['publisher'] == tp]
    all_top.append(data)

for d in range(len(all_top)):
    all_top[d] = all_top[d].reset_index(drop=True)

display_data = {}
for i in range(len(all_top)):
    year = all_top[i]['year_published'].value_counts().sort_values(ascending=True).index.tolist()
    year_freq = all_top[i]['year_published'].value_counts().sort_values(ascending=True).tolist()
    publsh = all_top[i]['publisher'].value_counts().index.tolist()
    year_data = {}
    for i in range(len(year)):
        year_data[year[i]] = year_freq[i]
    display_data[publsh[0]] = year_data

dd_df = pd.DataFrame.from_dict(display_data)
dd_df = dd_df.sort_index()
# print(dd_df)

def SerToArr(series):
    return [series.index, series.to_numpy()]

for i in range(5, len(dd_df.columns)):
    series = pd.Series(dd_df[dd_df.columns[i]])
    plt.plot(*SerToArr(series.dropna()), linestyle='-', marker='o', label=dd_df.columns[i])

plt.legend()
plt.show()

# # export to csv
# dd_df.to_csv('./images/multiple-line.csv')

# ========= End =========