from bs4 import BeautifulSoup
from tika import parser
import requests
import re
import json

def change_chars(string):
    if 'ქ' in string: string = string.replace('ქ', 'q')
    if 'წ' in string: string = string.replace('წ', 'w')
    if 'ე' in string: string = string.replace('ე', 'e')
    if 'რ' in string: string = string.replace('რ', 'r')
    if 'ტ' in string: string = string.replace('ტ', 't')
    if 'ყ' in string: string = string.replace('ყ', 'y')
    if 'უ' in string: string = string.replace('უ', 'u')
    if 'ი' in string: string = string.replace('ი', 'i')
    if 'ო' in string: string = string.replace('ო', 'o')
    if 'პ' in string: string = string.replace('პ', 'p')
    if 'ა' in string: string = string.replace('ა', 'a')
    if 'ს' in string: string = string.replace('ს', 's')
    if 'დ' in string: string = string.replace('დ', 'd')
    if 'ფ' in string: string = string.replace('ფ', 'f')
    if 'გ' in string: string = string.replace('გ', 'g')
    if 'ჰ' in string: string = string.replace('ჰ', 'h')
    if 'ჯ' in string: string = string.replace('ჯ', 'j')
    if 'კ' in string: string = string.replace('კ', 'k')
    if 'ლ' in string: string = string.replace('ლ', 'l')
    if 'ზ' in string: string = string.replace('ზ', 'z')
    if 'ხ' in string: string = string.replace('ხ', 'x')
    if 'ც' in string: string = string.replace('ც', 'c')
    if 'ვ' in string: string = string.replace('ვ', 'v')
    if 'ბ' in string: string = string.replace('ბ', 'b')
    if 'ნ' in string: string = string.replace('ნ', 'n')
    if 'მ' in string: string = string.replace('მ', 'm')
    if 'ჭ' in string: string = string.replace('ჭ', 'W')
    if 'ღ' in string: string = string.replace('ღ', 'R')
    if 'თ' in string: string = string.replace('თ', 'T')
    if 'შ' in string: string = string.replace('შ', 'S')
    if 'ჟ' in string: string = string.replace('ჟ', 'J')
    if 'ძ' in string: string = string.replace('ძ', 'Z')
    if 'ჩ' in string: string = string.replace('ჩ', 'C')
    return string

def rreplace(string: str, find: str, replace: str, n_occurences: int) -> str:
    """
    Given a `string`, `find` and `replace` the first `n_occurences`
    found from the right of the string.
    """
    temp = string.rsplit(find, n_occurences)
    return replace.join(temp)

URL = 'https://info.police.ge/page?id=102'
new_url = dict()
month_urls = dict()
soup = BeautifulSoup(requests.get(URL).text, 'lxml')

def scrape():
    for a in soup.find_all('a', href=True):
        if 'წელი' in a.text:
            tmp_request = requests.get(f"https://info.police.ge{a['href']}")
            tmp_soup = BeautifulSoup(tmp_request.text, "lxml")
            for a_tmp in tmp_soup.find_all('a', href=True):
                if 'ორდერები' in a_tmp.text:
                    if 'info.police.ge' in a_tmp['href']:
                        integerstring=""
                        for i in a_tmp.text:
                            if i.isdigit()==True:
                                integerstring=integerstring+i
                        if integerstring == '':
                            new_url['2022'] = rreplace(string=a_tmp['href'], find='..', replace='', n_occurences=a_tmp['href'].count('.') - 1)
                        else:
                            new_url[integerstring] = rreplace(string=a_tmp['href'], find='..', replace='', n_occurences=a_tmp['href'].count('.') - 1)
                    else:
                        integerstring=""
                        for i in a_tmp.text:
                            if i.isdigit()==True:
                                integerstring=integerstring+i
                        if integerstring == '':
                            new_url['2022'] = f"https://info.police.ge{rreplace(string=a_tmp['href'], find='..', replace='', n_occurences=a_tmp['href'].count('.') - 1)}"
                        else:
                            new_url[integerstring] = f"https://info.police.ge{rreplace(string=a_tmp['href'], find='..', replace='', n_occurences=a_tmp['href'].count('.') - 1)}"
                    break
    return new_url

def scrape_month():
    month_soup = BeautifulSoup(requests.get('https://info.police.ge/page?id=628&parent_id=102').text, 'lxml')
    for a in month_soup.find_all('a', href=True):
        if 'ორდერები' in a.text:
            month_urls[change_chars(a.text.split('(')[1][:-2])] = f"https://info.police.ge{rreplace(string=a['href'], find='..', replace='', n_occurences=a['href'].count('.') - 1)}"
        
    return month_urls

for key, value in scrape().items():   
    rawText = parser.from_file(value)
    rawList = rawText['content'].splitlines()
    if key == '2017':
            for i in rawList:
                if 'სულ აჭარა' in i:
                    tmp_data = i.split(' ')
                    data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                    with open(f'2017.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))

                elif 'სულ გურია' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

                elif 'სულ თბილისი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ იმერეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ კახეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ მცხეთა-მთიანეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ რაჭა-ლეჩხუმი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ სამეგრელო-ზემო სვანეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                                'Neglect': int(tmp_data[8]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ სამცხე-ჯავახეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                                'Neglect': int(tmp_data[7]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ ქვემო ქართლი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                                'Neglect': int(tmp_data[8]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ შიდა ქართლი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                                'Neglect': int(tmp_data[8]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ საქართველო' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2017.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2017.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    elif key == '2015':
            for i in rawList:
                if 'სულ აჭარა' in i:
                    tmp_data = i.split(' ')
                    data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                    with open(f'2015.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))

                elif 'სულ გურია' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

                elif 'სულ თბილისი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ იმერეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ კახეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ მცხეთა-მთიანეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ რაჭა-ლეჩხუმი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ სამეგრელო-ზემო სვანეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ სამცხე-ჯავახეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ ქვემო ქართლი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ შიდა ქართლი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ საქართველო' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2015.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2015.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    elif key == '2016':
            for i in rawList:
                if 'სულ აჭარა' in i:
                    tmp_data = i.split(' ')
                    data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                    with open(f'2016.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))

                elif 'სულ გურია' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

                elif 'სულ თბილისი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ იმერეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ კახეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ მცხეთა-მთიანეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ რაჭა-ლეჩხუმი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ სამეგრელო-ზემო სვანეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ სამცხე-ჯავახეთი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ ქვემო ქართლი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ შიდა ქართლი' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1]) + change_chars(tmp_data[2])): {
                                'Physical': int(tmp_data[3]),
                                'Psycological': int(tmp_data[4]),
                                'Economical': int(tmp_data[5]),
                                'Sexual': int(tmp_data[6]),
                                'Compulsive': int(tmp_data[7]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
                elif 'სულ საქართველო' in i:
                        tmp_data = i.split(' ')
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Physical': int(tmp_data[2]),
                                'Psycological': int(tmp_data[3]),
                                'Economical': int(tmp_data[4]),
                                'Sexual': int(tmp_data[5]),
                                'Compulsive': int(tmp_data[6]),
                            }
                        }
                        with open(f'2016.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2016.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

    elif key == '2020':
        for i in rawList:
            if 'აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<16': int(tmp_data[6]),
                                    '17-24': int(tmp_data[7]),
                                    '25-44': int(tmp_data[8]),
                                    '45>': int(tmp_data[9]),
                                },
                                'Female': {
                                    'All': int(tmp_data[10]),
                                    'Unknown': int(tmp_data[11]),
                                    '<16': int(tmp_data[12]),
                                    '17-24': int(tmp_data[13]),
                                    '25-44': int(tmp_data[14]),
                                    '45>': int(tmp_data[15]),
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[16]),
                                    'Unknown': int(tmp_data[17]),
                                    '<16': int(tmp_data[18]),
                                    '17-24': int(tmp_data[19]),
                                    '25-44': int(tmp_data[20]),
                                    '45>': int(tmp_data[21]),
                                },
                                'Female': {
                                    'All': int(tmp_data[22]),
                                    'Unknown': int(tmp_data[23]),
                                    '<16': int(tmp_data[24]),
                                    '17-24': int(tmp_data[25]),
                                    '25-44': int(tmp_data[26]),
                                    '45>': int(tmp_data[27]),
                                }
                            }
                        }
                    }
                    with open(f'2020.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'რაჭა-ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            
            if 'რაჭა-ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

            if 'მცხეთა-მთიანეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<16': int(tmp_data[5]),
                                        '17-24': int(tmp_data[6]),
                                        '25-44': int(tmp_data[7]),
                                        '45>': int(tmp_data[8]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[9]),
                                        'Unknown': int(tmp_data[10]),
                                        '<16': int(tmp_data[11]),
                                        '17-24': int(tmp_data[12]),
                                        '25-44': int(tmp_data[13]),
                                        '45>': int(tmp_data[14]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[15]),
                                        'Unknown': int(tmp_data[16]),
                                        '<16': int(tmp_data[17]),
                                        '17-24': int(tmp_data[18]),
                                        '25-44': int(tmp_data[19]),
                                        '45>': int(tmp_data[20]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[21]),
                                        'Unknown': int(tmp_data[22]),
                                        '<16': int(tmp_data[23]),
                                        '17-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45>': int(tmp_data[26]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სამცხე-ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<16': int(tmp_data[5]),
                                        '17-24': int(tmp_data[6]),
                                        '25-44': int(tmp_data[7]),
                                        '45>': int(tmp_data[8]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[9]),
                                        'Unknown': int(tmp_data[10]),
                                        '<16': int(tmp_data[11]),
                                        '17-24': int(tmp_data[12]),
                                        '25-44': int(tmp_data[13]),
                                        '45>': int(tmp_data[14]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[15]),
                                        'Unknown': int(tmp_data[16]),
                                        '<16': int(tmp_data[17]),
                                        '17-24': int(tmp_data[18]),
                                        '25-44': int(tmp_data[19]),
                                        '45>': int(tmp_data[20]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[21]),
                                        'Unknown': int(tmp_data[22]),
                                        '<16': int(tmp_data[23]),
                                        '17-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45>': int(tmp_data[26]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '630' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            'Sida ' + str(change_chars(tmp_data[2])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[5]),
                                        'Unknown': int(tmp_data[6]),
                                        '<16': int(tmp_data[7]),
                                        '17-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45>': int(tmp_data[10]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<16': int(tmp_data[13]),
                                        '17-24': int(tmp_data[14]),
                                        '25-44': int(tmp_data[15]),
                                        '45>': int(tmp_data[16]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[17]),
                                        'Unknown': int(tmp_data[18]),
                                        '<16': int(tmp_data[19]),
                                        '17-24': int(tmp_data[20]),
                                        '25-44': int(tmp_data[21]),
                                        '45>': int(tmp_data[22]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[23]),
                                        'Unknown': int(tmp_data[24]),
                                        '<16': int(tmp_data[25]),
                                        '17-24': int(tmp_data[26]),
                                        '25-44': int(tmp_data[27]),
                                        '45>': int(tmp_data[28]),
                                    }
                                }
                            }
                        }
            if 'ქართლი' in i and '902' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 100: pass
                    else:
                        data = {
                            'qvemo ' + str(change_chars(tmp_data[2])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[5]),
                                        'Unknown': int(tmp_data[6]),
                                        '<16': int(tmp_data[7]),
                                        '17-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45>': int(tmp_data[10]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<16': int(tmp_data[13]),
                                        '17-24': int(tmp_data[14]),
                                        '25-44': int(tmp_data[15]),
                                        '45>': int(tmp_data[16]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[17]),
                                        'Unknown': int(tmp_data[18]),
                                        '<16': int(tmp_data[19]),
                                        '17-24': int(tmp_data[20]),
                                        '25-44': int(tmp_data[21]),
                                        '45>': int(tmp_data[22]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[23]),
                                        'Unknown': int(tmp_data[24]),
                                        '<16': int(tmp_data[25]),
                                        '17-24': int(tmp_data[26]),
                                        '25-44': int(tmp_data[27]),
                                        '45>': int(tmp_data[28]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 28: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2020.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2020.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

    elif key == '2019':
        for i in rawList:
            if 'აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<16': int(tmp_data[6]),
                                    '17-24': int(tmp_data[7]),
                                    '25-44': int(tmp_data[8]),
                                    '45>': int(tmp_data[9]),
                                },
                                'Female': {
                                    'All': int(tmp_data[10]),
                                    'Unknown': int(tmp_data[11]),
                                    '<16': int(tmp_data[12]),
                                    '17-24': int(tmp_data[13]),
                                    '25-44': int(tmp_data[14]),
                                    '45>': int(tmp_data[15]),
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[16]),
                                    'Unknown': int(tmp_data[17]),
                                    '<16': int(tmp_data[18]),
                                    '17-24': int(tmp_data[19]),
                                    '25-44': int(tmp_data[20]),
                                    '45>': int(tmp_data[21]),
                                },
                                'Female': {
                                    'All': int(tmp_data[22]),
                                    'Unknown': int(tmp_data[23]),
                                    '<16': int(tmp_data[24]),
                                    '17-24': int(tmp_data[25]),
                                    '25-44': int(tmp_data[26]),
                                    '45>': int(tmp_data[27]),
                                }
                            }
                        }
                    }
                    with open(f'2019.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'რაჭა-ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'მცხეთა-მთიანეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<16': int(tmp_data[5]),
                                        '17-24': int(tmp_data[6]),
                                        '25-44': int(tmp_data[7]),
                                        '45>': int(tmp_data[8]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[9]),
                                        'Unknown': int(tmp_data[10]),
                                        '<16': int(tmp_data[11]),
                                        '17-24': int(tmp_data[12]),
                                        '25-44': int(tmp_data[13]),
                                        '45>': int(tmp_data[14]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[15]),
                                        'Unknown': int(tmp_data[16]),
                                        '<16': int(tmp_data[17]),
                                        '17-24': int(tmp_data[18]),
                                        '25-44': int(tmp_data[19]),
                                        '45>': int(tmp_data[20]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[21]),
                                        'Unknown': int(tmp_data[22]),
                                        '<16': int(tmp_data[23]),
                                        '17-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45>': int(tmp_data[26]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სამცხე-ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '891' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 29: pass
                    else:
                        data = {
                            'qvemo ' + str(change_chars(tmp_data[2])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[5]),
                                        'Unknown': int(tmp_data[6]),
                                        '<16': int(tmp_data[7]),
                                        '17-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45>': int(tmp_data[10]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<16': int(tmp_data[13]),
                                        '17-24': int(tmp_data[14]),
                                        '25-44': int(tmp_data[15]),
                                        '45>': int(tmp_data[16]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[17]),
                                        'Unknown': int(tmp_data[18]),
                                        '<16': int(tmp_data[19]),
                                        '17-24': int(tmp_data[20]),
                                        '25-44': int(tmp_data[21]),
                                        '45>': int(tmp_data[22]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[23]),
                                        'Unknown': int(tmp_data[24]),
                                        '<16': int(tmp_data[25]),
                                        '17-24': int(tmp_data[26]),
                                        '25-44': int(tmp_data[27]),
                                        '45>': int(tmp_data[28]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '637' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 29: pass
                    else:
                        data = {
                            'Sida ' + str(change_chars(tmp_data[2])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[5]),
                                        'Unknown': int(tmp_data[6]),
                                        '<16': int(tmp_data[7]),
                                        '17-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45>': int(tmp_data[10]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<16': int(tmp_data[13]),
                                        '17-24': int(tmp_data[14]),
                                        '25-44': int(tmp_data[15]),
                                        '45>': int(tmp_data[16]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[17]),
                                        'Unknown': int(tmp_data[18]),
                                        '<16': int(tmp_data[19]),
                                        '17-24': int(tmp_data[20]),
                                        '25-44': int(tmp_data[21]),
                                        '45>': int(tmp_data[22]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[23]),
                                        'Unknown': int(tmp_data[24]),
                                        '<16': int(tmp_data[25]),
                                        '17-24': int(tmp_data[26]),
                                        '25-44': int(tmp_data[27]),
                                        '45>': int(tmp_data[28]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 28: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2019.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2019.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

    elif key == '2018':
        for i in rawList:
            if 'აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<16': int(tmp_data[6]),
                                    '17-24': int(tmp_data[7]),
                                    '25-44': int(tmp_data[8]),
                                    '45>': int(tmp_data[9]),
                                },
                                'Female': {
                                    'All': int(tmp_data[10]),
                                    'Unknown': int(tmp_data[11]),
                                    '<16': int(tmp_data[12]),
                                    '17-24': int(tmp_data[13]),
                                    '25-44': int(tmp_data[14]),
                                    '45>': int(tmp_data[15]),
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[16]),
                                    'Unknown': int(tmp_data[17]),
                                    '<16': int(tmp_data[18]),
                                    '17-24': int(tmp_data[19]),
                                    '25-44': int(tmp_data[20]),
                                    '45>': int(tmp_data[21]),
                                },
                                'Female': {
                                    'All': int(tmp_data[22]),
                                    'Unknown': int(tmp_data[23]),
                                    '<16': int(tmp_data[24]),
                                    '17-24': int(tmp_data[25]),
                                    '25-44': int(tmp_data[26]),
                                    '45>': int(tmp_data[27]),
                                }
                            }
                        }
                    }
                    with open(f'2018.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'რაჭა-ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'მცხეთა-მთიანეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<16': int(tmp_data[5]),
                                        '17-24': int(tmp_data[6]),
                                        '25-44': int(tmp_data[7]),
                                        '45>': int(tmp_data[8]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[9]),
                                        'Unknown': int(tmp_data[10]),
                                        '<16': int(tmp_data[11]),
                                        '17-24': int(tmp_data[12]),
                                        '25-44': int(tmp_data[13]),
                                        '45>': int(tmp_data[14]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[15]),
                                        'Unknown': int(tmp_data[16]),
                                        '<16': int(tmp_data[17]),
                                        '17-24': int(tmp_data[18]),
                                        '25-44': int(tmp_data[19]),
                                        '45>': int(tmp_data[20]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[21]),
                                        'Unknown': int(tmp_data[22]),
                                        '<16': int(tmp_data[23]),
                                        '17-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45>': int(tmp_data[26]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სამცხე-ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '683' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            'qvemo ' + str(change_chars(tmp_data[2])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[5]),
                                        'Unknown': int(tmp_data[6]),
                                        '<16': int(tmp_data[7]),
                                        '17-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45>': int(tmp_data[10]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<16': int(tmp_data[13]),
                                        '17-24': int(tmp_data[14]),
                                        '25-44': int(tmp_data[15]),
                                        '45>': int(tmp_data[16]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[17]),
                                        'Unknown': int(tmp_data[18]),
                                        '<16': int(tmp_data[19]),
                                        '17-24': int(tmp_data[20]),
                                        '25-44': int(tmp_data[21]),
                                        '45>': int(tmp_data[22]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[23]),
                                        'Unknown': int(tmp_data[24]),
                                        '<16': int(tmp_data[25]),
                                        '17-24': int(tmp_data[26]),
                                        '25-44': int(tmp_data[27]),
                                        '45>': int(tmp_data[28]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '381' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            'Sida ' + str(change_chars(tmp_data[2])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[5]),
                                        'Unknown': int(tmp_data[6]),
                                        '<16': int(tmp_data[7]),
                                        '17-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45>': int(tmp_data[10]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<16': int(tmp_data[13]),
                                        '17-24': int(tmp_data[14]),
                                        '25-44': int(tmp_data[15]),
                                        '45>': int(tmp_data[16]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[17]),
                                        'Unknown': int(tmp_data[18]),
                                        '<16': int(tmp_data[19]),
                                        '17-24': int(tmp_data[20]),
                                        '25-44': int(tmp_data[21]),
                                        '45>': int(tmp_data[22]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[23]),
                                        'Unknown': int(tmp_data[24]),
                                        '<16': int(tmp_data[25]),
                                        '17-24': int(tmp_data[26]),
                                        '25-44': int(tmp_data[27]),
                                        '45>': int(tmp_data[28]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 28: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<16': int(tmp_data[6]),
                                        '17-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45>': int(tmp_data[9]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[10]),
                                        'Unknown': int(tmp_data[11]),
                                        '<16': int(tmp_data[12]),
                                        '17-24': int(tmp_data[13]),
                                        '25-44': int(tmp_data[14]),
                                        '45>': int(tmp_data[15]),
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[16]),
                                        'Unknown': int(tmp_data[17]),
                                        '<16': int(tmp_data[18]),
                                        '17-24': int(tmp_data[19]),
                                        '25-44': int(tmp_data[20]),
                                        '45>': int(tmp_data[21]),
                                    },
                                    'Female': {
                                        'All': int(tmp_data[22]),
                                        'Unknown': int(tmp_data[23]),
                                        '<16': int(tmp_data[24]),
                                        '17-24': int(tmp_data[25]),
                                        '25-44': int(tmp_data[26]),
                                        '45>': int(tmp_data[27]),
                                    }
                                }
                            }
                        }
                        with open(f'2018.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2018.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

    elif key == '2021':
        for i in rawList:
            if 'სულ აფხაზეთი' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2021.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ აჭარა' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'მთიანეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '1693' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            'qvemo ' + str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i and '520' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            'Sida ' +str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 36: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2021.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2021.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    
for key, value in scrape_month().items():   
    rawText = parser.from_file(value)
    rawList = rawText['content'].splitlines()
    if key == 'ianvari':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Jan.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'Tebervali':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Feb.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Feb.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Feb.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'marti':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_March.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_March.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_March.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'aprili':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_April.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_April.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_April.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'maisi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_May.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_May.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_May.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'ivnisi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_June.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_June.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_June.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'ivlisi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Jule.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            
            if 'ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jule.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jule.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'ianvari-ivnisi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Jan_Jun.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
        
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Jan_Jun.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Jan_Jun.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'agvisto':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Aug.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Aug.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Aug.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'seqtemberi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Sep.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ლეჩხუმი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

            if 'მთიანეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

            if 'ქართლი' in i and '151' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            'qvemo' + str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))

            if 'ქართლი' in i and '53' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            'Sida' + str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Sep.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Sep.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'oqtomberi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Oct.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Oct.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Oct.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'noemberi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Nov.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Nov.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Nov.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
    if key == 'dekemberi':
        for i in rawList:
            if 'სულ აჭარა' in i:
                tmp_data = i.split(' ')
                if len(tmp_data) == 8: pass
                else:
                    data = {
                        str(change_chars(tmp_data[1])): {
                            'Victims': {
                                'Male': {
                                    'All': int(tmp_data[4]),
                                    'Unknown': int(tmp_data[5]),
                                    '<13': int(tmp_data[6]),
                                    '14-17': int(tmp_data[7]),
                                    '18-24': int(tmp_data[8]),
                                    '25-44': int(tmp_data[9]),
                                    '45-60': int(tmp_data[10]),
                                    '61>': int(tmp_data[11])
                                },
                                'Female': {
                                    'All': int(tmp_data[12]),
                                    'Unknown': int(tmp_data[13]),
                                    '<13': int(tmp_data[14]),
                                    '14-17': int(tmp_data[15]),
                                    '18-24': int(tmp_data[16]),
                                    '25-44': int(tmp_data[17]),
                                    '45-60': int(tmp_data[18]),
                                    '61>': int(tmp_data[19])
                                }
                            },
                            'Abusers': {
                                'Male': {
                                    'All': int(tmp_data[20]),
                                    'Unknown': int(tmp_data[21]),
                                    '<13': int(tmp_data[22]),
                                    '14-17': int(tmp_data[23]),
                                    '18-24': int(tmp_data[24]),
                                    '25-44': int(tmp_data[25]),
                                    '45-60': int(tmp_data[26]),
                                    '61>': int(tmp_data[27])
                                },
                                'Female': {
                                    'All': int(tmp_data[28]),
                                    'Unknown': int(tmp_data[29]),
                                    '<13': int(tmp_data[30]),
                                    '14-17': int(tmp_data[31]),
                                    '18-24': int(tmp_data[32]),
                                    '25-44': int(tmp_data[33]),
                                    '45-60': int(tmp_data[34]),
                                    '61>': int(tmp_data[35])
                                }
                            }
                        }
                    }
                    with open(f'2022_Dec.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
            if 'სულ გურია' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ თბილისი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ იმერეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სულ კახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'სვანეთი' in i and 'სამეგრელო-ზემო' not in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[1])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[4]),
                                        'Unknown': int(tmp_data[5]),
                                        '<13': int(tmp_data[6]),
                                        '14-17': int(tmp_data[7]),
                                        '18-24': int(tmp_data[8]),
                                        '25-44': int(tmp_data[9]),
                                        '45-60': int(tmp_data[10]),
                                        '61>': int(tmp_data[11])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[12]),
                                        'Unknown': int(tmp_data[13]),
                                        '<13': int(tmp_data[14]),
                                        '14-17': int(tmp_data[15]),
                                        '18-24': int(tmp_data[16]),
                                        '25-44': int(tmp_data[17]),
                                        '45-60': int(tmp_data[18]),
                                        '61>': int(tmp_data[19])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[20]),
                                        'Unknown': int(tmp_data[21]),
                                        '<13': int(tmp_data[22]),
                                        '14-17': int(tmp_data[23]),
                                        '18-24': int(tmp_data[24]),
                                        '25-44': int(tmp_data[25]),
                                        '45-60': int(tmp_data[26]),
                                        '61>': int(tmp_data[27])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[28]),
                                        'Unknown': int(tmp_data[29]),
                                        '<13': int(tmp_data[30]),
                                        '14-17': int(tmp_data[31]),
                                        '18-24': int(tmp_data[32]),
                                        '25-44': int(tmp_data[33]),
                                        '45-60': int(tmp_data[34]),
                                        '61>': int(tmp_data[35])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ჯავახეთი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) == 8: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'ქართლი' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))
            if 'საქართველო' in i:
                    tmp_data = i.split(' ')
                    if len(tmp_data) != 35: pass
                    else:
                        data = {
                            str(change_chars(tmp_data[0])): {
                                'Victims': {
                                    'Male': {
                                        'All': int(tmp_data[3]),
                                        'Unknown': int(tmp_data[4]),
                                        '<13': int(tmp_data[5]),
                                        '14-17': int(tmp_data[6]),
                                        '18-24': int(tmp_data[7]),
                                        '25-44': int(tmp_data[8]),
                                        '45-60': int(tmp_data[9]),
                                        '61>': int(tmp_data[10])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[11]),
                                        'Unknown': int(tmp_data[12]),
                                        '<13': int(tmp_data[13]),
                                        '14-17': int(tmp_data[14]),
                                        '18-24': int(tmp_data[15]),
                                        '25-44': int(tmp_data[16]),
                                        '45-60': int(tmp_data[17]),
                                        '61>': int(tmp_data[18])
                                    }
                                },
                                'Abusers': {
                                    'Male': {
                                        'All': int(tmp_data[19]),
                                        'Unknown': int(tmp_data[20]),
                                        '<13': int(tmp_data[21]),
                                        '14-17': int(tmp_data[22]),
                                        '18-24': int(tmp_data[23]),
                                        '25-44': int(tmp_data[24]),
                                        '45-60': int(tmp_data[25]),
                                        '61>': int(tmp_data[26])
                                    },
                                    'Female': {
                                        'All': int(tmp_data[27]),
                                        'Unknown': int(tmp_data[28]),
                                        '<13': int(tmp_data[29]),
                                        '14-17': int(tmp_data[30]),
                                        '18-24': int(tmp_data[31]),
                                        '25-44': int(tmp_data[32]),
                                        '45-60': int(tmp_data[33]),
                                        '61>': int(tmp_data[34])
                                    }
                                }
                            }
                        }
                        with open(f'2022_Dec.json') as f:
                            tmp = json.loads(f.read())
                        tmp.update(data)
                        with open(f'2022_Dec.json', 'w') as f:
                            f.write(json.dumps(tmp, indent=4))