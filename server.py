from flask import Flask
from DJbamboo import DJbamboo, comeondata
from util import dic_to_str
app = Flask(__name__)

@app.route('/test/<val>')
def test(val):
    d = DJbamboo(val)
    return dic_to_str(d)

if __name__ == '__main__':
	comeondata()
	app.run()