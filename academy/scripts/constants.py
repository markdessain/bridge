from datetime import datetime, date, time, timedelta

name = 'Holland Park Bridge Group'

venue = 'The Castle'
venue_website = 'https://www.castlehollandpark.co.uk/'
venue_map = 'https://goo.gl/maps/AabBbGnSKvq'

start = time(19, 15)
bridge_start = (datetime.combine(date.today(), start) + timedelta(minutes=15)).time()
end = time(22, 15)

date_format = '%a %d %b %Y'

director = 'Mark Dessain'
director_email = ''
director_phone = ''
currency = '&pound;'

price = '&pound;10'

bridgewebs_club = 'ruffclub'

scoring_unit = '%'
