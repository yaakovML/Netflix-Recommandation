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
    Results.to_csv('MoviesIndex2.csv', sep='\t', index=False)
    #Results.to_csv('MoviesIndex.csv', sep='\t', index=False)

    # Results[Results['pValue']<0.05]

    #end = time.time()

    #print(end-start)

'''
Time: 21166.865052


path = "/Users/yaakov.tayeb/Documents/similar/Clients/MoviesIndex.csv"
movies = pd.read_csv(path, sep='\t', header=0)  # read from file
movies[(movies['Movie1']=='The Crown') & (movies['pValue']<0.2)]


ngood, nbad, nsamp = 100, 2, 10
s = np.random.hypergeometric(ngood, nbad, nsamp, 1000)
s = np.random.hypergeometric(15, 15, 15, 100000)

sum(s>=12)/100000.0 + sum(s<=3)/100000.0
plt.hist(s)

prop_dict = {}
for movie in tqdm(movies):
    tmp_users = set(movies_dict[movie])
    overlap_users = tmp_users.intersection(selected_users)
    [M, n, N] = [total_users, len(selected_users), len(tmp_users)]
    rv = hypergeom(M, n, N)
    tmp_prop = rv.cdf(len(overlap_users))
    try:
        prop_dict[tuple([titles_id_dict[int(movie)][0], 'http://www.netflix.com/watch/' + str(int(movie))])] = tmp_prop
    except:
        prop_dict[tuple(['Not Availble','http://www.netflix.com/watch/' + str(int(movie))])] = tmp_prop





# M - the entire pool
# N - the amount of what we take from the pool
# n - the desired group

[M, n, N] = [len(data), moviesHist['Forensic Files'], moviesHist['The Fosters']]
rv = hypergeom(M, n, N)
x = np.arange(0, n+1)
pmf_dogs = rv.pmf(x)

plt.figure()
plt.suptitle('hypergeom Moview', fontsize=10, color='#acc2d9')
plt.plot(x, pmf_dogs, color='#FADB6F')
plt.vlines(x, 0, pmf_dogs, lw=2)
plt.xlabel('# of dogs in our group of chosen animals')
plt.ylabel('hypergeom PMF')
plt.show()

rv.mean() (M, n, N, loc=0, moments='mv')

'''

