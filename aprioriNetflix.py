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
    from custom_algorithms.apyori import apriori


    data = getData()
    data = addMovieId(data)
    data.dropna(axis=0, how='any', inplace=True)
    data.head(5)

    moviesByUser = data[['user', 'movieName']].groupby('user')['movieName'].apply(set)
    moviesByUserList = [list(x) for x in list(moviesByUser)]
    rules = apriori(moviesByUserList, min_support=0.0001, min_confidence=0.1, min_lift=2, min_length=2)

    # Visualising the results
    results = list(rules)


movie1List = list()
movie2List = list()
liftList = list()


for i in range(0, len(results)):
    try:
        m1, m2 = results[i][0]
        lift = results[i][2][0][3]
        movie1List.append(m1)
        movie2List.append(m2)
        liftList.append(lift)
    except:
        continue


pairResults = pd.DataFrame({'Movie1': movie1List, 'Movie2': movie2List, 'lift': liftList}).sort_values(by='lift', ascending=False)
pairResults.to_csv('aprioriNetflix.csv', index=False)



