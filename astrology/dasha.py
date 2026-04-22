import swisseph as swe
from datetime import datetime, timedelta

NAKSHATRA_SIZE = 13.3333333333

DASHA_SEQUENCE = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17),
]

def get_moon_longitude(jd):
    return swe.calc_ut(jd, swe.MOON)[0][0]

def get_nakshatra(moon_long):
    return int(moon_long / NAKSHATRA_SIZE)

def calculate_vimshottari_dasha(dob, tob):
    dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour)

    moon_long = get_moon_longitude(jd)
    nakshatra_index = get_nakshatra(moon_long)

    dasha_index = nakshatra_index % 9
    start_planet, years = DASHA_SEQUENCE[dasha_index]

    dasha_list = []
    current_date = dt

    for planet, years in DASHA_SEQUENCE[dasha_index:] + DASHA_SEQUENCE[:dasha_index]:
        end_date = current_date + timedelta(days=years * 365)
        dasha_list.append({
            "planet": planet,
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        })
        current_date = end_date

    return dasha_list