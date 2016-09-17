import pandas as pd

def get_income_data():
    df = pd.read_excel('data/logs.xlsx', 'Income')
    df = df[['ID', 'Date', 'Category', 'Name', 'Price', 'Paid', 'Description']]
    df['Attendance'] = df['ID'].apply(lambda p: bool(p))
    df['Paid'] = df['Paid'].apply(lambda p: True if p == 'Yes' else False)
    df['Balance'] = df.apply(lambda row: row['Price'] if row['Paid'] else 0, axis=1)
    df['Owes'] = df.apply(lambda row: row['Price'] if not row['Paid'] else 0, axis=1)
    df['ID'] = df['ID'].apply(lambda i: '%010d' % i)
    df['Year'] = df['Date'].apply(lambda d: d.year)
    df['Month'] = df['Date'].apply(lambda d: d.month)
    return df


def get_expense_data():
    df = pd.read_excel('data/logs.xlsx', 'Expense')
    df = df[['ID', 'Date', 'Category', 'Name', 'Price', 'Receipt', 'Description']]
    df['Receipt'] = df['Receipt'].apply(lambda p: True if p == 'Yes' else False)
    df['ID'] = df['ID'].apply(lambda i: '%010d' % i)
    df['Year'] = df['Date'].apply(lambda d: d.year)
    df['Month'] = df['Date'].apply(lambda d: d.month)
    return df
