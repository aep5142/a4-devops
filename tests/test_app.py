from app.main import app

class FakeCursor:
	def __init__(self, fetch_result=None, rowcount=1):
		self._fetch = fetch_result or []
		self.rowcount = rowcount
		self.executed = []

	def execute(self, sql, params=None):
		self.executed.append((sql, params))

	def fetchall(self):
		return self._fetch

	def close(self):
		pass


class FakeConn:
	def __init__(self, cursor: FakeCursor):
		self._cursor = cursor

	def cursor(self):
		return self._cursor

	def commit(self):
		pass

	def close(self):
		pass


def test_add_missing_param():
	client = app.test_client()
	resp = client.get('/add')
	assert resp.status_code == 400
	assert b'Error: no todo item provided' in resp.data


def test_add_success(monkeypatch):
	# prepare fake cursor that will record executed SQL
	cursor = FakeCursor()

	def fake_connect(**kwargs):
		return FakeConn(cursor)

	monkeypatch.setattr('mysql.connector.connect', fake_connect)

	client = app.test_client()
	resp = client.get('/add?to_add_item=task1')
	assert resp.status_code == 200
	assert b'Added task1 successfully' in resp.data
	assert cursor.executed, "Expected an INSERT to be executed"
	assert 'INSERT INTO todo_table' in cursor.executed[0][0]


def test_delete_missing_param():
	client = app.test_client()
	resp = client.get('/delete')
	assert resp.status_code == 400
	assert b'Error: no todo item provided' in resp.data


def test_delete_not_found(monkeypatch):
	# cursor with rowcount 0 to simulate nothing deleted
	cursor = FakeCursor(rowcount=0)

	def fake_connect(**kwargs):
		return FakeConn(cursor)

	monkeypatch.setattr('mysql.connector.connect', fake_connect)
	client = app.test_client()
	resp = client.get('/delete?to_delete_item=missing')
	assert resp.status_code == 200
	assert b"No record found matching 'missing'" in resp.data


def test_delete_success(monkeypatch):
	cursor = FakeCursor(rowcount=1)

	def fake_connect(**kwargs):
		return FakeConn(cursor)

	monkeypatch.setattr('mysql.connector.connect', fake_connect)
	client = app.test_client()
	resp = client.get('/delete?to_delete_item=task1')
	assert resp.status_code == 200
	assert b'Deleted task1 successfully' in resp.data


def test_view_records(monkeypatch):
	# Simulate two rows in the DB
	cursor = FakeCursor(fetch_result=[(1, 'one'), (2, 'two')])

	def fake_connect(**kwargs):
		return FakeConn(cursor)

	monkeypatch.setattr('mysql.connector.connect', fake_connect)
	client = app.test_client()
	resp = client.get('/view')
	assert resp.status_code == 200
	# response should contain the todo strings
	assert b'one' in resp.data
	assert b'two' in resp.data

