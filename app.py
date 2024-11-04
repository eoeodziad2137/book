from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key ='secretkey'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mam10lat v'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)


@app.route('/')
def home():
    if  'username' in session:
        return render_template('home.html ', username=session['username'])
    else:
        return render_template('home.html')

    
#@app.route('/')
#def home():
 #   if  'username' in session:
  #      return render_template('profile.html ', username=session['username'])
   # else:
     #   return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from users where username = '{username}'")
        user = cur.fetchone()
        cur.close()
        
        if user and password == user[1]:    
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()

        cur.execute(f"insert into users (username, password) values ('{username}', '{password}')")
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')
        


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)