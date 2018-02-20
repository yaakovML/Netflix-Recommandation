def getData(path = "netflix_movies_users.txt"):
    from math import isnan
    data = pd.read_csv(path, sep='\t', header=None)  # read from file
    data.columns = ['user', 'movieId', 'none']
    data = data[['user', 'movieId']]
    data.dropna(axis=0, how='any', inplace=True)
    data['movieId'] = map(lambda x: str(int(x)) if str(x).isdigit() else x, data['movieId'])
    return data

def addMovieId(data, path = "titles-id_dict.csv"):

    titles = pd.read_csv(path, sep=',', header=0)  # read from file
    titles['title'] = map(lambda x: x[0:x.find(" |")] if x.find(" |") > 0 else x, titles['title'])
    titles.set_index('movieid', drop=True, inplace=True)

    idNames = dict(zip(titles.index, titles['title']))
    data2 = data.loc[data["movieId"].str.match(r'[^a-zA-Z]+', na=False)].copy()

    data2['movieName'] = map(lambda x: idNames[int(x)] if int(x) in idNames else None, data2['movieId'])
    return data2

if __name__ == '__main__':

    import pandas as pd
    from matplotlib import pyplot as plt
    import numpy as np
    # import time

    # start = time.time()
    data = getData()
    data = addMovieId(data)
    data.dropna(axis=0, how='any', inplace=True)
    # data.head(5)

    moviesByUser = data[['user', 'movieName']].groupby('user')['movieName'].apply(set)
    usersByMovie = data[['movieName', 'user']].groupby('movieName')['user'].apply(set)

    from scipy.stats import hypergeom

    moviesHist = pd.value_counts(data['movieName'])

    allMovies = list(set(data['movieName']))
    allMovies = [x for x in allMovies if x is not None]

    moviesMetrix = pd.DataFrame(np.empty([len(allMovies), len(allMovies)]), columns=allMovies, index=allMovies)

    for i in range(0, len(moviesByUser)):
        tmpRecord = list(moviesByUser.iloc[i])
        for j in range(0, len(tmpRecord)):
            moviesMetrix.loc[tmpRecord[0]][tmpRecord[j]] += 1

    nMovies = len(allMovies)
    nUsers = len(moviesByUser)
    resultsMovie1 = list()
    resultsMovie2 = list()
    rvPvalue = list()

    for movieIdx1 in range(0, nMovies):
    #for movieIdx1 in range(0, 10):
        for movieIdx2 in range(movieIdx1+1, nMovies):
            # hypergeom(entire pool, n = red marbles, N = attempts)
            movie1 = allMovies[movieIdx1]
            movie2 = allMovies[movieIdx2]
            #[M, n, N] = [nUsers, moviesHist[movie1], moviesHist[movie2]]
            [M, n, N] = [nUsers, moviesMetrix[movie1][movie1], moviesMetrix[movie2][movie2]]
            rv = hypergeom(M, n, N)

            #pValue = rv.pmf(moviesMetrix.loc[movie1][movie2]) + rv.sf(moviesMetrix.loc[movie1][movie2])
            pValue = rv.cdf(moviesMetrix.loc[movie1][movie2])
            if moviesMetrix.loc[movie1][movie2]<2:
                pValue = 0
                continue
            resultsMovie1.append(movie1)
            resultsMovie2.append(movie2)
            rvPvalue.append(pValue)
        print(movieIdx1, nMovies)

    Results = pd.DataFrame({'Movie1': resultsMovie1, 'Movie2': resultsMovie2, 'pValue': rvPvalue})
    Results.to_csv('HyperGeometricResults.csv', sep='\t', index=False)
