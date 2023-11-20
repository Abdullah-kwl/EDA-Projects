import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud,STOPWORDS
from collections import Counter
from nltk.corpus import stopwords
import re
import emoji

def describe_stat(data,name):
    # df for user
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]
    # df for overall
    else:
        df=data
    
    # geting statistics

    # total messages
    total_messages=df.shape[0]

    # total words
    words_list=[]
    for row in df['message']:
        words_list.extend(row.split())
    total_words=len(words_list)
    
    # total media file shared
    total_mediafile=df[df['message']=='<Media omitted>'].shape[0]

    # total link share
    extractor=URLExtract()
    links=[]
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))
    total_links=len(links)


    return (total_messages,total_words,total_mediafile,total_links)


def busy_user(df):
    busy_user_graph_df=df[df['user']!='group_notification']['user'].value_counts().reset_index()
    busy_user_df=round(df[df['user']!='group_notification']['user'].value_counts()/df.shape[0],2).reset_index().rename(columns={'index':'Users','user':'Percentage'})

    return(busy_user_graph_df,busy_user_df)

# function for data clean for wordcount and word cloud
def cleanTxt(text):
    emoj = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642" 
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                            "]+", re.UNICODE)
    
    text = re.sub('…', '', text)
    text = re.sub('&amp;', '', text)
    text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('|', '', text) # Removing '|' sign
    text = re.sub('-', '', text) # Removing '-' sign
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
    text = re.sub(emoj, '', text)
    return text

def word_cloud(data,name):
    # df for user
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

    # df for overall
    else:
        df=data
    
    df_message=df[df['message'] != '<Media omitted>']['message']
    wc =WordCloud(stopwords=STOPWORDS ,width = 600, height=450, random_state = 21, max_font_size = 200,background_color='#05171f')
    df_wc=wc.generate(df_message.str.cat(sep=" "))
    return( df_wc)

def word_counter(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    # opening hindi stop words file
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    # some data cleaning    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    # counting words
    allwords = ' '.join([m for m in temp['message'].apply(cleanTxt)])
    lower_wordz=allwords.lower()
    wordz=[word for word in lower_wordz.split() if word not in stop_words]
    count=Counter(wordz)
    data=count.most_common(10)
    count_df=pd.DataFrame(data=data,columns=['words','Frequency'])

    return count_df


def emoji_counter(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Frequency'])

    return emoji_df[:10]

def monthly_timeline(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    timeline=df.groupby(['year','month_num','month'])['message'].count().reset_index()
    time=[]
    for month,year in zip(timeline['month'],timeline['year']):
        time.append(f'{month}-{year}')
    timeline['time']=time

    return timeline

def daily_timeline(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    timeline=df.groupby(['only_date'])['message'].count().reset_index()

    return timeline

def weekly_busy(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    timeline=df.groupby('day_name')['message'].count().reset_index()

    return timeline

def monthly_busy(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    timeline=df.groupby('month')['message'].count().reset_index()

    return timeline


def weeekly_heatmap(data,name):
    if name != 'Overall Analysis':
        df=data
        df=df[df['user']==name]  

        # df for overall
    else:
        df=data

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
