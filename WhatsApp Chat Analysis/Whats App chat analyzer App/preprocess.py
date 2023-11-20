import pandas as pd
import re


# creating function to preprocess the data and convert into pandas dataframe
def preprocess_data(data):

    # pattren to extract6 dates from data
    pattren='\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM\s-\s)'

    # extract messages and dates from the data
    messages=re.split(pattren,data)[1:]
    dates=re.findall(pattren,data)

    # cleaning the dates data
    formate_dates=[]
    for val in dates:
        val=val.replace('-','')
        val=val.replace('\u202f', '')
        val=val.strip()
        formate_dates.append(val)
        
    # creating the data frame
    df = pd.DataFrame({'user_message': messages, 'message_date': formate_dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M%p")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # extracting username and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            user_name=entry[1]
            user_name=user_name.replace('-','')
            user_name=user_name.strip()
            users.append(user_name)
            
            msg=("".join(entry[2:]))
            msg=msg.strip()
            messages.append(msg)
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    # extracting coloumns from datetime column of df
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    # returning the df
    return(df)

