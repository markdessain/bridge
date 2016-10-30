import datetime
import argparse
import subprocess

import requests
from bs4 import BeautifulSoup

import constants


def standard_email(template, template_params):
    with open('markdown_templates/%s.md' % template, 'r') as f:
        lines = ''.join(f.readlines())
        email = lines.format(**template_params)

    path = 'emails/%s-%s.md' % (datetime.date.today(), template)
    with open(path, 'w') as f:
        f.write(email)

    return path


def results_email(template, template_params):
    r = requests.get('http://www.bridgewebs.com/cgi-bin/bwoi/bw.cgi?pid=display_rank&event=%s&club=%s' % (
        template_params['session_id'],
        template_params['bridgewebs_club']
    ))
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    results = soup.find(id='results_main')
    table = results.find('table').find('table')

    results = []

    for pair in table.find_all('tr')[1:]:
        row = pair.find_all('td')
        results.append('|{}|{}{}|'.format(
            row[2].find('div', class_='r_show').text,
            row[5].text,
            template_params['scoring_unit']
        ))

    template_params['results'] = '\n'.join(results)
    template_params['bridgewebs_results_title'] = soup.find(id='result_title').find('span').text

    return standard_email(template, template_params)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True, help='name of a template')
    parser.add_argument('--params', default='', help='a=b,x=y...')

    args = parser.parse_args()

    params = dict([a.split('=') for a in args.params.split(',')]) if args.params else {}
    defaults = dict([(d, getattr(constants, d)) for d in dir(constants) if not d.startswith('_')])

    template_params = defaults.copy()
    template_params.update(params)

    if args.template in ('results'):
        func = results_email
    else:
        func = standard_email

    path = func(args.template, template_params)
