import streamlit as st
import requests
from PIL import Image
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import date, datetime
from dateutil.parser import parse
import uuid
from streamlit_lottie import st_lottie
import squarify
import textwrap

st.set_page_config(page_title='YouViwer', page_icon=":cinema:", layout="centered")

grey_colors = ['#e15454', '#FFA231', '#ffe599', '#9bc18a', '#92b0cc']

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_youtube = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_bwk2zS.json")
lottie_upload = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_qdmak08f.json")
lottie_analytics = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_khwfxgwr.json")
lottie_typing = load_lottieurl("https://assets9.lottiefiles.com/datafiles/WIRy7Ny0KV28BJg/data.json")
    
with st.container():
    st.image('Youtube-Wrapped Logo .PNG')
st.write('##')

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Step 1:")
        st.subheader("Access Your YouTube Data!")
    with right_column:
        st.write("####")
        st.write("####")
        st_lottie(lottie_youtube, height=75, key='youtube')
        
with st.container():
    st.write("####")
    st.write("NOTE: Download your Data as a JSON file!")
    tutorial = st.button("Not Sure How? Watch My Video!")
    if tutorial:
        st.video("Demo.mov")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Step 2:")
        st.subheader("Upload watch-history.json")
        st.write("####")
        st.write("####")
    with right_column:
        st_lottie(lottie_upload, height=150, key='upload')

uploaded_file = st.file_uploader("Upload files", accept_multiple_files=False)

if uploaded_file is not None:
    df = pd.read_json(uploaded_file)
    pd.set_option('display.max_colwidth', None)
    st.write("File saved successfully!")
    df['title'] = df['title'].str.replace('^Watched', '', regex=True)
    df = df[~df['title'].str.contains("a video that has been removed|From Google Ads")]
    df = df[df['details'].isnull() | (df['details'] == '')]
    df = pd.json_normalize(df.to_dict('records'), "subtitles", ["title", "time"])
    df["date"] = df["time"].str[:10]
    df = df.rename(columns={ "date": "date", "name": "channel_name", "title": "video_title" })
    df = df[['date', 'video_title', 'channel_name']]
    title_counts = df['video_title'].value_counts().reset_index()
    title_counts.columns = ['video_title', 'count']
    title_counts_top_5 = title_counts.head(5)
    channel_counts = df['channel_name'].value_counts().reset_index()
    channel_counts.columns = ['channel_name', 'channel_count']
    channel_counts_top_5 = channel_counts.head(5)

    videos = plt.figure(figsize=(10, 6))
    text_kwargs = {'fontsize': 10, 'fontweight': 'bold', 'color': 'black', 'alpha': 1}
    title_counts_top_5['video_title'] = title_counts_top_5.apply(lambda row: f"{row['video_title']}\n - \n {row['count']} Watches", axis=1)
    title_counts_top_5['video_title'] = title_counts_top_5['video_title'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=20)))
    squarify.plot(
        sizes=title_counts_top_5['count'],
        label=title_counts_top_5['video_title'],
        alpha=0.6,
        text_kwargs=text_kwargs,
        pad=0.2,
        color=grey_colors 
    )
    plt.axis('off')

    channels = plt.figure(figsize=(10, 6))
    text_kwargs = {'fontsize': 10, 'fontweight': 'bold', 'color': 'black', 'alpha': 1}
    channel_counts_top_5['channel_name'] = channel_counts_top_5.apply(lambda row: f"{row['channel_name']}\n - \n {row['channel_count']} Watches", axis=1)
    channel_counts_top_5['channel_name'] = channel_counts_top_5['channel_name'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=20)))
    squarify.plot(
        sizes=channel_counts_top_5['channel_count'],
        label=channel_counts_top_5['channel_name'],
        alpha=0.6,
        text_kwargs=text_kwargs,
        pad=0.2,
        color=grey_colors
    )
    plt.axis('off')

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Step 3:")
        st.subheader("Top Viewed Dashboard")
        st.write("####")
    with right_column:
        st.write("####")
        st_lottie(lottie_analytics, height=100, key='bargraphs')

top_range = 'all'
left_column, middle_column, right_column = st.columns(3)
if uploaded_file is not None:
    with left_column:
        if st.button("All Time", key = 'top_all'):
            top_range = 'all'
    with middle_column:
        if st.button("Year to Date", key = 'top_year'):
            top_range = 'year'
    with right_column:
        if st.button("Month to Date", key = 'top_mtd'):
            top_range = 'month'

if uploaded_file is not None:
    if (top_range == 'all'):
            st.subheader('Top 5 most Rewatched Channels of All Time')
            st.pyplot(channels)
            st.write('#####')
            st.subheader('Top 5 most Rewatched Videos of All Time')
            st.pyplot(videos)
    elif (top_range == 'year') :
            st.subheader('Top 5 most Rewatched Channels This Year')
            st.pyplot(channels_ytd)
            st.write('#####')
            st.subheader('Top 5 most Rewatched Videos This Year')
            st.pyplot(videos_ytd)
    elif (top_range == 'month') :
            st.subheader('Top 5 most Rewatched Channels This Month')
            st.pyplot(channels_mtd)
            st.write('#####')
            st.subheader('Top 5 most Rewatched Videos This Month')
            st.pyplot(videos_mtd)



