from datetime import datetime, date, time, timedelta

name = 'Holland Park / Academy / Castle'

venue = 'The Castle Holland Park'
venue_website = 'https://www.castlehollandpark.co.uk/'
venue_map = 'https://goo.gl/maps/AabBbGnSKvq'

start = time(19, 15)
bridge_start = (datetime.combine(date.today(), start) + timedelta(minutes=15)).time()
end = time(22, 15)

director = 'Mark Dessain'
