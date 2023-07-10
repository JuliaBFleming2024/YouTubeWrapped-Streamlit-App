import streamlit as st
import requests
from PIL import Image
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests
from datetime import date, datetime
from dateutil.parser import parse
import uuid
from streamlit_lottie import st_lottie


st.set_page_config(page_title='YouViwer', page_icon=":cinema:", layout="centered")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def autolabel(ax, rects):
    """
    Attach a text label above each bar in the given axes with the height of the bar.
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')
                    
def format_date(video_date):
    video_date = video_date[:10]
    video_date = parse(video_date).date()
    date_str = video_date.strftime("%Y-%m-%d")
    return date_str
                    
def Top_10_Ever(data, startDate):
    today = date.today()
    total_viewing = 0
    endDate = today.strftime("%Y-%m-%d")
    channel_frequencies = pd.Series()
    video_frequencies = pd.Series()
    channel_names = []
    video_names = []
    viewing_dates = []
    for item in data:
        video_time_details = item.get('time')
        video_date = format_date(video_time_details)
        if (video_date >= startDate) and (video_date <= endDate):
            subtitles = item.get('subtitles')
            video_title = item.get('title')
            video_details = item.get('details')
            if subtitles:
                name_data = subtitles[0].get('name')
                channel_names.append(name_data)  # Add the channel name to the list
            if video_title and not video_details and video_title != 'Watched a video that has been removed':
                video_names.append(video_title)  # Add the video title to the list
                total_viewing = total_viewing + 1
    channel_frequencies = pd.Series(channel_names).value_counts()
    video_frequencies = pd.Series(video_names).value_counts()
    return channel_frequencies, video_frequencies

    
def format_title(video_title):
    formatted = video_title.split(' ', 1)[1]
    return formatted

lottie_youtube = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_bwk2zS.json")
lottie_upload = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_qdmak08f.json")
lottie_analytics = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_khwfxgwr.json")
lottie_typing = load_lottieurl("https://assets9.lottiefiles.com/datafiles/WIRy7Ny0KV28BJg/data.json")


##### Header Section #####
with st.container():
    st.header('Welcome to YouViewer! :wave:')
    st.subheader('Analytics for YouTube Consumers ')
    st.write('##')
    st.write('By Julia Fleming 🧸')

#### Get your Data ######
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Step 1:")
        st.subheader("Download Your Data")
    with right_column:
        st.write("####")
        st.write("####")
        st_lottie(lottie_youtube, height=75, key='youtube')
        
with st.container():
    st.write("####")
    st.write("NOTE: Download your Data as a JSON file!")
    tutorial = st.button("Not Sure How? Watch My Video!")
    if tutorial:
        video_file = open("tutorial.mov", 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
    ##st.write("[Watch this Video!](https://www.youtube.com/watch?v=zlzzO1e6dws)")

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
    # Generate a unique filename
    unique_filename = str(uuid.uuid4())
    # Save the uploaded file with the unique filename
    with open(unique_filename, "wb") as f:
        f.write(uploaded_file.read())
    st.write("File saved successfully!")

    # Open the saved file for processing
    with open(unique_filename, 'r') as watch_log:
        data = json.load(watch_log)
        
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Step 3:")
        st.subheader("View Your Analytics Report")
        st.write("####")
    with right_column:
        st.write("####")
        st_lottie(lottie_analytics, height=100, key='bargraphs')
        
with st.container():
    st.write("Select Time Range:")
    all_time = st.button("All Time")
    ytd = st.button("Year to Date")
    mtd = st.button("Month to Date")
    left_column, right_column = st.columns(2)
    start_of_youtube = date(2005,2,14)
    startDate = start_of_youtube.strftime("%Y-%m-%d")
    
    if all_time:
        start_of_youtube = date(2005,2,14)
        startDate = start_of_youtube.strftime("%Y-%m-%d")
    elif ytd:
        current_date = date.today()
        start_of_year = date(current_date.year, 1, 1)
        startDate = start_of_year.strftime("%Y-%m-%d")
    elif mtd:
        current_date = date.today()
        start_of_month = date(current_date.year, current_date.month, 1)
        startDate = start_of_month.strftime("%Y-%m-%d")


if uploaded_file is not None:
    with open(unique_filename, 'r') as watch_log:
        data = json.load(watch_log)
        Top_10_Channels, Top_10_Videos = Top_10_Ever(data, startDate)
    # Generate and display the bar plot for Top 5 Channels
        sns.set_theme()  # Set seaborn theme
        red_palette = sns.color_palette("Reds_r", n_colors=5)
        fig_channels, ax_channels = plt.subplots()
        channel_names = [Top_10_Channels.index[0], Top_10_Channels.index[1], Top_10_Channels.index[2], Top_10_Channels.index[3], Top_10_Channels.index[4]]
        counts = [Top_10_Channels.iloc[0], Top_10_Channels.iloc[1], Top_10_Channels.iloc[2], Top_10_Channels.iloc[3], Top_10_Channels.iloc[4]]
        bars_channels = ax_channels.bar(channel_names, counts, color=red_palette)
        ax_channels.set_ylabel('Videos Watched')
        ax_channels.set_title('Top 5 Channels')
        autolabel(ax_channels, bars_channels)
        ax_channels.set_xticklabels(channel_names, rotation=-45, ha='left')  # Angle x-axis labels from top left to bottom r
    fig_videos, ax_videos = plt.subplots()
    top_1_video = Top_10_Videos.index[0]
    top_2_video = Top_10_Videos.index[1]
    top_3_video = Top_10_Videos.index[2]
    formatted_1 = format_title(top_1_video)
    formatted_2 = format_title(top_2_video)
    formatted_3 = format_title(top_3_video)
    video_titles = [formatted_1, formatted_2, formatted_3]
    counts = [Top_10_Videos.iloc[0], Top_10_Videos.iloc[1], Top_10_Videos.iloc[2]]
    bars_videos = ax_videos.bar(video_titles, counts, color=red_palette[:3])
    ax_videos.set_ylabel('Amount of Watches')
    ax_videos.set_title('Most Rewatched Videos')
    autolabel(ax_videos, bars_videos)
    ax_videos.set_xticklabels(video_titles, rotation=-45, ha='left')


    with left_column:
    # Generate and display the bar plot for Top 3 Videos
        st.pyplot(fig_channels)
    with right_column:
        st.pyplot(fig_videos)



        
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Step 4:")
        st.subheader("Interactive Mode")

    with right_column:
        st.write("####")
        st_lottie(lottie_typing, height=125, key='keyboard')



channel_search = st.text_input('Input a YouTube Channel Name', key = 'Channel_Search')
Found_it = False
start_of_youtube = date(2005,2,14)
startDate = start_of_youtube.strftime("%Y-%m-%d")
if channel_search:
    if uploaded_file is not None:
            with open(unique_filename, 'r') as watch_log:
                data = json.load(watch_log)
                left_column, right_column = st.columns(2)
                Top_10_Channels, Top_10_Videos = Top_10_Ever(data,startDate)
                for i in range(len(Top_10_Channels)):
                    if channel_search == Top_10_Channels.index[i]:
                        st.write('\n\nYou watched a video by',channel_search,Top_10_Channels.iloc[i],'times\n\n')
                        Found_it = True
                        break
                if Found_it == False:
                    st.write('\n\nYou havent watched a video by',channel_search,'on this account \n\n')
    else:
        st.write('Oops! Make sure your file is uploaded!')
        

    
