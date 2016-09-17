import os
import random
import string
import datetime
import argparse

import pandas as pd
import numpy as np

import constants

from common import get_income_data


def standard_invoice(template, template_params):
    with open('templates/%s.md' % template, 'r') as f:
        lines = ''.join(f.readlines())
        email = lines.format(**template_params)

    directory = 'invoices/%s-%s/' % (
        template_params['year'],
        template_params['month'].zfill(2),
    )
    os.makedirs(directory, exist_ok=True)

    path = '%s/%s.md' % (
        directory,
        template_params['customer_name'].lower(),
    )
    with open(path, 'w') as f:
        f.write(email)

    return path


def create_pivot_table(data):

    table = pd.pivot_table(
        data,
        values=['Price', 'Paid', 'Attendance', 'Owes'],
        index=['Year', 'Month', 'Category', 'Name'],
        columns=[],
        aggfunc={'Owes': 'sum', 'Price': 'sum', 'Paid': 'sum', 'Attendance': 'count'},
        margins=True
    )
    return table


def invoice_numbers():
    while True:
        yield ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))


def build_invoices(year, month):
    invoice_num_gen = invoice_numbers()
    data = get_income_data()
    table = create_pivot_table(data)

    report = data[(data.Year == year) & (data.Month == month)]

    report['Date'] = report['Date'].apply(lambda d: d.strftime(constants.date_format))
    report['DisplayPrice'] = report['Price'].apply(lambda p: constants.currency + str(p))

    names = report['Name'].unique()

    for name in names:
        games = report[report.Name == name]

        summary = []

        for index, row in games[['Date', 'Category', 'DisplayPrice']].iterrows():
            summary.append('|'.join(map(str, row.tolist())))

        yield {
            'invoice_number': next(invoice_num_gen),
            'customer_name': name,
            'summary': '\n'.join(summary),
            'sub_total': games['Price'].sum(),
            'tax': 0,
            'shipping': 0,
            'total': games['Price'].sum(),
            'amount_paid': games['Price'].sum() - games['Owes'].sum(),
            'amount_owed': games['Owes'].sum(),
            'date': datetime.date.today().strftime(constants.date_format)
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', default='invoice', help='name of a template')
    parser.add_argument('--year', required=True, help='year of invoices')
    parser.add_argument('--month', required=True, help='month of invoices')
    parser.add_argument('--params', default='', help='a=b,x=y...')

    args = parser.parse_args()

    params = dict([a.split('=') for a in args.params.split(',')]) if args.params else {}
    defaults = dict([(d, getattr(constants, d)) for d in dir(constants) if not d.startswith('_')])

    params['year'] = args.year
    params['month'] = args.month

    template_params = defaults.copy()
    template_params.update(params)

    for invoice_params in build_invoices(int(args.year), int(args.month)):
        p = template_params.copy()
        p.update(invoice_params)

        path = standard_invoice(args.template, p)
