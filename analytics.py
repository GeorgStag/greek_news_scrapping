###########################################################################
###########################################################################
###########################################################################
### libraries


import plotly.express as px

import pandas as pd



###########################################################################
###########################################################################
###########################################################################
### data cleaning


### google data cleaning
google_text = pd.read_csv('data/google_scrapies.csv')
google_text['Date'] = pd.to_datetime(google_text['Date'])
for i in range(google_text.shape[0]):
    try:
        if 'ps://' in google_text.iloc[i,2]:
            google_text.iloc[i,2] = google_text.iloc[i,2].replace('ps://','')
            temp = google_text.iloc[i,2]
            google_text.iloc[i,2] = temp[:temp.find('/')]
        if '/' in google_text.iloc[i,2]:
            temp = google_text.iloc[i,2]
            google_text.iloc[i,2] = temp[:temp.find('/')]
    except:
        if str(google_text.iloc[i,2]) == 'nan':
            temp = google_text.iloc[i, 5]
            temp = temp.replace('https://','')
            temp = temp.replace('http://', '')
            temp = temp.replace('www.', '')
            no = temp.find('/')
            google_text.iloc[i,2] = temp[:no]
    if 'ps:' in google_text.iloc[i, 2]:
        google_text.iloc[i, 2] = google_text.iloc[i, 2].replace('ps://', '')
        temp = google_text.iloc[i, 2]
        google_text.iloc[i, 2] = temp[:temp.find('/')]
    if '/' in google_text.iloc[i, 2]:
        temp = google_text.iloc[i, 2]
        google_text.iloc[i, 2] = temp[:temp.find('/')]




###########################################################################
###########################################################################
###########################################################################
### plots for Providers and and Type


### matplotlib pies
google_text[['Provider','Type']].apply(pd.value_counts).plot.pie(subplots=True)


### plotlib pies
fig = px.pie(google_text, values=google_text['Provider'].value_counts().values/sum(google_text['Type'].value_counts().values), names=google_text['Provider'].value_counts().index , hole=.3)
fig.update_traces(hoverinfo='percent+value', textinfo='none')
fig.update_layout( title_text='Google news from:', )
fig.show()

### plotlib bar
fig = px.bar(google_text, y=google_text['Provider'].value_counts().values/sum(google_text['Type'].value_counts().values), x=google_text['Provider'].value_counts().index)
#fig.update_traces(hoverinfo='percent+value', textinfo='none')
fig.update_layout( title_text='Google news from:', )
fig.show()

### plotlib pies
fig = px.pie(google_text, values=google_text['Type'].value_counts().values/sum(google_text['Type'].value_counts().values), names=google_text['Type'].value_counts().index)
fig.update_traces(hoverinfo='percent+value', textinfo='none')
fig.update_layout( title_text='Google news from:', )
fig.show()

### plotlib bar
fig = px.bar(google_text, y=google_text['Type'].value_counts().values/sum(google_text['Type'].value_counts().values), x=google_text['Type'].value_counts().index)
#fig.update_traces(hoverinfo='percent+value', textinfo='none')
fig.update_layout( title_text='Google news from:', )
fig.show()






###########################################################################
###########################################################################
###########################################################################
### pie chart for top news


no = 10
temp = google_text['Title'].value_counts().head(no)
top_news = pd.DataFrame({'News':[0]*no,'Percentage':[0]*no})
for i in range(no):
    ind = -1
    for j in (google_text['Title'] == temp.index[i]):
        ind = ind + 1
        if j == True: break
    top_news.iloc[i,0] =  google_text['Provider'][ind] + ' : ' + google_text['Title'][ind] #+ ' \n' + google_text['Url'][ind]
    top_news.iloc[i,1] = temp.values[i]/sum(temp.values)


### plotlib pies
fig = px.pie(top_news, values='Percentage', names='News')
fig.update_traces(hoverinfo='percent+value', textinfo='none')
fig.update_layout( title_text='Top Google news:', )
fig.show()





###########################################################################
###########################################################################
###########################################################################
### protothema



proto_thema = pd.read_csv('data/proto_thema_scrapies.csv')
proto_thema['Date'] = pd.to_datetime(proto_thema['Date'])

nd = ['ΝΔ', 'νδ΄', 'Νέα Δημοκρατία', 'νέα δημοκρατία', 'Μητσοτάκη', 'Δένδια', 'δεξιά', 'Δεξιά', 'Άδωνι', 'Αδώνι' ,'Σαμαρά', 'ΟΝΝΕΔ', 'Οννεδ', 'Οννέδ', 'οννεδ', 'οννέδ']
sy = ['Σύριζα', 'σύριζα΄', 'Syriza', 'syriza', 'Πολάκη', 'Τσίπρα', 'αριστερά', 'Αριστερά']

nd_news = []
sy_news = []
for i in proto_thema['0']:
    for j in i.split(' '):
        if j in nd: nd_news.append(i)
        if j in sy: sy_news.append(i)


chart = pd.DataFrame([ ['nd', len(nd_news)], ['syr', len(sy_news)] ])

fig = px.pie(chart, values=1, names=0, hole=0.3)
fig.update_traces(hoverinfo='percent+value', textinfo='none')
fig.update_layout( title_text='Political Part news:', )
fig.show()


chart = pd.DataFrame(nd_news).value_counts()


