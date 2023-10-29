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
non_cur_assets = get_tbl_el(non_cur_assets_df, 'Итого внеоборотных активов', LAST_YEAR)
stocks = get_tbl_el(cur_assets_df, 'Запасы', LAST_YEAR)
dbt_dolg  = get_tbl_el(cur_assets_df, 'Дебиторская задолженность', LAST_YEAR)
other_NCA = int((balance_row[-1]) - (non_cur_assets + stocks + dbt_dolg))

balance_asset_structure = [non_cur_assets, stocks, dbt_dolg, other_NCA]

own_capital = get_tbl_el(capital_and_stocks_df, 'ИТОГО капитал', LAST_YEAR)
long_obl = get_tbl_el(long_obl_df, 'ИТОГО долгосрочных обязательств', LAST_YEAR)
short_obl = get_tbl_el(short_obl_df, 'ИТОГО краткосрочных обязательств', LAST_YEAR)

balance_passive_structure = [own_capital, long_obl, short_obl]

# ===========ОФР===========
ebit_row = get_tbl_row(others_profit_loss_df, 'Прибыль (убыток) до налогообложения')

ofr_col_names = ['Выручка', 'Чистая прибыль', 'EBIT', 'Год']
ofr = pd.DataFrame([income_row, clean_profit_row, ebit_row, YEARS]).T
ofr.columns = ofr_col_names


# ===========ОДДС. Сальдо от операций===========
cur_flow_saldo = get_tbl_el(cur_cash_flow_df, 'Сальдо денежных потоков от текущих операций', LAST_YEAR)
inv_flow_saldo = get_tbl_el(inv_cash_flow_df, 'Сальдо денежных потоков от инвестиционных операций', LAST_YEAR)
fin_flow_saldo = get_tbl_el(fin_cash_flow_df, 'Сальдо денежных потоков от финансовых операций', LAST_YEAR)

odds_saldo_col_names = ['Текущие операции', 'Инвестиционные операции', 'Финансовые операции']
odds_saldo = pd.DataFrame([cur_flow_saldo, inv_flow_saldo, fin_flow_saldo]).T
odds_saldo.columns = odds_saldo_col_names


# ===========ОДДС. Поступления от операций===========
cur_flow_rises = get_tbl_el(cur_cash_flow_df, 'Поступления – всего', LAST_YEAR)
inv_flow_rises = get_tbl_el(inv_cash_flow_df, 'Поступления – всего', LAST_YEAR)
fin_flow_rises = get_tbl_el(fin_cash_flow_df, 'Поступления – всего', LAST_YEAR)

odds_rises_col_names = ['Текущие операции', 'Инвестиционные операции', 'Финансовые операции']
odds_rises_cols = [cur_flow_rises, inv_flow_rises, fin_flow_rises]
odds_rises = pd.DataFrame(odds_rises_cols).T
odds_rises.columns = odds_rises_col_names