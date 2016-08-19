import datetime
import constants
import argparse




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True, help='name of a template')
    parser.add_argument('--params', default='', help='a=b,x=y...')

    args = parser.parse_args()

    params = dict([a.split('=') for a in args.params.split(',')])
    defaults = dict([(d, getattr(constants, d)) for d in dir(constants) if not d.startswith('_')])

    template_params = defaults.copy()
    template_params.update(params)

    with open('templates/%s.md' % args.template, 'r') as f:
        lines = ''.join(f.readlines())

        email = lines.format(**template_params)

    with open('emails/%s-%s.md' % (datetime.date.today(), args.template), 'w') as f:
        f.write(email)
