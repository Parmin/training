from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route("/")
def shell():	
	r = make_response(render_template('index.html'))
	r.headers.set('Access-Control-Allow-Origin', '*')
	return r

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")
