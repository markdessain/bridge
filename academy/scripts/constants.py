from datetime import datetime, date, time, timedelta

name = ' Walmer Castle Bridge Group'

venue = 'The Walmer Castle'
venue_website = 'https://www.walmercastlenottinghill.co.uk/'
venue_map = 'https://goo.gl/maps/QcMgQpUAovE2'

start = time(19, 15)
bridge_start = (datetime.combine(date.today(), start) + timedelta(minutes=15)).time()
end = time(22, 15)

date_format = '%a %d %b %Y'

director = 'Mark Dessain'
director_email = ''
director_phone = ''

director_first = 'I'

currency = '&pound;'

price = '&pound;10'

bridgewebs_club = 'ruffclub'

scoring_unit = '%'
