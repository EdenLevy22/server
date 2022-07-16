from flask import Blueprint, render_template,redirect
import mysql.connector
from flask import request,session, jsonify
import requests


assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='JS',
                         template_folder='templates')

@assignment_4.route('/assignment_4')
def assignment_4_func():
        users_list = get_all_users()
        return render_template('assignment_4.html', users=users_list)



def get_all_users():
    query = 'select * from users'
    list_of_users = interact_db(query, query_type='fetch')
    return(list_of_users)


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='schema_homework4')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

@assignment_4.route('/insert_user' , methods=['POST'])
def insert_user():
    name = request.form['user_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    query = "INSERT INTO users(name, last_name ,email, password) VALUES ('%s','%s','%s','%s')" % (name,last_name, email,password)
    interact_db(query=query, query_type='commit')
    users = get_all_users()
    message = 'a new user added successfully'
    return render_template('assignment_4.html', users=users, message=message)

    return redirect('/assignment_4')

@assignment_4.route('/update_user', methods=['POST'])
def update_user_func():
        name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        query = "UPDATE users SET email = '%s' WHERE name='%s';" % (email, name)
        interact_db(query, query_type='commit')
        query = "UPDATE users SET password ='%s' WHERE name='%s';" % (password, name)
        interact_db(query, query_type='commit')
        users=get_all_users()
        message='users list was update successfully'
        return render_template('assignment_4.html',users=users,message=message)


@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_name = request.form['user_name']
    last_name = request.form['last_name']
    query = "DELETE FROM users WHERE name='%s';" % user_name
    interact_db(query, query_type='commit')
    query = "DELETE FROM users WHERE last_name='%s';" % last_name
    interact_db(query, query_type='commit')
    users = get_all_users()
    message = 'one user deleted from users list'
    return render_template('assignment_4.html', users=users, message=message)


@assignment_4.route('/assignment4/users')
def get_users():
        query = f'select * from users'
        users_list = interact_db(query, query_type='fetch')
        return_list = []
        for user in users_list:
            user_dict = {
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
            }
            return_list.append(user_dict)
        return jsonify(return_list)

def get_users_sync(from_val):
    pockemons = []
    res = requests.get(f'https://reqres.in/api/users/{from_val}')
    pockemons.append(res.json())
    print(pockemons)
    return pockemons


def save_users_to_session(pockemons):
    users_list_to_save = []
    for user in pockemons:
        user_dict = {}
        user_dict['sprites'] = user['data']['avatar']
        user_dict['first_name'] = user['data']['first_name']
        user_dict['last_name'] = user['data']['last_name']
        user_dict['email'] = user['data']['email']
        users_list_to_save.append(user_dict)
    session['pockemons'] = users_list_to_save


@assignment_4.route('/assignment4/backend')
def fetch_be_func():
    if 'type' in request.args:
        print('type')
        num = int(request.args['num'])
        session['num'] = num
        pockemons = []

        if request.args['type'] == 'sync':
            pockemons = get_users_sync(num)
        save_users_to_session(pockemons)
        return render_template('fetch.html')

    else:
        session.clear()
        return render_template('fetch.html')

@assignment_4.route('/assignment4/restapi_users', defaults={'USER_ID': 1})
@assignment_4.route('/assignment4/restapi_users/<int:USER_ID>')
def get_user_by_ID(USER_ID):
    query = f'select * from users where id ={USER_ID}'
    users_list = interact_db(query, query_type='fetch')

    if len(users_list) == 0:
        return_dict = {
            'message': 'user not found'
        }
    else:
        user_list=users_list[0]
        return_dict = {
            'name': user_list.name,
            'last_name': user_list.last_name,
            'email': user_list.email
    }
    return jsonify(return_dict)


