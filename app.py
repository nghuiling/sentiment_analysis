from flask import Flask,url_for,render_template,request
# import nltk
# from nltk.tokenize import word_tokenize
import stanza
# import random
import json
from waitress import serve



# import pickle
# f = open('sent_model.pickle', 'rb')
# classifier = pickle.load(f)
# f.close()

nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')


HTML_WRAPPER = """<div style="overflow-x: auto">{}\n</div>"""

from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)



@app.route('/', methods=['GET','POST'])
def home():	
	return render_template('index.html')


@app.route('/extract',methods=['GET','POST'])
def extract():


	raw_text = request.form['rawtext']
	doc = nlp(raw_text)
	moods={0:'<b> Negative &#128533</b>', 1:'<b>Neutral &#128528</b>'
	, 2:'<b>Positive &#128522</b>'}
	a =[]

	for i, sentence in enumerate(doc.sentences):
		a.append('Sentence {} is {} <br>'.format(i+1,moods[sentence.sentiment]))
		result = HTML_WRAPPER.format(a)

	return render_template('result.html',rawtext=raw_text,result=result)



if __name__ == '__main__':
   # app.run(debug=True)
   serve(app, host='0.0.0.0', port=8000)