# projekt_3.py: třetí projekt do Engeto Online Python Akademie
# author: Jiří Kotrle
# email: jirikotrle@gmail.com
# discord: jirikotrle

import os
import csv
import sys
import subprocess
from requests import get
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote

# Spustí příkaz pip freeze a uloží výstup do souboru requirements.txt
subprocess.run(['pip', 'freeze', '>', 'requirements.txt'], shell=True, check=True)

# Vyčistí terminál
os.system('cls')

# Funkce k získání odkazů k výsledkům každé z obcí v zadaném okrese
def get_links(url):
    response = get(url)
    if response.status_code != 200:
        print("Chyba: Nelze získat obsah stránky.")
        return

    soup = bs(response.text, 'html.parser')
    rows = soup.find_all('tr')
    
    links = []

    for row in rows:
        cell = row.find("a")
        
        if cell:
            relative_link = cell.get("href")
            decoded_relative_link = unquote(relative_link)
            adress = "https://volby.cz/pls/ps2017nss/"
            link = adress + decoded_relative_link
            links.append(link)
            
    return links


# Vytvoří množinu s údaji název obce a její kód
def get_code_location(url):
    response = get(url)
    if response.status_code != 200:
        print("Chyba: Nelze získat obsah stránky.")
        return

    soup1 = bs(response.text, 'html.parser')
    td_elements1 = soup1.find_all('td', class_='cislo')

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
        code_location.setdefault(i, {'code': act_code, 'location': act_location})
    
    return code_location


# Funkce získá volební data (strany, hlasy) pro každou obec ze zadaného okresu
# Funkce si zavolá funkci get_code_location získá z ní kód obce a název obce a vytvoří množinu all_data, kde je požadovaný řádek, který má být v .csv
def get_data(link):
    response = get(link)
    if response.status_code != 200:
        print("Chyba: Nelze získat obsah stránky.")
        return
    soup = bs(response.text, 'html.parser')

    parties_votes = {}
  
    # voliči v seznamu:
    registered = soup.find('td', class_ = 'cislo', headers = 'sa2').get_text()
    registered = int(registered.replace("\xa0", ""))
    parties_votes["registered"] = registered
    # odevzdané hlasy:
    envelopes = soup.find('td', class_ = 'cislo', headers = 'sa5').get_text()
    envelopes = int(envelopes.replace("\xa0", ""))
    parties_votes["envelopes"] = envelopes
    # platné hlasy:
    valid = soup.find('td', class_ = 'cislo', headers = 'sa6').get_text()
    valid = int(valid.replace("\xa0", ""))
    parties_votes["valid"] = valid
    
    # Hlasy odevzdané jednotlivým stranám
    rows = soup.find_all('tr')
    for row in rows:
 
        cells_1 = row.find_all('td', class_='overflow_name')
        for cell in cells_1:
            strana = cell.get_text(strip=True)
            hlasy = row.find_all('td', class_='cislo')[1].get_text(strip=True)
            hlasy = int(hlasy.replace("\xa0", ""))
            parties_votes[strana] = hlasy if hlasy else 0
   
    code_location = get_code_location(url)
    all_data = code_location[a] | (parties_votes)
    
    return all_data
    

# Fuknce vymaže všechna data v csv
def delete_all_data_in_csv(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        pass  # Pokud chcete napsat nějaká data, můžete sem napsat inicializační řádek.


# Funkce získá a vytvoří v.csv názvy jednotlivých sloupců 
def copy_header_to_csv(csv_file, link):
    data = get_data(link)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter=',')
        writer.writeheader()


# Funkce získá a zapíše volební data do řádku pod jednotlivé sloupce (pro každou obec)
def copy_data_to_csv(csv_file, link):
    data = get_data(link)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter=',')
        writer.writerow(data)
        


if __name__ == "__main__":
    # Kontrola zda jsou poskytnuty argumenty
    if len(sys.argv) != 3:
        print("Zadáno málo argumentů. Program nejde spustit. Ukončuji...")
        sys.exit

    # Získat argumenty
    url = sys.argv[1]
    csv_file = sys.argv[2]
    links = get_links(url)
    get_code_location(url)
    delete_all_data_in_csv(csv_file)

    a = 0
    for link in links:
        if a == 0:
            copy_header_to_csv(csv_file, link)
            copy_data_to_csv(csv_file, link)
        
        else:
            copy_data_to_csv(csv_file, link)
        a += 1




