from datetime import datetime

print(datetime.strptime("2023-11-29T19:00:00+00:00".split('T')[0],"%Y-%m-%d").day)