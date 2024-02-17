# import xml.etree.ElementTree as ET
#
# root_node = ET.parse('all_grant.xml').getroot()
#
# for tag in root_node.findall('projects/project/title'):
#     print(tag)
from bs4 import BeautifulSoup

file = open('all_grant.xml', 'r', encoding='utf-8')
xml_file = file.read()
soup = BeautifulSoup(xml_file, 'lxml')
for tag in soup.find_all("project"):
    print(tag)
    print(tag.title)
    print(tag.number)
