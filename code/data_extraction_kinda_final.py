import re
import os
import urllib.request
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
import random
# import some geomodule

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

# создает файл для записи результатов,
# если его не было до этого
def create_output_file(output_file, fields):
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
                    csvfile, delimiter=';',
                    fieldnames=fields)
        writer.writeheader()


# записывает строку данных в файл
def write_data_down(output_file, fields, full_title,link,location,start_day,start_month,start_year,end_day,end_month,end_year,tags,site,cd_day,cd_month,cd_year):
    with open(output_file, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, delimiter=';',
            fieldnames=fields)
        writer.writerow({'full_title': full_title,'link': link,'location': location,
                         'start_day': start_day,'start_month': start_month,'start_year': start_year,
                         'end_day': end_day,'end_month': end_month,'end_year': end_year,
                         'tags': tags,'site': site,
                         'cd_day': cd_day,'cd_month': cd_month,'cd_year': cd_year})
        
#достает ссылку на страницу конференции со страницы со списком конференций        
def extract_main_info(conf_raw):    
    name_raw = re.search('<a href="(.*?)">((.|\n)*?)<', conf_raw[0])
    name = name_raw.group(2).strip()
    link_raw = name_raw.group(1)
    link = 'https://linguistlist.org/'  + link_raw[3:]
    print(link)
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
    
    return name, link, place, start_day, start_month, start_year, end_day, end_month, end_year

def extract_details(link):
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
        #print(soup)
        #full_title = re.search('Full Title: (.*?)<br/>', str(soup), re.DOTALL).group(1).strip()

        '''start_date, end_date = re.search('Date: (.*?)<br/>', str(soup)).group(1).strip().split(' - ')
        
        start_date= start_date.split('-')
        start_day = start_date[0]
        start_month = decode_month(start_date[1])
        start_year = start_date[2]
        
        end_date = end_date.split('-')
        end_day = end_date[0]
        end_month = decode_month(end_date[1])
        end_year = end_date[2]
        
        if re.search('Location: (.*?)<br/>', str(soup)):
            location = re.search('Location: (.*?)<br/>', str(soup)).group(1).strip()
        else:
            location = 'Unknown'''
        
        if re.search('Linguistic Field\(s\): (.*?)<br/>', str(soup)):
            tags = ', '.join(re.search('Linguistic Field\(s\): (.*?)<br/>', str(soup)).group(1).strip().split('; '))
        else:
            tags = 'None'
        
        if re.search('Web Site: <a href="(.*?)"', str(soup)):
            site = re.search('Web Site: <a href="(.*?)"', str(soup)).group(1)
        else:
            site = 'None'

        if re.search('Call Deadline: (.*?)<br/>', str(soup)):
            call_deadline = re.search('Call Deadline: (.*?)<br/>', str(soup)).group(1).strip().split('-')
            cd_day = call_deadline[0]
            cd_month = decode_month(call_deadline[1])
            cd_year = call_deadline[2]      
        else:
            cd_day, cd_month, cd_year = 'None', 'None', 'None'
    return tags,site,cd_day,cd_month,cd_year

# тут все сразу
def main():
    link = 'https://linguistlist.org/callconf/browse-current.cfm?type=Conf'
    output_file = 'results.csv'
    fields = ['full_title','link','location','start_day','start_month','start_year','end_day','end_month','end_year','tags','site','cd_day','cd_month','cd_year']

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
                conf_name, conf_link, place, sday, smonth, syear, eday, emonth, eyear = extract_main_info(conf_raw)
                tags,site,cd_day,cd_month,cd_year = extract_details(conf_link)
                
    #записывает строчку в файл
                write_data_down(
                    output_file,fields,conf_name,conf_link,place,sday,smonth,syear,eday,emonth,eyear,tags,site,cd_day,cd_month,cd_year) 
        else:
            print('an error occured')
    print('All done.')
    

if __name__ == '__main__':
    main()
