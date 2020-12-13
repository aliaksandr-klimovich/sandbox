from datetime import datetime, timedelta

print('today:', datetime.today())
print('same:', datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f"))
print('iso format:', datetime.today().isoformat())
print('utc datetime:', datetime.utcnow())

sub_datetime = datetime.today()
sub_datetime = sub_datetime + timedelta(hours=-2)
print('time with delta -2 hours:', sub_datetime.time())

# todo extend with format doc help
