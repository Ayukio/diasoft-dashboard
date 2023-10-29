import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

r = requests.get('https://vbankcenter.ru/contragent/1057746642436/finance')
# r = requests.get('https://vbankcenter.ru/contragent/1217700253671/finance')
# r = requests.get('https://vbankcenter.ru/contragent/1027700229193/finance')
soup = bs(r.text, 'lxml')

# функция для получения всех доступных названий столбцов
def get_columns():
    columns = ['Показатель']
    columns_tag = soup.find('table', {'class': 'table table-striped balance w-full text-right'})
    columns_td = columns_tag.find_all('tr')[0].find_all('td')[1:]
    for td in columns_td:
        columns.append(td.text)
    return columns


# функция для получения первой таблицы в группе
def get_first_table_from_group(form_num: int):
    data = []
    group = soup.find('div', {'id': f'form{form_num}'})
    first_table_in_group = group.find(
        'table', 
        {'class': 'table table-striped balance w-full text-right'}
    )
    first_table_all_tr = first_table_in_group.find_all('tr')[1:]
    for tr in first_table_all_tr:
        first_table_all_td = tr.find_all('td')
        first_table_all_td.pop(1)
        inner_data = []
        for td in first_table_all_td:
            inner_data.append(td.text.replace('\u00a0', ''))
        data.append(inner_data)

    first_table_df = pd.DataFrame(columns=COLUMNS, data=data)
    
    return first_table_df

# фунция для получения таблицы по названию
def get_some_table(table_name: str):
    data = []
    table_name_checkpoint = soup.find('h3', string=table_name)
    some_table_all_tr = table_name_checkpoint.find_next(
        'table', 
        {'class': 'table table-striped balance text-right w-full'}
    ).find_all('tr')
    for tr in some_table_all_tr:
        some_table_all_td = tr.find_all('td')
        some_table_all_td.pop(1)
        inner_data = []
        for td in some_table_all_td:
            inner_data.append(td.text.replace('\u00a0', ''))
        data.append(inner_data)

    some_table_df = pd.DataFrame(columns=COLUMNS, data=data)

    return some_table_df

# функция для получения строки таблицы по названию показателя
def get_tbl_row(df, param):
    return list(map(int, df[df['Показатель'] == param].values.tolist()[0][1:]))

#  функция для получения элемента строки таблицы по названию показателя и году
def get_tbl_el(df, param, year):
    return int(df[df['Показатель'] == param][year])

COLUMNS = get_columns()
YEARS = [int(x) for x in COLUMNS[1:]]
LAST_YEAR = str(YEARS[-1])