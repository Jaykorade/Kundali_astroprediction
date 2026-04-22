import swisseph as swe
from datetime import datetime

swe.set_ephe_path('.')

def generate_kundali(dob, tob, lat, lon):
    dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")

    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour)

    planets = {
        "Sun": swe.calc_ut(jd, swe.SUN)[0][0],
        "Moon": swe.calc_ut(jd, swe.MOON)[0][0],
        "Mars": swe.calc_ut(jd, swe.MARS)[0][0],
        "Mercury": swe.calc_ut(jd, swe.MERCURY)[0][0],
        "Jupiter": swe.calc_ut(jd, swe.JUPITER)[0][0],
        "Venus": swe.calc_ut(jd, swe.VENUS)[0][0],
        "Saturn": swe.calc_ut(jd, swe.SATURN)[0][0],
    }

    houses = swe.houses(jd, lat, lon)[0]

    return {
        "planets": planets,
        "houses": houses.tolist()
    }