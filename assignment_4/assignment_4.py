from flask import Blueprint, render_template,redirect
import mysql.connector
from flask import request,session, jsonify
import requests
from flask import url_for

assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='JS',
                         template_folder='templates')

@assignment_4.route('/assignment_4')
def assignment_4_func():
        query = 'select * from users'
        users_list = interact_db(query, query_type='fetch')
        return render_template('assignment_4.html', users=users_list)
    # return render_template('assignment_4.html')



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
    print(f'{name} {last_name} {email} {password}')
    # query="INSERT INTO users(name, last_name ,email, password) VALUES ('Blon','higler','alo@gmail.com','1212');"
    query = "INSERT INTO users(name, last_name ,email, password) VALUES ('%s','%s','%s','%s')" % (name,last_name, email,password)
    interact_db(query=query, query_type='commit')
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

        return redirect('/assignment_4')


@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_name = request.form['user_name']
    last_name = request.form['last_name']
    query = "DELETE FROM users WHERE name='%s';" % user_name
    interact_db(query, query_type='commit')
    query = "DELETE FROM users WHERE last_name='%s';" % last_name
    #print(query)
    interact_db(query, query_type='commit')

    return redirect('/assignment_4')

# @assignment_4.route('/Select_user')
# def users():
#     query = 'select * from users'
#     users_list = interact_db(query, query_type='fetch')
#     return render_template('assignment_4.html', users=users_list)




# @assignment_4.route('/assignment4/outer_source')
# def outer_source():
#     return render_template('fetch.html')



# @assignment_4.route('/assignment4/backend')
# def outer_backend():
#     return render_template('fetch.html')


# @assignment_4.route('/assignment4/backend')
# def fetch_be_func():
#     if 'type' in request.args:
#         print(" form")
#         start_time = time.time()
#         num = int(request.args['num'])
#         print(num)
#         rand_start = random.randint(1, 30)
#         rand_end = rand_start + num
#         session['num'] = num
#         pockemons = []
#
#         # # SYNC
#         if request.args['type'] == 'sync':
#             pockemons = get_pockemons_sync(rand_start, rand_end)
#
#
#         end_time = time.time()
#         time_to_finish = f'{end_time - start_time: .2f} seconds'
#         session[f'{request.args["type"]}_time'] = time_to_finish
#         session[f'{request.args["type"]}_num'] = session['num']
#         save_users_to_session(pockemons)
#     else:
#         session.clear()
#
#
#     return render_template('fetch.html')
#
#
# def get_pockemons_sync(from_val, until_val):
#     pockemons = []
#     num = request.args['num']
#     res = requests.get(f': https://reqres.in/api/users/{num}')
#     print(res)
#     pockemons.append(res.json())
#
#     return pockemons
#
# def save_users_to_session(pockemons):
#     users_list_to_save = []
#     for pockemon in pockemons:
#         pockemons_dict = {
#             'sprites': {
#                 'front_default': pockemon['sprites']['front_default']
#             },
#             'first_name': pockemon['name'],
#             # 'height': pockemon['height'],
#             # 'weight': pockemon['weight'],
#         }
#         users_list_to_save.append(pockemons_dict)
#     session['pockemons'] = users_list_to_save
#     print(users_list_to_save)

# def get_user(from_val, until_val):
#     users = []
#     for id in range(from_val, until_val):
#         res = requests.get(f'https://reqres.in/api/users/{id}')
#         print(res)
#         users.append(res.json())
#     return users

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
        # user_dict['sprites'] = {}
        user_dict['sprites'] = user['data']['avatar']
        user_dict['first_name'] = user['data']['first_name']
        user_dict['last_name'] = user['data']['last_name']
        user_dict['email'] = user['data']['email']
        # print(user['data']['first_name'])
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


