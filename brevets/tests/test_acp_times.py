import acp_times

START = "2017-01-01T00:00:00"

def test_start_control():
    assert acp_times.open_time(0, 200, START) == "2017-01-01T00:00:00+00:00"
    assert acp_times.close_time(0, 200, START) == "2017-01-01T01:00:00+00:00"

def test_single_segment_100km():
    assert acp_times.open_time(100, 200, START) == "2017-01-01T02:56:00+00:00"
    assert acp_times.close_time(100, 200, START) == "2017-01-01T06:40:00+00:00"

def test_multi_segment_550km():
    assert acp_times.open_time(550, 600, START) == "2017-01-01T17:08:00+00:00"
    assert acp_times.close_time(550, 600, START) == "2017-01-02T12:40:00+00:00"

def test_french_rule_50km():
    assert acp_times.open_time(50, 200, START) == "2017-01-01T01:28:00+00:00"
    assert acp_times.close_time(50, 200, START) == "2017-01-01T03:30:00+00:00"

def test_control_slightly_beyond_brevet():
    assert acp_times.open_time(205, 200, START) == "2017-01-01T05:53:00+00:00"
    assert acp_times.close_time(205, 200, START) == "2017-01-01T13:30:00+00:00"

def test_segment_boundary_200km():
    assert acp_times.open_time(200, 300, START) == "2017-01-01T05:53:00+00:00"
    assert acp_times.close_time(200, 300, START) == "2017-01-01T13:20:00+00:00"