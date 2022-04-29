import pandas as pd

from reviews.models import Category, Genre, Title, genre_title

t_data=pd.read_csv('titles.csv',sep=',')

titles = [
    Title(
        name = t_data.ix[row]['name'], 
        year = t_data.ix[row]['year'],
        category = t_data.ix[row]['category'],
    )
    for row in t_data['id']
]
Title.objects.bulk_create(titles)

g_data=pd.read_csv('genre.csv',sep=',')

genres = [
    Genre(
        name = g_data.ix[row]['name'], 
        slug = g_data.ix[row]['slug'],
    )
    for row in g_data['id']
]
Genre.objects.bulk_create(genres)

c_data=pd.read_csv('catigory.csv',sep=',')

catigories = [
    Category(
        name = c_data.ix[row]['name'], 
        slug = c_data.ix[row]['slug'],
    )
    for row in c_data['id']
]
Category.objects.bulk_create(catigories)

gt_data=pd.read_csv('genre_title.csv',sep=',')

genre_titles = [
    genre_title(
        genre = gt_data.ix[row]['genre'], 
        title = gt_data.ix[row]['title'],
    )
    for row in c_data['id']
]
genre_title.objects.bulk_create(genre_titles)
