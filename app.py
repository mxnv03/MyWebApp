import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="postgres", user="postgres", password='postgres', host="localhost", port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                           (str(username.title()), str(password)))
            records = list(cursor.fetchall())
            if username == '' and password == '':
                return render_template('error.html', text='Put your login and password!')
            elif password == '':
                return render_template('error.html', text='Put your password!')
            elif username == '':
                return render_template('error.html', text='Put your login!')
            elif len(records) != 0:
                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
            elif len(records) == 0:
                print(records)
                return render_template('error.html', text='You are not in data base, but you can create a new account')
        elif request.form.get("registration"):
                return redirect("/registration/")
        elif request.form.get("delete"):
                return redirect("/delete/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        login = request.form.get('login')
        full = str(name) + ' ' + surname
        password = request.form.get('password')
        st_list = [name, surname, login, password]
        txt_list = ['name', 'surname', 'username', 'password']
        if name != '' and surname != '' and login != '' and password != '':
            cursor.execute("SELECT * FROM service.users WHERE login=%s",
                           (str(login),))
            gg = list(cursor.fetchall())
            if len(gg) == 0:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(full.title()), str(login), str(password)))
                conn.commit()
                return redirect('/login/')
            else:
                return render_template('error.html', text='User already exists, try to put another username')
        else:
            text = []
            for i in range(len(st_list)):
                if st_list[i] == '':
                    text.append(txt_list[i])
            text = ', '.join(text)
            return render_template('error.html', text=f'Put your {text}')
        return redirect('/login/')
    return render_template('registration.html')

@app.route('/delete/', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' and password == '':
            return render_template('error.html', text='Put your login and password!')
        elif password == '':
            return render_template('error.html', text='Put your password!')
        elif username == '':
            return render_template('error.html', text='Put your login!')
        else:
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                           (str(username), str(password)))
            tr = list(cursor.fetchall())
            if len(tr) != 0:
                cursor.execute("DELETE FROM service.users WHERE login=%s",
                               (str(username),))
                conn.commit()
                return redirect('/login/')
            else:
                return render_template('error.html', text='No users')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
