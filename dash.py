import streamlit as st
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
db = client["inst_nike"]
info_prof = db["profile_nike"] 
posts = db["posts_nike"]  

def load_profile():
    profile_data = info_prof.find_one()
    print(profile_data)  
    return profile_data

def load_posts():
    post_data = list(posts.find()) 
    return pd.DataFrame(post_data)

profile_data = load_profile()
post_data = load_posts()

st.title("Dashboard")
st.sidebar.header("Instagram Profile")

if profile_data:
    st.sidebar.subheader(f"@{profile_data['username']}")
    st.sidebar.write(f"**Nome Completo:** {profile_data['full_name']}")
    st.sidebar.write(f"**Bio:** {profile_data['biography']}")
    st.sidebar.write(f"**Seguidores:** {profile_data['followers']}")
    st.sidebar.write(f"**Seguindo:** {profile_data['followees']}")
    st.sidebar.write(f"**Publicações:** {profile_data['media_count']}")

st.header("Publications")

if not post_data.empty:
    st.subheader("Publication notes")
    st.write(post_data[['date', 'caption', 'likes', 'comments']].head(10))
    
    st.subheader("Publication likes")
    likes_chart = post_data[['date', 'likes']].sort_values(by='date')
    st.line_chart(likes_chart.set_index('date'))

    st.subheader("Publication comments")
    comments_chart = post_data[['date', 'comments']].sort_values(by='date')
    st.line_chart(comments_chart.set_index('date'))    
else:
    st.write("Nenhuma publicação disponível para visualização.")
