import re
import os
import urllib.request
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
import random
# import some geomodule

# создает файл для записи результатов,
# если его не было до этого
def create_output_file(output_file, fields):
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
                    csvfile, delimiter=';',
                    fieldnames=fields)
        writer.writeheader()


# записывает строку данных в файл
def write_data_down(output_file, fields, name, link, place,
                    start_day, start_month, start_year,
                    end_day, end_month, end_year):
    with open(output_file, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, delimiter=';',
            fieldnames=fields)
        writer.writerow({'name': name, 'city': place,
                        'start_day': start_day , 'start_month': start_month, 'start_year': start_year,
                        'end_day': end_day, 'end_month': end_month, 'end_year': end_year,
                        'link': link})

def decode_month(word):
    months = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'Jun': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11}
    month = months[word]
    return month


# из html вытаскивает значения
def extract_data_from_html(conf_raw):    
    name_raw = re.search('<a href="(.*?)">((.|\n)*?)<', conf_raw[0])
    name = name_raw.group(2)
    name = name.strip()
                
    link_raw = name_raw.group(1)
    link = 'https://linguistlist.org/'  + link_raw[3:]

    meta = re.search('\[(.*?)] \[(.*?) - (.*?)]<', conf_raw[0])
    place = meta.group(1)
    
    start_date_raw = meta.group(2)
    start_date_raw = start_date_raw.split('-')
    start_day = start_date_raw[0]
    start_month = decode_month(start_date_raw[1])
    start_year = start_date_raw[2]
    
    end_date_raw = meta.group(3)
    end_date_raw = end_date_raw.split('-')
    end_day = end_date_raw[0]
    end_month = decode_month(end_date_raw[1])
    end_year = end_date_raw[2]
                
    print('name: {}.'.format(name))
    print('place: {}. Start: {}, end: {}.'.format(
        place, start_date_raw, end_date_raw))
    print(link + '\n')
    return name,link,place,start_day,start_month,start_year,end_day,end_month,end_year


# тут все сразу
def main():
    link = 'https://linguistlist.org/callconf/browse-current.cfm?type=Conf'
    output_file = 'results.csv'
    fields = ['name', 'city',
              'start_day', 'start_month', 'start_year',
              'end_day', 'end_month', 'end_year',
              'link']

    #создает файл, если его нет
    create_output_file(output_file, fields)

    #открывает сайт
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        #connect to that page
        f = urlopen(req)
    except urllib.error.HTTPError:
        print('An Error occured')
    else:
        #read it all in
        myfile = f.read().decode('utf-8')
        #build a document model
        soup = BeautifulSoup(myfile,'html.parser')
    #парсит сайт
        all_conf_raw = re.findall('<td colspan="2">((.|\n)*?)<\/td>', str(soup))
        if len(all_conf_raw) > 1:
            for conf_raw in all_conf_raw[1:]: #именно с 1! можно ограничить кол-во
                name,link,place,start_day,start_month,start_year,end_day,end_month,end_year = extract_data_from_html(
                    conf_raw)
    #записывает строчку в файл
                write_data_down(output_file, fields, name, link, place,
                                start_day, start_month, start_year,
                                end_day, end_month, end_year)
        else:
            print('an error occured')
    print('All done.')
    

if __name__ == '__main__':
    main()
