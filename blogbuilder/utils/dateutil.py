import logging

import pendulum


def get_time_now():  # type: () -> pendulum.DateTime
    return pendulum.now()


def end_time(start: pendulum.DateTime):
    end = pendulum.now()


def get_datetime(datetime, date=True, time=True):
    if isinstance(datetime, str):
        datetime = parse2date(datetime, strict=False)
    if date and not time:
        return datetime.to_date_string()
    if not date and time:
        return datetime.to_time_string()
    return datetime.to_datetime_string()


def get_date_part(datetime):
    dt = datetime
    is_bc = False
    if isinstance(datetime, str):
        # only for year(/month/day), year(-month-day), and year, month, day are all digits
        if datetime.startswith("-"):
            is_bc = True
            datetime = datetime[1:]

        split_tag = "/" if "/" in datetime else "-"
        parts = datetime.split(split_tag)
        parts = parts + ["01", "01"][:3 - len(parts)]
        if all([p.isdigit() for p in parts]):
            datetime = "{:04d}-{:02d}-{:02d}".format(int(parts[0]), int(parts[1]), int(parts[2]))
        try:
            dt = parse2date(datetime, strict=True)
        except:
            logging.warning(f"datetime=`{datetime}` may not valid")
            dt = parse2date(datetime, strict=False)
    return ("{}{:04d}".format("-" if is_bc else "", int(dt.year)),
            "{:02d}".format(int(dt.month)),
            "{:02d}".format(int(dt.day)))


def get_deltatime(start, end):
    return (end - start).as_timedelta()


def parse2date(datetime, strict=True):  # type: (str, bool) -> pendulum.DateTime
    return pendulum.parse(datetime, strict=strict)
