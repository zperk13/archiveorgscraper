# Inspiration and some credit goes to The PC Geek https://youtu.be/RTZlPaGX4Mg

import requests


def get_calender_json(url, year):
    url = url.replace(':', '%3A').replace('/', '%2F').replace('&', '%26')
    json_url = f'https://web.archive.org/__wb/calendarcaptures?url={url}&selected_year={year}'
    json_response = requests.get(json_url, timeout=10)
    status_code = json_response.status_code
    if status_code != 200:
        raise Exception(f"Got status code that isn't 200: {status_code}")
    else:
        return json_response.json()


def num_of_timestamps(url, year, month_num=None):
    url = url.replace(':', '%3A').replace('/', '%2F').replace('&', '%26')
    json_url = f'https://web.archive.org/__wb/sparkline?url={url}&collection=web&output=json'
    json_response = requests.get(json_url, timeout=10)
    status_code = json_response.status_code
    if status_code != 200:
        raise Exception(f"Got status code that isn't 200: {status_code}")
    else:
        json_dict = json_response.json()
        try:
            if month_num == None:
                return sum(json_dict['years'][str(year)])
            else:
                return json_dict['years'][str(year)][month_num - 1]
        except KeyError:
            return 0


def get_years_data(url):
    url = url.replace(':', '%3A').replace('/', '%2F').replace('&', '%26')
    json_url = f'https://web.archive.org/__wb/sparkline?url={url}&collection=web&output=json'
    json_response = requests.get(json_url, timeout=10)
    status_code = json_response.status_code
    if status_code != 200:
        raise Exception(f"Got status code that isn't 200: {status_code}")
    else:
        return json_response.json()


def get_years(url):
    json_dict = get_years_data(url)
    return sorted(int(k) for k in json_dict['years'].keys())


def get_site_html_raw_date(url, raw_date):
    html = requests.get(f'https://web.archive.org/web/{raw_date}/{url}').text
    html = html.replace('''<div id="wm-ipp-base" lang="en" style="display: block; direction: ltr;">
</div>''', '')
    print(html)


def get_site_html_first(url):
    ts = get_years_data(url)
    ts = ts['first_ts']
    return get_site_html_raw_date(url, ts)


def get_site_html_last(url):
    ts = get_years_data(url)
    ts = ts['last_ts']
    return get_site_html_raw_date(url, ts)
