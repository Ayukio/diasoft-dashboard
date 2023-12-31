from src.components.data_extractor import get_first_table_from_group, get_some_table, get_tbl_row, get_tbl_el, YEARS, LAST_YEAR
import pandas as pd


BALANCE_ID, OFR_ID, CAPITAL_ID, ODDS_ID = 1, 2, 3, 4

# ===========ТАБЛИЦЫ ДЛЯ ДИАГРАММ===========
balance_df = get_first_table_from_group(BALANCE_ID)
profit_loss_df = get_some_table('Доходы и расходы по обычным видам деятельности')
capital_df = get_some_table('Итого')
non_cur_assets_df = get_some_table('Внеоборотные активы')
cur_assets_df = get_some_table('Оборотные активы')
capital_and_stocks_df = get_some_table('Капитал и резервы')
long_obl_df = get_some_table('Долгосрочные обязательства')
short_obl_df = get_some_table('Краткосрочные обязательства')
others_profit_loss_df = get_some_table('Прочие доходы и расходы')
cur_cash_flow_df =  get_some_table('Денежные потоки от текущих операций')
inv_cash_flow_df =  get_some_table('Денежные потоки от инвестиционных операций')
fin_cash_flow_df =  get_some_table('Денежные потоки от финансовых операций')


# ===========KPI КАРТОЧКИ===========
balance_row =  get_tbl_row(balance_df, 'Баланс (актив)')
income_row =  get_tbl_row(profit_loss_df, 'Выручка')
clean_profit_row = get_tbl_row(capital_df, 'Чистая прибыль')
capital_row = get_tbl_row(capital_df, 'Величина капитала на 31 декабря отчетного года')

kpi_col_names = ['Баланс', 'Выручка', 'Прибыль', 'Капитал', 'Год']
kpi = pd.DataFrame([balance_row, income_row, clean_profit_row, capital_row, YEARS]).T
kpi.columns = kpi_col_names
kpi.set_index('Год')

# ===========БУХГАЛТЕРСКИЙ БАЛАНС===========
# актив
non_cur_assets = get_tbl_row(non_cur_assets_df, 'Итого внеоборотных активов')
stocks = get_tbl_row(cur_assets_df, 'Запасы')
dbt_dolg  = get_tbl_row(cur_assets_df, 'Дебиторская задолженность')
other_NCA = [[[int((balance_row[-1]) - (i + j + k)) for i in non_cur_assets] for j in  stocks] for k in dbt_dolg][0][0]

balance_asset_structure = pd.DataFrame([non_cur_assets, stocks, dbt_dolg, other_NCA, YEARS]).T
balance_asset_structure_col_names = ["Внеоборотные активы", "Запасы", "Дебиторская задолженность", "Прочие оборотные активы", "Год"]
balance_asset_structure.columns = balance_asset_structure_col_names
balance_asset_structure.set_index('Год')

balance_asset_structure_last_year = list(balance_asset_structure.iloc[[-1]].values.tolist()[0][:-1])

# пассив
own_capital = get_tbl_row(capital_and_stocks_df, 'ИТОГО капитал')
long_obl = get_tbl_row(long_obl_df, 'ИТОГО долгосрочных обязательств')
short_obl = get_tbl_row(short_obl_df, 'ИТОГО краткосрочных обязательств')

balance_passive_structure = pd.DataFrame([own_capital, long_obl, short_obl, YEARS]).T
balance_passive_structure_col_names = ["Собственный капитал", "Долгосрочные обязательства", "Краткосрочные обязательства", "Год"]
balance_passive_structure.columns = balance_passive_structure_col_names
balance_passive_structure.set_index('Год')

balance_passive_structure_last_year = list(balance_passive_structure.iloc[[-1]].values.tolist()[0][:-1])


# ===========ОФР===========
valov_profit_row = get_tbl_row(profit_loss_df, 'Валовая прибыль (убыток)')
sales_profit_row = get_tbl_row(profit_loss_df, 'Прибыль (убыток) от продаж')
ebit_row = get_tbl_row(others_profit_loss_df, 'Прибыль (убыток) до налогообложения')

ofr_col_names = ['Выручка', 'Чистая прибыль', 'Прибыль до налогообложения', 'Валовая прибыль', 'Прибыль от продаж', 'Год']
ofr = pd.DataFrame([income_row, clean_profit_row, ebit_row, valov_profit_row, sales_profit_row, YEARS]).T
ofr.columns = ofr_col_names


# ===========ОДДС. Сальдо от операций===========
cur_flow_saldo = get_tbl_row(cur_cash_flow_df, 'Сальдо денежных потоков от текущих операций')
inv_flow_saldo = get_tbl_row(inv_cash_flow_df, 'Сальдо денежных потоков от инвестиционных операций')
fin_flow_saldo = get_tbl_row(fin_cash_flow_df, 'Сальдо денежных потоков от финансовых операций')

odds_saldo_col_names = ['Текущие операции', 'Инвестиционные операции', 'Финансовые операции', 'Год']
odds_saldo = pd.DataFrame([cur_flow_saldo, inv_flow_saldo, fin_flow_saldo, YEARS]).T
odds_saldo.columns = odds_saldo_col_names
odds_saldo.set_index('Год')

odds_saldo_last_year = odds_saldo.iloc[[-1]].iloc[: , :-1]


# ===========ОДДС. Поступления от операций===========
cur_flow_rises = get_tbl_row(cur_cash_flow_df, 'Поступления – всего')
inv_flow_rises = get_tbl_row(inv_cash_flow_df, 'Поступления – всего')
fin_flow_rises = get_tbl_row(fin_cash_flow_df, 'Поступления – всего')

odds_rises_col_names = ['Текущие операции', 'Инвестиционные операции', 'Финансовые операции', 'Год']
odds_rises = pd.DataFrame([cur_flow_rises, inv_flow_rises, fin_flow_rises, YEARS]).T
odds_rises.columns = odds_rises_col_names
odds_rises.set_index('Год')

odds_rises_last_year = list(odds_rises.iloc[[-1]].values.tolist()[0][:-1])

# ===========ОДДС. Cтруктура потоков по операциям===========
t_rise_row_19={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Поступления', 'Сумма': get_tbl_el(cur_cash_flow_df, 'Поступления – всего', '2019'), 'Год': 2019}
i_rise_row_19={'Вид операции': 'Инвестиционные операции', 'Вид денежного потока':  'Поступления', 'Сумма': get_tbl_el(inv_cash_flow_df, 'Поступления – всего', '2019'), 'Год': 2019}
f_rise_row_19={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Поступления','Сумма': get_tbl_el(fin_cash_flow_df, 'Поступления – всего', '2019'),'Год': 2019}
t_down_row_19={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(cur_cash_flow_df, 'Платежи – всего', '2019'), 'Год':2019}
i_down_row_19={'Вид операции': 'Инвестиционные операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(inv_cash_flow_df, 'Платежи – всего', '2019'), 'Год':2019}
f_down_row_19={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(fin_cash_flow_df, 'Платежи – всего', '2019'), 'Год':2019}

t_rise_row_20={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Поступления', 'Сумма':get_tbl_el(cur_cash_flow_df, 'Поступления – всего', '2020'), 'Год':2020}
i_rise_row_20={'Вид операции': 'Инвестиционные операции','Вид денежного потока':  'Поступления', 'Сумма':get_tbl_el(inv_cash_flow_df, 'Поступления – всего', '2020'), 'Год':2020}
f_rise_row_20={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Поступления', 'Сумма':get_tbl_el(fin_cash_flow_df, 'Поступления – всего', '2020'), 'Год':2020}
t_down_row_20={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(cur_cash_flow_df, 'Платежи – всего', '2020'), 'Год':2020}
i_down_row_20={'Вид операции': 'Инвестиционные операции','Вид денежного потока':  'Платежи', 'Сумма':get_tbl_el(inv_cash_flow_df, 'Платежи – всего', '2020'),'Год': 2020}
f_down_row_20={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(fin_cash_flow_df, 'Платежи – всего', '2020'), 'Год':2020}

t_rise_row_21={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Поступления','Сумма': get_tbl_el(cur_cash_flow_df, 'Поступления – всего', '2021'), 'Год':2021}
i_rise_row_21={'Вид операции': 'Инвестиционные операции', 'Вид денежного потока': 'Поступления','Сумма': get_tbl_el(inv_cash_flow_df, 'Поступления – всего', '2021'), 'Год':2021}
f_rise_row_21={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Поступления', 'Сумма':get_tbl_el(fin_cash_flow_df, 'Поступления – всего', '2021'), 'Год': 2021}
t_down_row_21={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Платежи','Сумма': get_tbl_el(cur_cash_flow_df, 'Платежи – всего', '2021'), 'Год':2021}
i_down_row_21={'Вид операции': 'Инвестиционные операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(inv_cash_flow_df, 'Платежи – всего', '2021'),'Год': 2021}
f_down_row_21={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(fin_cash_flow_df, 'Платежи – всего', '2021'), 'Год':2021}

t_rise_row_22={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Поступления','Сумма': get_tbl_el(cur_cash_flow_df, 'Поступления – всего', '2022'), 'Год':2022}
i_rise_row_22={'Вид операции': 'Инвестиционные операции', 'Вид денежного потока': 'Поступления', 'Сумма':get_tbl_el(inv_cash_flow_df, 'Поступления – всего', '2022'), 'Год':2022}
f_rise_row_22={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Поступления','Сумма': get_tbl_el(fin_cash_flow_df, 'Поступления – всего', '2022'), 'Год': 2022}
t_down_row_22={'Вид операции': 'Текущие операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(cur_cash_flow_df, 'Платежи – всего', '2022'), 'Год':2022}
i_down_row_22={'Вид операции': 'Инвестиционные операции', 'Вид денежного потока': 'Платежи','Сумма': get_tbl_el(inv_cash_flow_df, 'Платежи – всего', '2022'), 'Год':2022}
f_down_row_22={'Вид операции': 'Финансовые операции', 'Вид денежного потока': 'Платежи', 'Сумма':get_tbl_el(fin_cash_flow_df, 'Платежи – всего', '2022'), 'Год':2022}

flow_structure_19 = pd.DataFrame([t_rise_row_19, i_rise_row_19, f_rise_row_19, t_down_row_19, i_down_row_19, f_down_row_19])
flow_structure_20 = pd.DataFrame([t_rise_row_20, i_rise_row_20, f_rise_row_20, t_down_row_20, i_down_row_20, f_down_row_20])
flow_structure_21 = pd.DataFrame([t_rise_row_21, i_rise_row_21, f_rise_row_21, t_down_row_21, i_down_row_21, f_down_row_21])
flow_structure_22 = pd.DataFrame([t_rise_row_22, i_rise_row_22, f_rise_row_22, t_down_row_22, i_down_row_22, f_down_row_22])

