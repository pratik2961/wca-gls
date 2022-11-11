import re
import pandas as pd
def preprocess(data):
    temp = data.split("-")
    
    if("PM" in temp[0] or "AM" in temp[0]):
        return "",False
    else:
    
        pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        messages = re.split(pattern,data)[1:]
        dates = re.findall(pattern,data)
        df = pd.DataFrame({'user_message':messages,'message_date':dates})
        df.rename(columns = {'message_date':'date'},inplace=True)
        users = []
        messages = []
        for message in df['user_message']:
            entry =  re.split('([\w\W]+?):\s',message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group notification')
                messages.append(entry[0])
                
        df['users'] = users
        df['message'] = messages
        df.drop(columns=['user_message'],inplace=True)
            
        year = []
        month = []
        day = []
        hour = []
        minute = []
        month_num = []
        for date in df['date']:
            date1 = date.split(",")
            date2 = date1[0].split("/")
            year.append(date2[2])
            month_num.append(date2[0])
            if date2[0] == '1':
                month.append("Jan")
            elif date2[0] == '2':
                month.append("Feb")
            elif date2[0] == '3':
                month.append("March")
            elif date2[0] == '4':
                month.append("Apr")
            elif date2[0] == '5':
                month.append("May")
            elif date2[0] == '6':
                month.append("June")
            elif date2[0] == '7':
                month.append("July")
            elif date2[0] == '8':
                month.append("August")
            elif date2[0] == '9':
                month.append("Sep")
            elif date2[0] == '10':
                month.append("Oct")
            elif date2[0] == '11':
                month.append("Nov")
            elif date2[0] == '12':
                month.append("Dec")


            
            day.append(date2[1])
            date3 = date1[1].split(":")
            hour.append(date3[0])
            minute.append(date3[1][0:2])
            
        df['year'] = year
        df['month'] = month
        df['day'] = day
        df['hour'] = hour
        df['minute'] = minute
        df['month_num'] = month_num
        
        period = []
        for hour in df['hour']:
            if hour == 23:
                period.append(str(hour)+"-"+str('00'))
            elif hour == 0:
                period.append(str('00')+"-"+str(hour+1))
            else:
        #         print(type(hour))
                period.append(str(hour)+"-"+str(int(hour)+1))
        df['period'] = period

        return df,True