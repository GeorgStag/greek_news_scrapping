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
url = '''https://www.parapolitika.gr/'''
page = requests.get( url, headers=headers, cookies=cookies )
#page.status_code
#page.content
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

download_time = time.asctime( time.localtime(time.time()) )


page_text = soup.get_text()
page_text = page_text.split('\n')

filtered_text = []
for i in page_text:
    if i!='': filtered_text.append(i)

temp = filtered_text
filtered_text = []
for i in temp[30:]:
    if len(i)>20: filtered_text.append(i)
