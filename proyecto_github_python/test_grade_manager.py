import os
from grade_manager import add_student, add_grade, average, DATA_FILE
def setup_function():
if os.path.exists(DATA_FILE):
os.remove(DATA_FILE)
def teardown_function():
if os.path.exists(DATA_FILE):
os.remove(DATA_FILE)
def test_add_student_and_average():
sid = add_student(&quot;Ana Perez&quot;)
assert isinstance(sid, str)
assert add_grade(sid, 8.5) is True
assert add_grade(sid, 9.0) is True
avg = average(sid)
assert abs(avg - 8.75) &lt; 1e-6
