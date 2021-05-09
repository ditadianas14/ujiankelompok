from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import mysql.connector
import random, datetime, time

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'DitaDianaSari14'
app.config['MYSQL_DB'] = 'ac'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")


#LOGIN ADMIN
@app.route('/loginadmin', methods=["GET", "POST"])
def loginadmin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM admin WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['admin'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("loginadmin.html")
#AKHIRLOGIN ADMIN

# LOGIN USERS
@app.route('/loginusers', methods=["GET", "POST"])
def loginusers():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['user'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("loginusers.html")
    # AKHIR LOGIN USERS


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")

#REGISTER USERS

@app.route('/register', methods=["GET", "POST"])
def registerusers():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                    (name, email, hash_password,))
        mysql.connection.commit()
        session['user'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

#AKHIR REGISTER USERS

#REGISTER ADMIN

@app.route('/daftar', methods=["GET", "POST"])
def daftar():
    if request.method == 'GET':
        return render_template("daftar.html")    
    else:
        if  request.form['otp'] != 'kelompokdua':
            return render_template("daftar.html")
        else:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            otp = request.form['otp'].encode('utf-8')
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
            hash_otp = bcrypt.hashpw(otp, bcrypt.gensalt())
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO admin (name, email, password, otp) VALUES (%s,%s,%s,%s)",
                        (name, email, hash_password, hash_otp))
            mysql.connection.commit()
            session['admin'] = request.form['name']
            session['email'] = request.form['email']
            return redirect(url_for('home'))

#AKHIR REGISTER ADMIN



#MONITOR AC FOR ADMIN

@app.route('/monitorac')
def monitorac():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *  FROM monitoring_ac ORDER BY datetime DESC LIMIT 10")
    rv = cur.fetchall()
    cur.close()
    return render_template('monitorac.html', monitoring_ac=rv)

@app.route('/refreshdataac', methods=["GET", "POST"])
def refreshdataac():
     
        #ini kodingan masukin data
         for i in range(10):
          
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            in_con = random.randint(55,65)
            out_con = in_con - 13
            in_evp = random.randint(55,65)
            out_evp = in_evp + 30
            comp = random.randint (50,90)
            room = random.randint (27,35)
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO monitoring_ac (datetime, in_conden, out_conden, in_evapor, out_evapor, compressor, ambient) VALUES (%s, %s, %s, %s, %s, %s, %s)", (date_time, in_con, out_con, in_evp, out_evp, comp, room))
            mysql.connection.commit()
            return redirect(url_for('monitorac'))


@app.route('/hapusdataac/<string:id_data>', methods=["GET"])
def hapusdataac(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM monitoring_ac WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('monitorac'))

#AKHIR MONITOR AC
            

#MONITOR AC FOR USERS
@app.route('/monitorac_users')
def monitorac_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *  FROM monitoring_ac ORDER BY datetime DESC LIMIT 10")
    rv = cur.fetchall()
    cur.close()
    return render_template('monitorac_users.html', monitoring_ac=rv)

@app.route('/refreshdataac_users', methods=["GET", "POST"])
def refreshdataac_users():
     
        #ini kodingan masukin data
         for i in range(10):
          
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            in_con = random.randint(55,65)
            out_con = in_con - 13
            in_evp = random.randint(55,65)
            out_evp = in_evp + 30
            comp = random.randint (50,90)
            room = random.randint (27,35)
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO monitoring_ac (datetime, in_conden, out_conden, in_evapor, out_evapor, compressor, ambient) VALUES (%s, %s, %s, %s, %s, %s, %s)", (date_time, in_con, out_con, in_evp, out_evp, comp, room))
            mysql.connection.commit()
            return redirect(url_for('monitorac_users'))
   #AKHIR MONITOR AC FOR USERS 

#MONITOR AC USERS2

@app.route('/monitorac_users2')
def monitorac_users2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *  FROM monitoring_ac ORDER BY datetime DESC LIMIT 10")
    rv = cur.fetchall()
    cur.close()
    return render_template('monitorac_users2.html', monitoring_ac=rv)

#AKHIR MONITOR AC USERS 2


#MONITOR AC FOR ADMIN 2
@app.route('/monitorac_admin2')
def monitorac_admin2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *  FROM monitoring_ac ORDER BY datetime DESC LIMIT 10")
    rv = cur.fetchall()
    cur.close()
    return render_template('monitorac_admin2.html', monitoring_ac=rv)

@app.route('/insertdataac2', methods=["GET", "POST"])
def inserthdataac2():
     
        #ini kodingan masukin data
         for i in range(10):
          
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            in_con = random.randint(55,65)
            out_con = in_con - 13
            in_evp = random.randint(55,65)
            out_evp = in_evp + 30
            comp = random.randint (50,90)
            room = random.randint (27,35)
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO monitoring_ac (datetime, in_conden, out_conden, in_evapor, out_evapor, compressor, ambient) VALUES (%s, %s, %s, %s, %s, %s, %s)", (date_time, in_con, out_con, in_evp, out_evp, comp, room))
            mysql.connection.commit()
            return redirect(url_for('monitorac_admin2'))


@app.route('/delete2/<string:id_data>', methods=["GET"])
def delete2(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM monitoring_ac WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('monitorac_admin2'))

#AKHIR MONITOR AC ADMIN 2

@app.route('/about')
def about():
    return render_template('about.html')  # render a template


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(host='0.0.0.0', debug=True)