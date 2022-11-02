import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    user_list = df['users'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list )

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_message,num_words,num_media_msg,link_count = helper.fetch_stats(selected_user,df)
        col1 , col2 , col3 , col4 = st.columns(4)
        
        with col1:
            
            st.header("Total Messages")
            st.title(num_message)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)

        with col4:
            st.header("Total Links")
            st.title(link_count)

        
        #finding most busiest user
        if selected_user == "Overall":
            st.title("Most Busy User")
            x,df1 = helper.fetch_most_busy_user(df)
            fig,ax = plt.subplots()
            name = x.index
            value = x.values

            
            col1 , col2 =  st.columns(2)

            with col1:
                ax.bar(name,value,color='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                new_df = df1.head()
                st.dataframe(new_df)


        st.title("Most Comman Word")
        #word cloud
    
        st.header("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)


        #most common word
        st.header("Word and Count - bar chart")
        col1 , col2 = st.columns(2)

        
        
        comman_df = helper.top_comman_word(selected_user,df)
        with col1:
            st.dataframe(comman_df)
        with col2:    
            fig,ax = plt.subplots()
            ax.bar(comman_df['words'],comman_df['count'],color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
    
        




        #month time 
        st.title("Timeline")
        timeline_df = helper.month_timeline(selected_user,df)
        st.header("Monthly TimeLine")

        fig,ax = plt.subplots()
        ax.plot(timeline_df['time'],timeline_df['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        

        #daily timeline
        st.header("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        
        ax.plot(daily_timeline['daily_timeline'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #most busy month
        
        st.title("Activity Map")
        st.header("Most Busy Month")
        col1,col2 = st.columns(2)
        month_count_df = helper.active_month(selected_user,df)
        with col1:
            st.dataframe(month_count_df)
        with col2:
            fig,ax = plt.subplots()
            ax.bar(month_count_df['index'],month_count_df['month'],color='black')
            st.pyplot(fig)

        st.header('Monthly heat map')
        heat_map = helper.activity_heatmap(selected_user,df)

        fig,ax = plt.subplots()
        ax = sns.heatmap(heat_map)
        st.pyplot(fig)


        #emoji 

        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user,df).head()

        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['count'],labels=emoji_df['emoji'],autopct='%0.2f')
            st.pyplot(fig)


        #positive and negative word count
        st.title("Word Count")
        positive_count = helper.positive_word_count(selected_user,df)
        negative_count = helper.negative_word_count(selected_user,df)
        col1 , col2  = st.columns(2)
        
        with col1:
            
            st.header("Positive Word Count")
            st.title(positive_count)

        with col2:
            st.header("Negative Word Count")
            st.title(negative_count)


        
        #positive and negative word dataframe
        
        positive_df = helper.positive_word_df(selected_user,df)
        negative_df = helper.negative_word_df(selected_user,df)
        col1 , col2  = st.columns(2)
        
        with col1:
            
            st.header("Positive Word With Count")
            st.dataframe(positive_df)

        with col2:
            st.header("Negative Word With Count")
            st.dataframe(negative_df)

        p_df,n_df = helper.comparison_positive_negative(user_list,df)

        
        col1 , col2 = st.columns(2)

        with col1:
            st.title("Positive word comparison")
            fig,ax = plt.subplots()
            ax.pie(p_df['count'],labels=p_df['name'],autopct='%0.2f')
            st.pyplot(fig)
        with col2:
            st.title("Negative word comparison")
            fig,ax = plt.subplots()
            ax.pie(n_df['count'],labels=n_df['name'],autopct='%0.2f')
            st.pyplot(fig)

        #negative positive comaprison for selected user
        if selected_user != "Overall":
            st.title("Positive and Negative Comparison for "+selected_user)
            df1 = helper.user_positive_negative(selected_user,df)
            fig,ax = plt.subplots()
            ax.pie(df1['count'],labels=df1['type'],autopct='%0.2f')
            st.pyplot(fig)


        #select positive word
        positive_df = helper.positive_word_df(selected_user,df)
        positive_word_list = list(positive_df['word'])

        st.header("Positive word and messages : ")
        for i in range(0,len(positive_word_list)):
            st.text("Word is : "+positive_word_list[i])
            new_df = helper.list_of_message(selected_user,df,positive_word_list[i])
            st.dataframe(new_df)


        #select negative word
        negative_df = helper.negative_word_df(selected_user,df)
        negative_word_list = list(negative_df['word'])

        st.header("Negative word and messages : ")
        for i in range(0,len(negative_word_list)):
            st.text("Word is : "+negative_word_list[i])
            new_df = helper.list_of_message(selected_user,df,negative_word_list[i])
            st.dataframe(new_df)