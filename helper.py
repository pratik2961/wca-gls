from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import matplotlib

matplotlib.use('Agg')

extract = URLExtract()


f = open("positive-words.txt","r")
positive_word = f.read().split("\n")

f = open("negative-words.txt","r")
negative_word = f.read().split("\n")

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

def positive_word_count(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
        
    positive_word_count = 0

    for msg in df['message'][1:]:
        l = msg.split(" ")
        for word in l:
            if word != "":
                if word in positive_word:
                    positive_word_count = positive_word_count + 1
    return positive_word_count


def negative_word_count(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
        
    negative_word_count = 0

    for msg in df['message'][1:]:
        l = msg.split(" ")
        for word in l:
            if word != "":
                if word in negative_word:
                    negative_word_count = negative_word_count + 1
    return negative_word_count

def positive_word_df(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    positive_word_dict = {}
    for msg in df['message'][1:]:
        l = msg.split(" ")
        for word in l:
            if word in positive_word:
                if word != "":
                    if word not in positive_word_dict:
                        positive_word_dict[word] = 1
                    else:
                        positive_word_dict[word] = positive_word_dict[word] + 1
    positive_df = pd.DataFrame({"word":positive_word_dict.keys(),"count":positive_word_dict.values()})
    return positive_df


def negative_word_df(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    negative_word_dict = {}
    for msg in df['message'][1:]:
        l = msg.split(" ")
        for word in l:
            if word in negative_word:
                if word != "":
                    if word not in negative_word_dict:
                        negative_word_dict[word] = 1
                    else:
                        negative_word_dict[word] = negative_word_dict[word] + 1
    negative_df = pd.DataFrame({"word":negative_word_dict.keys(),"count":negative_word_dict.values()})
    return negative_df


def comparison_positive_negative(user_list,df):
    positive_count = []
    negative_count = []

    for name in user_list[1:]:
        pc  = positive_word_count(name,df)
        positive_count.append(pc)

    p_df = pd.DataFrame({"name":user_list[1:],"count":positive_count})
    
    for name in user_list[1:]:
        nc  = negative_word_count(name,df)
        negative_count.append(nc)

    n_df = pd.DataFrame({"name":user_list[1:],"count":negative_count})

    return p_df,n_df

def user_positive_negative(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['users'] ==  selected_user]
    pc  = positive_word_count(selected_user,df)
    nc  = negative_word_count(selected_user,df)

    df1 = pd.DataFrame()
    df1["type"] = ["Positive","Negative"]
    df1["count"] = [pc,nc]

    return df1


def list_of_message(selected_user,df,word):
    if selected_user == "Overall":
        new_df = pd.DataFrame()
        time_list = []
        user_list = []
        msg_list = []
        for i in range(0,df.shape[0]):
            
            msg_word_list = df["message"][i].split(" ")
            if word in msg_word_list: 
                msg_list.append(df["message"][i])
                time_list.append(df["date"][i])
                user_list.append(df["users"][i])
        new_df["Date And Time"] = time_list
        new_df["User"] = user_list
        new_df["Message"] = msg_list
        return new_df
        
    else:
        new_df = pd.DataFrame()
        time_list = []
        user_list = []
        msg_list = []
        for i in range(0,df.shape[0]):
            
            msg_word_list = df["message"][i].split(" ")
            if word in msg_word_list and (df["users"][i] == selected_user or df["users"][i] == "Overall") : 
                msg_list.append(df["message"][i])
                time_list.append(df["date"][i])
                user_list.append(df["users"][i])
        new_df["Date And Time"] = time_list
        new_df["User"] = user_list
        new_df["Message"] = msg_list
        return new_df
            
