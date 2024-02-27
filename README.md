# Projekt 3: Analýza volebních dat
Tento projekt je součástí Engeto Online Python Akademie a slouží k analýze volebních dat. Pomocí tohoto skriptu lze získat volební data z webových stránek a uložit je do CSV souboru.

## Autor
Jméno: Jiří Kotrle  
Email: jirikotrle@gmail.com  
Discord: jirikotrle

## Popis  
Tento skript stahuje volební data z webových stránek Českého statistického úřadu a ukládá je do CSV souboru. Data obsahují informace o registraci voličů, počtu odevzdaných hlasů a počtu platných hlasů, stejně jako počet hlasů, které získaly jednotlivé politické strany.


## Použití
Skript je spouštěn z příkazové řádky s třemi argumenty, např:  
python projekt_3.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7105' 'okres_Sumperk.csv'

Kde jednotlivé argumenty jsou:  
Název souboru.  
URL adresa stránky s volebními výsledky pro daný okres.  
Název výstupního CSV souboru, do kterého budou data uložena.

## Příklad spuštění:
Níže je screen výstupního souboru.  
![image](https://github.com/JiriKotrle/Projekt_3/assets/152901006/e0b7272a-3f7c-4e9e-927f-59dce746a39f)


## Závislosti
Pro správné fungování tohoto skriptu je třeba mít nainstalované knihovny uvedené v souboru requirements.txt.  
Tyto knihovny můžete nainstalovat pomocí následujícího příkazu:  
pip install -r requirements.txt
