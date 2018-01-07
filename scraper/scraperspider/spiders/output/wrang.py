# -*- coding: utf-8 -*-

import pandas as pd
import re

#pd.set_option('display.max_row', 10000)
#pd.set_option('display.max_columns', 1000)

def pipeline_price(df):
    df['processed_price'] = df['parsed_price'].apply(process_price)
    
def pipeline_duration(df):
    df['processed_duration'] = df['parsed_duration'].apply(process_duration)

def process_price(price):
    price = str(price)
    price = price.replace(r'\D+', '')
    # CASE: 2 245.00
    ma = re.search(r"(?P<d1>\d{1,3})\s?(?P<d2>\d{1,3}).(?P<d3>\d{2})\n", price)
    if ma: return float(ma.group("d1")+ma.group("d2")+ma.group("d3"))/100
    # CASE:  1 095, 895
    ma = re.search(r"(?P<d1>\d{1,3})\s?(?P<d2>\d{1,3})\n", price)
    if ma: return float(ma.group("d1")+ma.group("d2"))
    # CASE: 10 %, 20 %
    ma = re.search(r"(\d{1,2})\xa0%", price)
    if ma: return 0
    #is nan 
    if price=="nan": return 0
    raise Exception

def process_duration(duration):
    DAY_TO_HOUR=7
    duration = str(duration)
    duration = duration.lower()
    #duration=duration.replace("\n","")
    #duration=re.sub(r"\\r\\n"," ", duration)
    # CASE: 2 jours - 14 h
    ma = re.search(r"\d+ jours? - (?P<hours>\d+) h", duration)
    if ma: return float(ma.group("hours"))
    # CASE: 1 heure, 7 heures
    ma = re.search(r"(?P<hours>\d+) heures?", duration)
    if ma: return float(ma.group("hours"))
    # CASE: 3 jours
    ma = re.search(r"(?P<days>\d+) jours?", duration)
    if ma: return float(ma.group("days")) * DAY_TO_HOUR
    # CASE: 2j, 2 j
    ma = re.search(r"(?P<days>\d+)\s?j", duration)
    if ma: return float(ma.group("days")) * DAY_TO_HOUR
    # CASE: 2 jours + 1 jour, 2 + 2, 2j + 2j
    ma = re.search(r"(?P<days>\d+)\s?(jours?|j)?\s?\+\s?\d+\s?(jours?|j)?", duration)
    if ma: return float(ma.group("days")) * DAY_TO_HOUR
    # CASE: 2h30
    ma = re.search(r"(?P<hours>\d{1,3})h(?P<minutes>\d{2})", duration)
    if ma: return float(ma.group("hours")) + float(ma.group("minutes")) / 60
    # CASE: 0.5 jours
    ma = re.search(r"(?P<hours>\d{1,2}.\d{1,2}) jours", duration)
    if ma: return float(ma.group("hours")) * DAY_TO_HOUR
    # CASE: 1.5 jour
    ma = re.search(r"(?P<hours>\d{1,2}.\d{1,2}) jour", duration)
    if ma: return float(ma.group("hours"))
    # CASE: (2 + 1) jours
    ma = re.search(r"\((?P<hours>\d{1,2}) \+ (?P<extra>\d{1,2})\) jours", duration)
    if ma: return float(ma.group("hours")) + float(ma.group("extra"))
    # CASE: intra-établissement
    ma = re.search(r"cette formation est disponible en intra-établissement seulement", duration)
    if ma: return 0
    ma = re.search(r"(\d{1,2}) formations", duration)
    if ma: return 0
    ma = re.search(r"^\n", duration)
    if ma: return 0
    #is nan 
    if duration == "nan":
        return 0
    raise Exception

if __name__ == '__main__':
    inputfile = "parsed_comundi.csv"
    outputfile ="outputprocessed/processed_comundi.csv"
    df=pd.read_csv(inputfile, encoding = "utf-8")
    pipeline_price(df)
    pipeline_duration(df)
    #drop duplicates
    df=df.drop_duplicates(subset=['sku'])
    df.to_csv(outputfile, encoding='utf-8')
    
    






