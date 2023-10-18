import json

import requests
from pprint import pprint
from bs4 import BeautifulSoup
from fake_headers import Headers
import re


#id_regex = re.compile(r"\d+")

headers_gen = Headers(os="win", browser="chrome")

res = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',headers=headers_gen.generate())

# pprint(res.text)
# print(res.status_code)

main_hh_html = res.text
soup = BeautifulSoup(main_hh_html , "lxml")
#print(soup.prettify())
s = []

vacances_list = soup.find_all("a", class_="serp-item__title")
vac_list2 = soup.find_all("div", attrs = {'data-qa': 'vacancy-serp__vacancy-address'})
#print(vac_list2)
for k in vac_list2:
    b=k.text
    s.append(b)
#print(s)
sp=[]
sp1=[]
for i,tag in enumerate(vacances_list):
    sp=[]
    name_tag = tag.text
    #print(name_tag)
    sp.append(name_tag)
    link = tag["href"]
    #print(link)
    sp.append(link)
    sp.append(s[i])
    res1_html = requests.get(link, headers=headers_gen.generate()).text
    vacancy_full_soup = BeautifulSoup(res1_html, "lxml")
    #print(vacancy_full_soup.prettify())
    info_tag = vacancy_full_soup.find_all("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
    #print(info_tag)
    #for el in info_tag:
    if len(info_tag) > 1:
        sal = info_tag[0].text
        comp = info_tag[1].text
        #print(sal)
        sp.append(sal)
        #print(comp)
        sp.append(comp)

    description = vacancy_full_soup.find('div', attrs={'data-qa': "vacancy-description"})
    #print(description.text)
    if "Django" in description.text or "Flask" in description.text:
        sp.append('True')
    else:
        sp.append('False')
    sp1.append(sp)
result=[]
sp_new=[]
#print(sp1)
result = [el for el in sp1 if "True" in el]
#print(result)
#print(len(result))
#print(len(sp1))
for vac in result:
    for el in vac:
        l = re.sub(r"\\xa0", r"\ ", el)
        el = l
        print(el)
print(result)
with open("vacances.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)




