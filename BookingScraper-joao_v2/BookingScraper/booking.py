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
    Make request to booking page and parse html
    :param offset:
    :return: html page
    '''

    # url = 'https://www.booking.com/searchresults.en-gb.html?' \
    #         'aid=304142&label' \
    #         '=gen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCnd' \
    #         'pbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&' \
    #         'sid=716ea5d78c4043fd78b7a1410d639e3d&checkin_month=' \
    #         '3&checkin_monthday=15&checkin_year=2020&checkout_month=3&' \
    #         'checkout_monthday=19&checkout_year=2020' \
    #         '&class_interval=1&dest_id=125&dest_type=country&dtdisc=0&from_sf'\
    #         '=1&genius_rate=1&no_rooms={rooms}&group_adults=2&group_children=0&inac=0&' \
    #         'index_postcard=0&label_click=undef' \
    #         '&no_rooms=1&postcard=0&raw_dest_type=country&room1=' \
    #         'A%2CA&sb_price' \
    #         '_type=total&src=searchresults&src_elem=sb&ss={country}&ss_all=' \
    #         '0&ssb=empty&sshis=0&ssne={country}' \
    #         '&ssne_untouched={country}&rows=15&offset='.format(
    #             rooms=rooms,
    #             country=country.replace(' ', '+')
    #         ) + str(offset)

    url = 'https://www.booking.com/searchresults.en-gb.html?'\
          'aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCndpbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&lang=en-gb&'\
          'sid=89ae7c6b6c6eb30c9bf7124b30548c75&sb=1&src=searchresults&'\
          'src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Faid%3D304142%3Blabel%3Dgen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCndpbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID%3Bsid%3D89ae7c6b6c6eb30c9bf7124b30548c75%3Btmpl%3Dsearchresults%3B'\
          'checkin_month%3D3%3Bcheckin_monthday%3D15%3Bcheckin_year%3D2020%3Bcheckout_month%3D3%3Bcheckout_monthday%3D19%3Bcheckout_year%3D2020%3B'\
          'class_interval%3D1%3Bdest_id%3D1804067%3Bdest_type%3Dhotel%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3B'\
          'highlighted_hotels%3D1804067%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D2%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%3Broom2%3DA%3B'\
          'sb_price_type%3Dtotal%3Bsearch_pageview_id%3Df1b8635d8e6600d9%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bsrpvid%3'\
          'Defa463d50fa90102%3Bss%3Dfewo1846%2520-%2520Parklick%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3DGermany%3Bssne_untouched%3DGermany%3B'\
          'top_ufis%3D1%26%3B&{country}&'\
          'city=-1770407&checkin_year={anoInicial}&checkin_month={mesInicial}&checkin_monthday={diaInicial}&checkout_year={anoFinal}&checkout_month={mesFinal}&checkout_monthday={diaFinal}&group_adults=2&'\
          'group_children=0&no_rooms=2&from_sf=1&search_pageview_id=efa463d50fa90102&ac_suggestion_list_length=6&ac_suggestion_theme_list_length=0&ac_position=0'\
          '&ac_langcode=en&ac_click_type=b&dest_id={dest_id}&dest_type=city&iata=LON&'\
          'place_id_lat=51.507391&place_id_lon=-0.127634&search_pageview_id=efa463d50fa90102&search_selected=true&'\
          '&nflt=roomfacility%3D38%3Breview_score%3D70%3Bpri%3D4%3Bpri%3D3%3Bpri%3D2%3Bpri%3D1%3B&'\
          'ss_raw=londres&rows=15&offset='.format(rooms=rooms, country=country.replace(' ', '+'),anoFinal=anoFinal,mesFinal=mesFinal,diaInicial=diaInicial,mesInicial=mesInicial,anoInicial=anoInicial,diaFinal=diaFinal,dest_id=dest_id) + str(offset)

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


        if ho.find('div', {'class': 'bui-review-score__badge'}) is not None :
            nota = str(ho.find('div', {'class': 'bui-review-score__badge'}).text.replace('\n','').replace("b","").replace("'",""))
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
