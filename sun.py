import astropy.coordinates as coord
from astropy.time import Time
import astropy.units as u

def alt(mon,day,hour,mins,lat=60.2,lon=25):
    loc = coord.EarthLocation(lon=25 * u.deg, lat=lat * u.deg)
    times = f'2022-{mon}-{day}T{hour}:{mins}:00'
    now  = Time(times, format='isot', scale='utc')
    altaz = coord.AltAz(location=loc, obstime=now)
    sun = coord.get_sun(now).transform_to(altaz).alt
    return sun.degree

