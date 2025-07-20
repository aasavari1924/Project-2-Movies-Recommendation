import streamlit as st
import pickle

# Load pickled files
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Functions
def get_movie_index(name):
    movie_ds_index = -1
    for i in movies.index:
        if movies.loc[i, "title"].lower() == name.lower():
            movie_ds_index = i
            break
    return movie_ds_index

def get_movie_name(index):
    return movies.loc[index, "title"]

def get_recommendation(name):
    mindex = get_movie_index(name)
    if mindex == -1:
        return []
    r_movies = []    
    similarity_indexes = list(enumerate(similarity[mindex]))
    similarity_indexes = sorted(similarity_indexes, key=lambda x: x[1], reverse=True)

    for count in range(1, 6):
        r_movies.append(get_movie_name(similarity_indexes[count][0]))
    return r_movies

# Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation System")
st.write("Get similar movie recommendations using content-based filtering.")

movie_input = st.text_input("Enter Movie Name:")

if st.button("Recommend"):
    if movie_input.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        recommendations = get_recommendation(movie_input)
        if recommendations:
            st.success("Top 5 Recommended Movies:")
            for i, movie in enumerate(recommendations, 1):
                st.write(f"{i}. {movie}")
        else:
            st.error("Movie not found. Try another title.")