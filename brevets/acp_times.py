"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import math
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#
OPEN_SPEEDS = [(200, 34), (400, 32), (600, 30), (1000, 28), (1300, 26)]
CLOSE_SPEEDS = [(200, 15), (400, 15), (600, 15), (1000, 11.428), (1300, 13.333)]
FINISH_TIMES = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}

def calc_segment_time(distance, speed_table):
   hours = 0
   prev_limit = 0
   for limit, speed in speed_table:
      if distance <= prev_limit:
         break
      hours += (min(distance, limit) - prev_limit) / speed
      prev_limit = limit
   return hours
def _round_minutes(hours):
    return math.floor(hours * 60 + 0.5)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    control_dist_km = min(control_dist_km, brevet_dist_km)
    start = arrow.get(brevet_start_time)
    minutes = _round_minutes(calc_segment_time(control_dist_km, OPEN_SPEEDS))
    return start.shift(minutes=minutes).isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    start = arrow.get(brevet_start_time)
    if control_dist_km == 0:
        return start.shift(hours=1).isoformat()
    control_dist_km = min(control_dist_km, brevet_dist_km)
    if control_dist_km == brevet_dist_km:
        hours = FINISH_TIMES[brevet_dist_km]
    elif control_dist_km < 60:
         hours = control_dist_km / 20 + 1
    else:
         hours = calc_segment_time(control_dist_km, CLOSE_SPEEDS)
    return start.shift(minutes=_round_minutes(hours)).isoformat()
