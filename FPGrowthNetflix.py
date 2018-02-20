def getData(path = "/Users/yaakov.tayeb/Documents/ML/Association_Rule_Learning/netflix_movies_users.txt"):
    from math import isnan
    data = pd.read_csv(path, sep='\t', header=None)  # read from file
    data.columns = ['user', 'movieId', 'none']
    data = data[['user', 'movieId']]
    data.dropna(axis=0, how='any', inplace=True)
    data['movieId'] = map(lambda x: str(int(x)) if str(x).isdigit() else x, data['movieId'])
    return data

def addMovieId(data, path = "/Users/yaakov.tayeb/Documents/ML/Association_Rule_Learning/titles-id_dict.csv"):

    titles = pd.read_csv(path, sep=',', header=0)  # read from file
    titles['title'] = map(lambda x: x[0:x.find(" |")] if x.find(" |") > 0 else x, titles['title'])
    titles.set_index('movieid', drop=True, inplace=True)

    idNames = dict(zip(titles.index, titles['title']))
    data2 = data.loc[data["movieId"].str.match(r'[^a-zA-Z]+', na=False)].copy()

    data2['movieName'] = map(lambda x: idNames[int(x)] if int(x) in idNames else None, data2['movieId'])
    return data2


if __name__ == '__main__':

    import pandas as pd
    from custom_algorithms.fp_growth import find_frequent_itemsets


    data = getData()
    data = addMovieId(data)
    data.dropna(axis=0, how='any', inplace=True)
    data.head(5)

    moviesByUser = data[['user', 'movieName']].groupby('user')['movieName'].apply(set)
    moviesByUserList = [list(x) for x in list(moviesByUser)]

    movie1List = list()
    movie2List = list()
    supportList = list()

    for itemset in find_frequent_itemsets(moviesByUserList, 2, include_support=True):
        # only save pairs:
        groupN = len(itemset[0])
        if groupN == 2:
            movie1List.append(itemset[0][0])
            movie2List.append(itemset[0][1])
            supportList.append(itemset[1])

    # Save to CSV

    pairResults = pd.DataFrame({'Movie1': movie1List, 'Movie2': movie2List, 'Support': supportList}).sort_values(by='Support', ascending=False)
    pairResults.to_csv('FPGrowthNetflix.csv', index=False)
