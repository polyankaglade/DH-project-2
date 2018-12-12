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
    try:
        file = open(output_file)
    except IOError as e:
        with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(
                    csvfile, delimiter=';',
                    fieldnames=fields)
                writer.writeheader()


# записывает строку данных в файл
def write_data_down(output_file, fields, name, link, place,
                    start_date, end_date,
                    Latitude, Longtitude):
    with open(output_file, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, delimiter=';',
            fieldnames=fields)
        writer.writerow({'name': name, 'city': place,
                        'start_date': start_date, 'end_date': end_date,
                        'Latitude': Latitude, 'Longtitude': Longtitude,
                        'link': link})


# Алина, это твое
def turn_place_into_coord(place):
    # place -> coord 1,2
    coord1 = random.uniform(-90, 90) #рандомная широта
    coord2 = random.uniform(-180, 180) # рандомная долгота
    
    Latitude = coord1 + random.uniform(-0.09, 0.09)
    Longtitude = coord2 + random.uniform(-0.09, 0.09)
    return Latitude, Longtitude


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
    start_date = start_date_raw.split('-')
    start_date = '{} {}, {}'.format(start_date[1], start_date[0], start_date[2])
    
    end_date_raw = meta.group(3)
    end_date = end_date_raw.split('-')
    end_date = '{} {}, {}'.format(end_date[1], end_date[0], end_date[2])
                
    print('name: {}.'.format(name))
    print('place: {}. Start: {}, end: {}.'.format(
        place, start_date, end_date))
    print(link + '\n')
    return name, link, place, start_date, end_date


# тут все сразу
def main():
    link = 'https://linguistlist.org/callconf/browse-current.cfm?type=Conf'
    output_file = 'results.csv'
    fields = ['name', 'city', 'start_date', 'end_date',
              'Latitude', 'Longtitude', 'link']

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
        myfile = f.read()
        #build a document model
        soup = BeautifulSoup(myfile,'html.parser')
    #парсит сайт
        all_conf_raw = re.findall('<td colspan="2">((.|\n)*?)<\/td>', str(soup))
        if len(all_conf_raw) > 1:
            for conf_raw in all_conf_raw[1:]: #именно с 1! можно ограничить кол-во
                name, link, place, start_date, end_date = extract_data_from_html(
                    conf_raw)
                
                Latitude, Longtitude = turn_place_into_coord(place)
    #записывает строчку в файл
                write_data_down(output_file, fields, name, link, place,
                                start_date, end_date,
                                Latitude, Longtitude)
        else:
            print('an error occured')
    print('All done.')
    

if __name__ == '__main__':
    main()
