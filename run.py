from mycode import app, database
from mycode.models import Entry, FTSEntry, User


def main():
	database.create_tables([User, Entry, FTSEntry])
	app.run(debug=True)

if __name__ == '__main__':
	# app.run(debug=True)
	main()