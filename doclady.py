from bs4 import BeautifulSoup
import re

student_irid = '342976388'
preses = []

file = open('all_doklady.xml', 'r', encoding='utf-8')
xml_file = file.read()
soup = BeautifulSoup(xml_file, features="xml")
for tag in soup.find_all("presentation"):
    for creator in tag.find_all('creator'):
        if creator.irid.text == student_irid:
            preses.append(tag.title.text)

for pres in preses:
    print(pres)
