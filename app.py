from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template

app = Flask(__name__)

@app.route('/Contact')
def Contact_func():
    return render_template('Contact.html')

@app.route('/Home Page')
def HomePage_func():  # put application's code here
    return render_template('Home Page.html')

@app.route('/assignment3_1')
def assignment3_1_func():  # put application's code here
    return render_template('assignment3_1.html')

@app.route('/<name>')
def Page(name):
    if name == 'Contact':
        return redirect(url_for('Contact_func'))
    if name == 'Home Page':
        return redirect(url_for('HomePage_func'))

if __name__ == '__main__':
    app.run(debug=True)
