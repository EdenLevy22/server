from flask import Flask, redirect,jsonify
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from datetime import timedelta


app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

@app.route('/Contact')
def Contact_func():
    return render_template('Contact.html')

@app.route('/Home Page')
def HomePage_func():
    return render_template('Home Page.html')

@app.route('/assignment3_1')
def assignment3_1_func():
    want_a_dog = True
    user_name = 'eden'
    dogs_names = {'name': 'Lieo',  'nickname': 'Lilo', 'age': '2 years '}
    dogs_types = ['Labrador', 'Bulldog', 'German Shepherd', 'Golden Retriever', 'Poodle', 'Rottweiler', 'Beagle']
    return render_template('assignment3_1.html', want_a_dog=want_a_dog , user_name= user_name , dogs_names=dogs_names, dogs_types =dogs_types )

@app.route('/')
def default():
    name = ""
    if name == "":
        return redirect("/Home Page")
    else:
        return redirect(url_for('assignment3_1_func'))

users=[{'name': 'Yossi', 'last_name': 'Bar','email': 'yo@gmail.com' , 'password': '1234'},
       {'name': 'Eden', 'last_name': ' Levy','email': 'ed@gmail.com' , 'password': '456'},
       {'name': 'Dany', 'last_name': ' Cohen', 'email': 'dan@gmail.com', 'password': '678'},
       {'name': 'Aviv', 'last_name': ' Hayun', 'email': 'aviv@gmail.com', 'password': '890'},
       {'name': 'Gal', 'last_name': ' Swisa', 'email': 'gal@gmail.com', 'password': '1020'} ]


@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2_func():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
        user=next((item for item in users if item['name'] == user_name), None)

        if request.args['user_name'] == "":
            return render_template('assignment3_2.html',
                                   users=users)
        if user in users:
           return render_template('assignment3_2.html',
                                   user_name=user_name,
                                   user=user)
        else:
            return render_template('assignment3_2.html',
                                    message='user not found')

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = next((item for item in users if item['name'] == user_name), None)
        if user in users:
            user_password = user['password']
            if user_password == password:
                session['user_name'] = user_name
                session['logedin'] = True
                return render_template('assignment3_2.html',
                                       message2='Success Logged-in, ' + user_name,
                                       username=user_name)
            else:
                return render_template('assignment3_2.html',
                                       message2='Wrong password!')
        else:
            return render_template('assignment3_2.html',
                                    message2='The user dose not exist, Please sign in!')
    return render_template('assignment3_2.html')

@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('assignment3_2_func'))

if __name__ == '__main__':
    app.run(debug=True)


from assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)


