###############################################################################
###############################################################################
### libraries



from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import urllib.parse
import sys



greek_alphabet = 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
latin_alphabet = 'AaBbGgDdEeZzHhJjIiKkLlMmNnXxOoPpRrSssTtUuFfQqYyWw'
greek2latin = str.maketrans(greek_alphabet, latin_alphabet)



###############################################################################
###############################################################################
### html of page to string


headers = {"User-Agent": "Mozilla/5.0"}
cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
url = '''https://www.google.com/search?q=%CE%B5%CE%BB%CE%BB%CE%AC%CE%B4%CE%B1&tbm=nws'''
page = requests.get( url, headers=headers, cookies=cookies )
#page.status_code
#page.content
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

download_time = time.asctime( time.localtime(time.time()) )

html = list(soup.children)[1]
body = list(html.children)[1]
soup_str = str(body)



###############################################################################
###############################################################################
### possible news



news = []
ind = 0
key = '''class="BNeawe'''
step = len(key)
start = soup_str.find(key)


assert start!=-1, 'No news found!!! \nProbably problem with the scraper!!!'


finish = 0
while finish+1:
    finish = soup_str[(start+step):].find(key) + start + step
    news.append( soup_str[start:finish] )
    start = finish
    if finish > len(soup_str): finish = -1




###############################################################################
###############################################################################
### news filtering based on urls



news_urls = []
key_url = '''href="/url?q='''
key_end1 = '''&amp'''
key_end2 = '''"'''

for i in news:
    link_start = i.find(key_url)
    if link_start+1 :
        #print(news.index(i))
        link_start = link_start + 13
        link_end = i[link_start:].find(key_end1) + link_start
        re = i[ link_start:link_end ]
        news_urls.append( re )


#############################################
#############################################
#############################################
### output
#file = open('test.txt','w')
#for item in news_urls:
#	file.write(item+"\n")
#file.close()





###############################################################################
###############################################################################
### output table


master_table = []
types_finance = ['finance','economy','oikonomia','bloomberg','comission','currency']
types_politics = ['ertogan','erdogan','tourkia','turkia','apolut','apolitarxia','politic','politiki','ypourgo','ypourgiki','komma']
types_culture = ['cinema', 'sinema', 'movies', 'music', 'theatro', 'theater', 'premiera', 'culture','art ','koultoura','mousiki','theatro','music','theater','texni','texnes', 'cinema', 'movies']
types_tech = ['tech','texno', 'apple', 'kinit', 'aytokinit']
types_kairos = ['thermo','krio','hlio','ilio','zesti','kataigida','vroxi','xion','ygrasia']


for i in news_urls:
    temp = i.split('-')
    temp = temp[1:]
    title = ''
    for j in temp:
        title = title + j + ' '
    if title.find('%25') != -1 :
        title = urllib.parse.unquote(title.replace('25',''))
        title = unidecode(title)
        title = title.translate(greek2latin)
        title = str(title)
    title = title.replace('/','')
    title = title.replace('.html','')
    start_prov = i.find('www.') + 4
    finish_prov = i.find('gr') - 1
    prov = i[start_prov:finish_prov]
    start_title = i.find('gr/') + 2
    type = ''
    for j in types_finance:
        if j in i:
            type = type + 'finance '
            break
    for j in types_politics:
        if j in i:
            type = type + 'politics '
            break
    for j in types_culture:
        if j in i:
            type = type + 'culture '
            break
    for j in types_tech:
        if j in i:
            type = type + 'tech '
            break
    for j in types_kairos:
        if j in i:
            type = type + 'weather '
            break
    type = type[:-1]
    type = type.replace(' ','/')
    if type == '': type = 'Null'
    master_table.append( [ download_time, prov, title, type, i ] )


df = pd.DataFrame(master_table)
df.columns = ['Date', 'Provider', 'Title', 'Type', 'Url']