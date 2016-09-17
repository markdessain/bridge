import calendar
import datetime
import argparse

import pandas as pd
pd.set_option('expand_frame_repr', False)

from common import get_income_data, get_expense_data


def create_accounts(tax_year):
    writer = pd.ExcelWriter('data/accounts.xlsx')

    expense = get_expense_data()
    income = get_income_data()

    year_one, year_two = tax_year.split('/')

    years = ([year_one] * 9) + ([year_two] * 4)
    months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4]

    expense = expense[
        (expense.Date >= datetime.date(int(year_one), 4, 6)) &
        (expense.Date <= datetime.date(int(year_two), 4, 5))
    ]

    income = income[
        (income.Date >= datetime.date(int(year_one), 4, 6)) &
        (income.Date <= datetime.date(int(year_two), 4, 5))
    ]

    rows = []
    for year, month in zip(years, months):
        rows.append({
            'ID': '',
            'Date': datetime.date(int(year), int(month), 1),
            'Category': ' ' * 30,
            'Name': '',
            'Price': 0,
            'Receipt': False,
            'Description': '',
            'Year': int(year),
            'Month': int(month)
        })
    df = pd.DataFrame(rows)
    data = pd.concat([expense, df])

    table = pd.pivot_table(
        data,
        values=['Price'],
        index=['Category'],
        columns=['Year', 'Month'],
        aggfunc={'Price': 'sum'},
        margins=True
    )

    table = table.fillna(0.0)
    print(table.Price)

    table.Price.to_excel(writer, 'Expense')

    rows = []
    for year, month in zip(years, months):
        rows.append({
            'ID': '',
            'Date': datetime.date(int(year), int(month), 1),
            'Category': ' ' * 30,
            'Name': '',
            'Price': 0,
            'Paid': False,
            'Description': '',
            'Year': int(year),
            'Month': int(month)
        })
    df = pd.DataFrame(rows)
    data = pd.concat([income, df])

    table = pd.pivot_table(
        data,
        values=['Price'],
        index=['Category'],
        columns=['Year', 'Month'],
        aggfunc={'Price': 'sum'},
        margins=True
    )
    table = table.fillna(0.0)
    print(table.Price)

    table.Price.to_excel(writer, 'Income')
    writer.save()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--taxyear', required=True, help='eg 2016/2017')
    args = parser.parse_args()

    create_accounts(args.taxyear)
