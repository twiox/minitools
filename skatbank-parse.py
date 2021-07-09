import pandas as pd
import sys
import glob
import codecs
from datetime import datetime 
import os
from pathlib import Path

"""Quick and dirty Skatbank-Account-data splitter --> just splits the Account-data into different csv-files
So I want to split it by Textschlüssel to filter regular and irregular payments"""

filenames = {'05 Basislastschrift':'S_Abbuchungen', 
             '08 Dauerauftrag':'S_Daueraufträge', 
             '52 Dauerauftrag':'H_SEPA_und_DA', 
             '16 SEPA Überweisung':'S_Überweisungen', 
             '51 Überweisungsgutschr.':'H_Überweisungen', 
             '31 Abschluss':'S_Abschluss_Skatbank', 
             '09 Retouren':'S_Retouren'}

def create_files(year, month, subset):
    p = Path(f"out/{year}/{month}")
    p.mkdir(parents=True, exist_ok=True)
    
    for key in set(subset["Textschlüssel"]):
        subsubset = subset[subset["Textschlüssel"] == key]
        subsubset.sort_values("Primanota")
        try:
            out = p/f'{filenames[key]}.csv'
            subsubset.to_csv(out,sep=";")
        except:
            pass       

def main():
    data=pd.read_csv(sys.argv[1], delimiter = ";", encoding="unicode_escape")
    data = data.replace('\n','', regex=True) 
    data = data.replace(',','.', regex=True) 
    data.columns = data.iloc[14] 
    data = data[15:]
    print(data)
    data.drop(['Valuta', 'ZahlungsempfängerKto','ZahlungsempfängerIBAN','ZahlungsempfängerBLZ','ZahlungsempfängerBIC','Währung'], axis=1, inplace=True)
    for row in data.iterrows():
        try:
            data.at[row[0],"Month"] = datetime.strftime(datetime.strptime(row[1]["Buchungstag"],"%d.%m.%Y"),"%m")
            data.at[row[0],"Year"] = datetime.strftime(datetime.strptime(row[1]["Buchungstag"],"%d.%m.%Y"),"%Y")
        except:
            pass
    for year in set(data["Year"]):
        for month in set(data["Month"]):
            subset = data[(data["Month"] == month)&(data["Year"]==year)]
            if len(subset) > 0:
                create_files(year, month, subset)

if(__name__ == "__main__"):
    main()