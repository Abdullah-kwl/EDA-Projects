import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import pandas as pd
from preprocess import preprocess_data
from stat_data import describe_stat,busy_user,word_cloud,word_counter,emoji_counter,monthly_timeline,daily_timeline,weekly_busy,monthly_busy,weeekly_heatmap


# main screen title
st.title('WhatsApp Chat Analyzer')


# side bar content
st.sidebar.header('Whatsapp Chat Analysis')

# file uploder in side-bar
msg=st.sidebar.warning('Export chat Without media', icon="⚠️")
upload_file=st.sidebar.file_uploader('Upload text file')
if upload_file is not None:  
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocess_data(data)

    # show data on screen
    st.dataframe(df)
    # download buttoon to download clean data
    st.download_button('Download Clean data',df.to_csv(index=False),'Whatsapp_clean_df.csv')

    

    # fech all the users to show on dropdown
    users=df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0,'Overall Analysis')
    analysis_name=st.sidebar.selectbox('Show Analysis On',users)

    # show analysis button
    if st.sidebar.button('Show Analysis'):
        # divider
        st.markdown("---")
                
        # creat coloumns to show data
        st.header(analysis_name)
        col1,col2,col3,col4=st.columns(4)
        
        # geting statistics of data
        # send data to function for further analysis
        total_messages,total_words,total_mediafile,total_links=describe_stat(df, analysis_name)

        with col1:
            st.subheader('Total Messages')
            st.subheader(total_messages)
        with col2:
            st.subheader('Total Words')
            st.subheader(total_words)
        with col3:
            st.subheader('Total Links')
            st.subheader(total_links)
        with col4:
            st.subheader('Total Mediafiles')
            st.subheader(total_mediafile)

        
        # most busy person on group_leval     
        if analysis_name == 'Overall Analysis':
            # divider
            st.markdown("---")
            # send data into function to get graph_df object and busy_dataframe
            busy_user_graph_df,busy_user_df=busy_user(df)
            # creat columns to show graph and data
            st.header('Most Busy Users')
            col1,col2=st.columns(2)
            with col1:
                fig_busy_user=px.bar(data_frame=busy_user_graph_df,x='index',y='user',color='index')
                fig_busy_user.update_layout(width=80,height=300,xaxis_title='Name',yaxis_title='Count')                          
                st.plotly_chart(fig_busy_user,use_container_width=True)
                
                
            with col2:
                st.dataframe(busy_user_df)
        
        # creating wordCloud~
        st.markdown("---")
        st.header('Word-Cloud')
        df_wc=word_cloud(df,analysis_name)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)
       
        #Most common words graph
        st.markdown("---")
        st.header('Most Common words')
        count_df=word_counter(df,analysis_name)
        fig_common_words=px.bar(data_frame=count_df,x='words',y='Frequency',color='words')
        fig_common_words.update_layout(width=80,height=500)                          
        st.plotly_chart(fig_common_words,use_container_width=True)
              
        #Most common emoji
        st.markdown("---")
        st.header('Most Common Used Emojis')
        emoji_df=emoji_counter(df,analysis_name)
        fig_common_emoji=px.bar(data_frame=emoji_df,y='Emoji',x='Frequency',color='Emoji',orientation='h')
        fig_common_emoji.update_layout(width=80,height=500)                          
        st.plotly_chart(fig_common_emoji,use_container_width=True)


        #M monthly timeline
        st.markdown("---")
        st.header('Monthly Timeline')
        timeline_df=monthly_timeline(df,analysis_name)
        fig_timeline_df=px.line(data_frame=timeline_df,x='time',y='message')
        fig_timeline_df.update_layout(width=80,height=500,xaxis_title='Month')                          
        st.plotly_chart(fig_timeline_df,use_container_width=True)


        #M daily timeline
        st.markdown("---")
        st.header('Daily Timeline')
        timeline_df=daily_timeline(df,analysis_name)
        fig_timeline_df=px.bar(data_frame=timeline_df,x='only_date',y='message')
        fig_timeline_df.update_layout(width=80,height=500,xaxis_title='Days')                          
        st.plotly_chart(fig_timeline_df,use_container_width=True)

        #M Busy Day Of Week
        st.markdown("---")
        st.header('Most Busy Days')
        timeline_df=weekly_busy(df,analysis_name)
        fig_timeline_df=px.bar(data_frame=timeline_df,x='day_name',y='message',color='day_name')
        fig_timeline_df.update_layout(width=80,height=500,xaxis_title='Day Of Week')                          
        st.plotly_chart(fig_timeline_df,use_container_width=True)

        #M busy month
        st.markdown("---")
        st.header('Most Busy Months')
        timeline_df=monthly_busy(df,analysis_name)
        fig_timeline_df=px.bar(data_frame=timeline_df,x='month',y='message',color='month')
        fig_timeline_df.update_layout(width=80,height=500)                          
        st.plotly_chart(fig_timeline_df,use_container_width=True)

        #M busy month
        st.markdown("---")
        st.title("Weekly Activity HeatMap")
        user_heatmap = weeekly_heatmap(df,analysis_name)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
