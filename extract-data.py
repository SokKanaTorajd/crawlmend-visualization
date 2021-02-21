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

# reset index
df = df.reset_index(drop=True)

# ========= Trends year by year publication =========

# # counting trends
# year_trends = df['year_published'].value_counts().index.tolist()
# # print(year_trends)
# value_trends = df['year_published'].value_counts().tolist()
# # print(value_trends)
# print(df['year_published'].value_counts())

# trend_dict = {}
# for i in range(len(year_trends)):
#     trend_dict[year_trends[i]] = value_trends[i]

# # sorting from older year
# trend_items = trend_dict.items()
# trend_dict = sorted(trend_items)

# # convert to DataFrame
# td = pd.DataFrame(trend_dict, columns=['year', 'number_publications'])
# # extract to csv
# td.to_csv('./data-crawling/publication-year-by-year.csv')

# # plotting graphic of publications by year
# ax = plt.gca() #gca --> get current axis
# td.plot(kind='line',x='year', y='number_publications', ax=ax)
# plt.show()
# plt.savefig('./images/trends-by-year.png')

# ========= End =========



# ========= Top 10 Publishers =========

# counting publishers
publisher_list = df['publisher'].value_counts()[:10].sort_values(ascending=True).index.tolist()
publisher_value = df['publisher'].value_counts()[:10].sort_values(ascending=True).tolist()
print(df['publisher'].value_counts()[:10])

# create DataFrame
top10_dict = {}
for i in range(len(publisher_list)):
    top10_dict[publisher_list[i]] = publisher_value[i]
print(top10_dict)

d = [top10_dict]
top_df



# ========= End =========