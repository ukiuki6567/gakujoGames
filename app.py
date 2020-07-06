import pathlib
from flask import *
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
bootstrap = Bootstrap(app)

def importData(fileName):
	return [line.rstrip() for line in open(fileName)]

def exportData(listName, fileName):
	concatList = '\n'.join(listName)
	with open(fileName, 'w') as f:
		f.write(concatList)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dice')
def dice():
	users = importData('users.txt')
	talks = importData('talks.txt')
	return render_template('dice.html', users=users, talks=talks)

@app.route('/order')
def order():
	users = importData('users.txt')
	random.shuffle(users)
	return render_template('order.html', users=users)

@app.route('/settings')
def settings():
	return render_template('settings_menu.html')

@app.route('/nameList', methods=["GET", "POST"])
def nameSettings():
	users = importData('users.txt')
	if request.method == "GET":
		return render_template('nameSettings.html', users=users)

	if request.form["command"] == 'del':
		users.remove(request.form["userName"])
		exportData(users, 'users.txt')
	elif request.form["command"] == 'add':
		users.append(request.form["userName"])
		exportData(users, 'users.txt')

	return redirect('/nameList')


@app.route('/talkList', methods=["GET", "POST"])
def talkSettings():
	talks = importData('talks.txt')
	if request.method == "GET":
		return render_template('talkSettings.html', talks=talks)

	if request.form["command"] == 'del':
		talks.remove(request.form["theme"])
		exportData(talks, 'talks.txt')
	elif request.form["command"] == 'add':
		talks.append(request.form["theme"])
		exportData(talks, 'talks.txt')

	return redirect('/talkList')



if __name__ == "__main__":
	userFile = pathlib.Path('users.txt')
	talkFile = pathlib.Path('talks.txt')
	if not userFile.exists():
		userFile.touch()
	if not talkFile.exists():
		talkFile.touch()

	app.run(debug=True)