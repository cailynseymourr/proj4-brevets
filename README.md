# ACP Brevet Time Calculator
 
A Flask + Ajax reimplementation of the RUSA ACP controle time calculator
(https://rusa.org/octime_acp.html). Enter a control distance and the open and
close times fill in automatically.
 
**Author:** Cailyn Seymour
**Email:** cailyn@uoregon.edu
**Course:** CIS 322, University of Oregon
 
Based on the starter code by Michal Young.
 
## Using the calculator
 
1. Pick the brevet distance (200, 300, 400, 600, or 1000 km).
2. Set the brevet start date and time.
3. Enter a control distance in either the **Miles** or **Km** box. The other box
   fills in, and the **Open** and **Close** times appear for that row.
Changing the brevet distance or start time does not update rows that are already
filled in. Re-enter the km value in those rows to recalculate.
 
## Running it
 
With Docker:
 
```
docker build -t brevets .
docker run -p 5000:5000 brevets
```
 
Then open http://localhost:5000.
 
Without Docker (from the `brevets` directory, Python 3 with `flask` and `arrow`
installed):
 
```
python flask_brevets.py
```
 
## Running the tests
 
From the `brevets` directory:
 
```
nosetests
```
 
(`nose2` or `pytest` also work if `nosetests` does not run on your Python version.)
 
The tests are in `tests/test_acp_times.py` and cover the start control, a
single-segment control, a multi-segment control, the first-60-km rule, a control
slightly beyond the brevet distance, and a control on a segment boundary.
 
## Rules implemented
 
The calculation lives in `acp_times.py` as `open_time(control_dist_km,
brevet_dist_km, brevet_start_time)` and `close_time(...)`. Both return ISO 8601
strings in the same time zone as the start time. The rules below follow
https://rusa.org/pages/acp-brevet-control-times-calculator. Where that page is
ambiguous, the choice made here is stated.
 
### Speed table
 
| Control location (km) | Minimum speed (km/h) | Maximum speed (km/h) |
|---|---|---|
| 0 - 200 | 15 | 34 |
| 200 - 400 | 15 | 32 |
| 400 - 600 | 15 | 30 |
| 600 - 1000 | 11.428 | 28 |
| 1000 - 1300 | 13.333 | 26 |
 
### Open time
 
The open time is the sum, over each segment of the table up to the control, of
(distance in that segment / maximum speed). For example, a control at 550 km is
200/34 + 200/32 + 150/30 = 17.1324 hours, which is 17:08 after the start.
 
### Close time
 
The close time is computed the same way using the minimum speeds. For example,
550 km is 200/15 + 200/15 + 150/15 = 36.667 hours, which is 36:40 after the
start.
 
### Clarifications
 
- **Rounding.** Times are converted to minutes and rounded to the nearest minute,
  with exact halves rounded up. Seconds are always zero.
- **Start control (0 km).** Opens at the start time and closes 1 hour after the
  start.
- **First 60 km (French rule).** For a control closer than 60 km, the close time
  is (distance / 20) + 1 hour instead of distance / 15. For example, a control at
  50 km closes 3:30 after the start. The open time is unaffected.
- **Final control.** A control at or beyond the brevet distance uses the brevet
  distance for its calculation. Its open time comes from the normal formula
  (e.g. 200 km opens at 5:53). Its close time is the official brevet limit, not
  the formula:
  | Brevet (km) | Final control closes after |
  |---|---|
  | 200 | 13:30 |
  | 300 | 20:00 |
  | 400 | 27:00 |
  | 600 | 40:00 |
  | 1000 | 75:00 |
- **Controls beyond the brevet distance.** RUSA allows the final control to be up
  to 20% past the nominal distance. A control past the brevet distance is treated
  as being at the brevet distance, so 205 km on a 200 km brevet gives the same
  times as 200 km (open 5:53, close 13:30).
- **Segment boundaries.** A control exactly on a boundary (200, 400, 600, 1000 km)
  uses the speeds of the segment that ends there; no distance falls into the next
  segment.
## Files
 
- `acp_times.py` - open and close time calculations
- `flask_brevets.py` - Flask app and the `/_calc_times` Ajax endpoint
- `templates/calc.html` - the page and its JavaScript
- `tests/test_acp_times.py` - automated tests
- `Dockerfile` - container build
 