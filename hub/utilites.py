from datetime import date, datetime, timedelta


from logger import getLogger
log = getLogger(__name__)

TODAY = date.today
NOW = datetime.now().time
MONTH = datetime.now().month
