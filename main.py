import os
# import urllib

import requests
from flask import Flask, send_file, Response, redirect
from bs4 import BeautifulSoup

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>Python 230: Lesson 5</head>
<body>
    <h1>Pig Latin Translation Mashup:</h1>
    <p>
    <span>
    Click this button for the mashup:</span>
    <form> 
    <button type="submit" formaction="{}">Click Me</button>
    </form>
    <span> </span>
    </p>
</body>
</html>
"""

def get_fact():
	""" Obtains/returns random information from unkno.com"""
	response = requests.get("http://unkno.com")
	soup = BeautifulSoup(response.content, "html.parser")
	facts = soup.find_all("div", id="content")
	
	return facts[0].getText()

@app.route('/')
def home():
	""" 
	Obtains the text from unkno to inject into the Pig Latin translator
	Returns a landing page with a button to redirect to the translation.
	"""
	random_fact = get_fact()
	make_request = requests.post("http://hidden-journey-62459.herokuapp.com/piglatinize/", 
		allow_redirects=False, data={'input_text': random_fact})
	display = template.format(make_request.headers['location'], make_request.headers['location'])

	return display


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 6787))
	app.run(host='0.0.0.0', port=port)

