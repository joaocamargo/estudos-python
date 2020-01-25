#! /usr/bin/env python3.6
import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter
from argcomplete.completers import EnvironCompleter
import requests
from bthread import BookingThread
from bs4 import BeautifulSoup
from file_writer import FileWriter

hotels = []


def get_countries():
    with open("europa2020.txt", "r") as f:
        countries = f.read().splitlines()
    return countries


def get_booking_page(session, offset, rooms, country, dest_id, DayIni, DayFim):

    print('get_booking_page(session, offset, rooms, country, dest_id, DayIni, DayFim):')
    print(session, offset, rooms, country, dest_id, DayIni, DayFim)

    diaInicial = str(int(DayIni[0:2]))
    mesInicial = str(int(DayIni[3:5]))
    anoInicial = str(int(DayIni[6:10]))

    diaFinal = str(int(DayFim[0:2]))
    mesFinal = str(int(DayFim[3:5]))
    anoFinal = str(int(DayFim[6:10]))

    '''
    Make request to airbnb page and parse html
    :param offset:
    :return: html page
    '''


    url = 'https://www.airbnb.com.br/s/Londres/'\
          'homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&source=mc_search_bar&search_type=unknown'\
          '&click_referer=t%3ASEE_ALL%7Csid%3A874f16ee-6196-4289-9717-17dec73e1e5c%7Cst%3AMAGAZINE_HOMES&screen_size=large&hide_dates_and_guests_filters=false'\
          '&ne_lat=51.80546533345978&ne_lng=0.4969575708007312&sw_lat=51.17528882051496&sw_lng=-0.8200285131836154&zoom=10&search_by_map=false&checkin={anoInicial}-{mesInicial}-{diaInicial}'\
          '&checkout={anoFinal}-{mesFinal}-{diaFinal}&adults={rooms}&property_type_id%5B%5D=1&property_type_id%5B%5D=43&property_type_id%5B%5D=47'\
          '&place_id=ChIJdd4hrwug2EcRmSrV3Vo6llI&room_types%5B%5D=Entire%20home%2Fapt'\
          '&section_offset=6&items_offset=18'.format(rooms=rooms, country=country.replace(' ', '+'),anoFinal=anoFinal,mesFinal=mesFinal,diaInicial=diaInicial,mesInicial=mesInicial,anoInicial=anoInicial,diaFinal=diaFinal,dest_id=dest_id) + str(offset)

    r = requests.get(url, headers=
      {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)'
                     ' Gecko/20100101 Firefox/48.0'})
    html = r.content

    print(url)
    parsed_html = BeautifulSoup(html, 'lxml')
    return parsed_html


def process_hotels(session, offset, rooms, country, dest_id, DayIni, DayFim):
    parsed_html = get_booking_page(session, offset, rooms, country, dest_id,DayIni, DayFim)
    hotel = parsed_html.find_all('div', {'class': 'sr_item'})
    for ho in hotel:
        #print("ho.find('a', {'class': 'jq_tooltip'})")
        #print(ho.find('a', {'class': 'jq_tooltip'}))
        #name = ho.find('a', {'class': 'jq_tooltip'})['data-title']
        print("ho.find('span', {'class': 'sr-hotel__name'})")
        #print(ho.find('span', {'class': 'sr-hotel__name'}))

        if ho.find('span', {'class': 'sr-hotel__name'}) is not None:
            name = str(ho.find('span', {'class': 'sr-hotel__name'}).text.encode('utf-8')).replace('\\n','').replace("b","").replace("'","").replace('\\','')
        else:
            name = '-1'

        if ho.find('div', {'class': 'bui-price-display__value prco-inline-block-maker-helper'}) is not None:
            price = ho.find('div', {'class': 'bui-price-display__value prco-inline-block-maker-helper'}).text.replace('\n','').replace("b","").replace("'","")
        else:
            price = '-1'

        if ho.find('span', {'class': '_ky9opu0'}) is not None:
            nota = str(ho.find('span', {'class': '_ky9opu0'}).text.replace('\n','').replace("b","").replace("'",""))
        else :
            nota = '-1'

        if ho.find('span', {'title': 'This is the straight-line distance on the map. Actual travel distance may vary.'}) is not None:
            distance = str(ho.find('span', {'title': 'This is the straight-line distance on the map. Actual travel distance may vary.'}).text.encode('utf-8')).replace('\\n','').replace("b","").replace("'","").replace('\\','')
        else :
            distance = '-1'

        # if ho.find('a', {'class': 'bui-link'}) is not None :
        #     result = [str(item) for item in ho.find_all('span', attrs={'data-bui-component' : 'Tooltip'})]
        #     print('TAMANHO TOOLTIP', str(len(result)))
        #     for i in result:
        #         print(i)
        #     for i in result:
        #         if i in 'km':
        #             distance = str(i)
        #         else:
        #             distance = '----'
        #     else:
        #         distance = '----'

        #     if len(result) ==1:
        #         if result[0] in 'km':
        #             distance = result
        #     else:

        #         distance = 'aaaaa' + str(len(result))
        # else:
        #     distance = '---'


        hotels.append(DayIni+';'+DayFim+';'+name + ';' + price + ';' + nota + ';' + distance)
        #hotels.append(str(len(hotels) + 1) + ' : ' + name + ' : ' + price)


def prep_data(rooms=1, country='Macedonia', dest_id='-1', DayIni='01/01/2019', DayFim='02/01/2019', out_format=None):
    '''
    Prepare data for saving
    :return: hotels: set()
    '''
    offset = 1

    session = requests.Session()

    parsed_html = get_booking_page(session, offset, rooms, country, dest_id, DayIni,DayFim)
    all_offset = parsed_html.find_all('li', {'class':
                                      'sr_pagination_item'})[-1].get_text().splitlines()[-1]
    threads = []
    for i in range(int(all_offset)):
        offset += 1
        t = BookingThread(session, offset, rooms, country,dest_id,DayIni, DayFim, process_hotels)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    hotels2 = hotels
    return hotels2


def get_data(rooms=1, country='Macedonia', dest_id='-1',DayIni='01/01/2019',DayFim='02/01/2019', out_format=None):
    '''
    Get all accomodations in Macedonia and save them in file
    :return: hotels-in-macedonia.{txt/csv/xlsx} file
    '''
    print('Procurando por',country)
    hotels_list = prep_data(rooms, country,dest_id, DayIni, DayFim, out_format)
    save_data(hotels_list , out_format=out_format, country=country)


def save_data(data, out_format, country):
    '''
    Saves hotels list in file
    :param data: hotels list
    :param out_format: json, csv or excel
    :return:
    '''
    writer = FileWriter(data, out_format, country)
    file = writer.output_file()

    print('All accommodations are saved.')
    print('You can find them in', file, 'file')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    countries = get_countries()


    parser.add_argument("--rooms",
                        help='Add the number of rooms to the booking request.',
                        default=1,
                        type=int,
                        nargs='?')
    parser.add_argument("--country",
                        help='Add the country to the booking request.',
                        default='Macedonia',
                        nargs='?').completer = ChoicesCompleter(countries)
    parser.add_argument("--dest_id",
                        help='Add the country to the booking request.',
                        default='0',
                        nargs='?')
    parser.add_argument("--DayIni",
                        help='Data inicial',
                        default='01/01/2019',
                        nargs='?')
    parser.add_argument("--DayFim",
                        help='Data inicial',
                        default='02/01/2019',
                        nargs='?')
    parser.add_argument("--out_format",
                        help='Add the format for the output file. Add excel, json or csv.',
                        default='json',
                        choices=['json', 'excel', 'csv'],
                        nargs='?').completer = EnvironCompleter

    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    localidades = [{
        'Pais': 'London',
        'dest_id': '-2601889'
    }, {
        'Pais': 'Utrecht',
        'dest_id': '-2154382'
    }, {
        'Pais': 'Buzios',
        'dest_id': '-626254'
    }, {
        'Pais': '',
        'dest_id': ''
    }]

    countryAux = [d['Pais'] for d in localidades if args.dest_id in d['dest_id']]
    if len(countryAux)>0:
        country = countryAux[0]
        print('Parametros')
        print(args.rooms, country,args.dest_id,args.DayIni,args.DayFim, args.out_format)
        get_data(args.rooms, country,args.dest_id,args.DayIni,args.DayFim, args.out_format)
    else:
        country = 'Nao Identificado'

        locais = [d['Pais'] + ':' + d['dest_id']  for d in localidades if d['Pais'] != '']
        print('----------')
        print('Utilize uma das seguintes localizações')
        for i in locais:
            print(i)
        print('----------')





