import csv
import sys
from requests import get
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote

import os
os.system('cls')

url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105"

csv_file = "vysledky.csv"


# získání názvu všech obcí v okrese 
# def get_location(url):
#     response = get(url)
#     if response.status_code != 200:
#         print("Chyba: Nelze získat obsah stránky.")
#         return

#     soup = bs(response.text, 'html.parser')
#     td_elements = soup.find_all('td', class_='overflow_name')
#     for location in td_elements:
#         return location.text


def get_code_location(url): # získá kód volebního obvodu
        # Získání obsahu webové stránky
    response = get(url)
    if response.status_code != 200:
        print("Chyba: Nelze získat obsah stránky.")
        return

    # získání code:
    soup1 = bs(response.text, 'html.parser')
    td_elements1 = soup1.find_all('td', class_='cislo')

    # získání location
    soup2 = bs(response.text, 'html.parser')
    td_elements2 = soup2.find_all('td', class_='overflow_name')


    code_list =[]
    for a in td_elements1:
        a_tag = a.find('a')
        code = a_tag.text
        code_list.append(code)

    location_list =[]
    for location in td_elements2:
        location_text = location.text
        location_list.append(location_text)
    
    code_location = {}
    i = 0
    for i in range(len(code_list)):
        act_code = code_list[i]
        act_location = location_list[i]
        code_location.setdefault(i, {'location': act_location, 'code': act_code})
    print(code_location[46])

    
get_code_location(url)