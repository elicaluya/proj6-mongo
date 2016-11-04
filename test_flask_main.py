import flask_main.py

now = arrow.utcnow()

def test_time():
	assert humanize_arrow_date(now.replace(days=+1)) == "Tomorrow"
	
def test_time2():
	assert humanize_arrow_date(now.replace(days=+2)) == "in 2 days"
	