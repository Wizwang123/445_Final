from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

image = Image.open('rating.webp')
st.image(image,use_column_width = 'always')

'''
# Movie Rating Data Analysis

## Original Data
'''

unames = ['uid', 'age', 'gender', 'occupation', 'zip']
users = pd.read_table('u.user', sep='|', header=None, names=unames)

rnames = ['uid', 'mid', 'rating', 'timestamp']
ratings = pd.read_table('u.data', sep='\t', header=None, names=rnames)

mnames = ['mid', 'title', 'date1', 'data2', 'url',
          'unknown', 'Action', 'Adventure', 'Animation',
          'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
          'Fantansy', 'Film-Noir', 'Horror', 'Musical',
          'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_table('u.item', sep='|', header=None, names=mnames,encoding='ISO-8859-1')
frame = pd.merge(pd.merge(ratings,users),movies)
st.dataframe(frame)


'''
This dataset mainly contains 100000 ratings of 1000 users to about 1700 classic movies. Coulumn uid is the indicator of user. Column mid is the indicator of movies. Column rating is the rating scores. Column timestamp is the time the users gave the ratings. Columns age,gender, occupation, zip are all user related informations. Column title is the movie name. The columns left are all about movie genres.
'''

'''
## Dataset Information
### Name
Movie Rating Dataset
### Source
MovieLens 100K movie ratings. Stable benchmark dataset. 100,000 ratings from 1000 users on 1700 movies. MovieLens is run by GroupLens, a research lab at the University of Minnesota.
### Link
https://grouplens.org/datasets/movielens/ https://movielens.org
### Dataset License
Movielens is a Non-commercial movie dataset, which can be used for building a custom taste profile and recommendation, learning more about movies with rich data, images, and trailers.
### Size
The whole folder is about 16.2MB, the main files we I use is u.user(25KB, user information), u.data(2MB, ratings data) and u.item(238KB, movie information).

## Data alysis

The following data processing statistics are given to our five ratings for movies in the Comedy category. We can tell from this plot that, most people who rated comedy movies mostly about 4. And over 90% of them give a score equal or higher than three, which means that people loves comedy movies.
'''

comedy_ratings = frame[frame["Comedy"] == 1][["uid","title","rating"]]
user_rating_stat = comedy_ratings.groupby('rating').agg(num_of_user = ("rating","sum")).reset_index()
st.table(user_rating_stat)


user_rating_stat.set_index(["rating"], inplace=True)
num_list = user_rating_stat["num_of_user"]
st.bar_chart(num_list)



'''
We can select the genre we want to see the rating distribution of a specific kind.
'''

option = st.selectbox(
     'Select the movie genre:',
     ('Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantansy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'))

st.write('You selected:', option)

genre_ratings = frame[frame[option] == 1][["uid","title","rating"]]
genre_rating_stat = genre_ratings.groupby('rating').agg(num_of_user = ("rating","sum")).reset_index()
genre_rating_stat.set_index(["rating"], inplace=True)
genre_list = genre_rating_stat["num_of_user"]
st.bar_chart(genre_list)

'''
We can also select the top 5 movies with the highest ratings for men and women, and dig out the genres of movies that are more popular with audiences of both genders based on these movies.
'''

gender = option = st.selectbox(
     'Select the movie genre:',
     ('Female', 'Male'))
gender_ratings = frame[frame["gender"] == gender[0]][["title","rating"]]
gender_ratings["Movie Name"] = gender_ratings["title"]
gender_rating_stat = gender_ratings.groupby('Movie Name',as_index = False).agg(rating_sum = ("rating","sum"),rating_num = ("rating","count"))
gender_rating_stat["avg"] = gender_rating_stat["rating_sum"]/gender_rating_stat["rating_num"]
gender_rating_stat.sort_values(by=['avg'], ascending=False,inplace=True)
gender_top = gender_rating_stat.head(5)["Movie Name"].reset_index()
st.table(gender_top)
