from time import time
from turtle import width
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    
    num_messages = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split(" "))
    
    num_media_msg =  df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    


    return num_messages , len(words) , num_media_msg , len(links)

def fetch_most_busy_user(df):
    x = df['users'].value_counts() 
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x , df
    
        
def create_word_cloud(selected_user,df):
    f = open("stop_word.txt","r")
    stop_word = f.read()

    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    
    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    def remove_stop_word(msg):
        y = []
        for word in msg.lower().split():
            if word not in stop_word:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=300,height=300,min_font_size=10,background_color='black')
    temp['message'] = temp['message'].apply(remove_stop_word) 
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def top_comman_word(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    df = df[df['users'] != 'group notification']

    stop_word = open("stop_word.txt",'r')
    stop_word = stop_word.read()
    word_lst = []
    for messages in df['message']:
        message = messages.lower().split()
        for word in message:
            if word not in stop_word:
                word_lst.append(word)

    comman_df = pd.DataFrame(Counter(word_lst).most_common(10)).rename(columns={0:'words',1:'count'})
    return comman_df


def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    emojis = []
    for msg in df['message']:
        emojis.extend(c for c in msg if c in emoji.EMOJI_DATA)

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0:'emoji',1:'count'})

def month_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    timeline_lst = []
    for i in range(timeline.shape[0]):
    #     print(i)
        timeline_lst.append(timeline['month'][i] + " - " + str(timeline['year'][i]))
    timeline['time'] = timeline_lst
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    daily_timeline = []

    for date_only in df['date']:
        lst = date_only.split(",")
        daily_timeline.append(lst[0])
    df['daily_timeline'] = daily_timeline
    daily_timeline = df.groupby('daily_timeline').count()['message'].reset_index()
    return daily_timeline

def active_month(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    month_count_df = df['month'].value_counts().reset_index()
    return month_count_df

def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    
    heat_map = df.pivot_table(index='month',columns='period',values='message',aggfunc='count').fillna(0)
    return heat_map