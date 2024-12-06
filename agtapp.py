from flask import Flask, render_template, request, redirect, url_for
import oracledb

app = Flask(__name__)

# Database connection details
def get_db_connection():
    return oracledb.connect(
        user='ADMIN', 
        password='vUcW96AC.gd.d4y', 
        dsn='a1z2qbbh602iu73y_medium', 
        config_dir="C:\\ChukProj\\config_dir",
        wallet_location="C:\\ChukProj\\config_dir", 
        wallet_password='gHpt468/Chuk.VGA.Lli.ps'
    )

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM AGT_CHILDREN_DATA_RECORDS")
    names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', names=names)

@app.route('/update', methods=['POST'])
def update_record():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    dob = request.form['dob']
    tag_number = request.form['tag_number']
    attendance = request.form['attendance']
    date_of_entry = request.form['date_of_entry']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE AGT_CHILDREN_DATA_RECORDS
        SET AGE = :age, GENDER = :gender, DATE_OF_BIRTH = :dob, TAG_NUMBER = :tag_number,
            ATTENDANCE = :attendance, DATE_OF_ENTRY = :date_of_entry
        WHERE FIRST_NAME = :first_name AND LAST_NAME = :last_name
    """, {
        'age': age,
        'gender': gender,
        'dob': dob,
        'tag_number': tag_number,
        'attendance': attendance,
        'date_of_entry': date_of_entry,
        'first_name': first_name,
        'last_name': last_name
    })
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_record():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    dob = request.form['dob']
    tag_number = request.form['tag_number']
    attendance = request.form['attendance']
    date_of_entry = request.form['date_of_entry']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO AGT_CHILDREN_DATA_RECORDS (FIRST_NAME, LAST_NAME, AGE, GENDER, DATE_OF_BIRTH, TAG_NUMBER, ATTENDANCE, DATE_OF_ENTRY)
        VALUES (:first_name, :last_name, :age, :gender, :dob, :tag_number, :attendance, :date_of_entry)
    """, {
        'first_name': first_name,
        'last_name': last_name,
        'age': age,
        'gender': gender,
        'dob': dob,
        'tag_number': tag_number,
        'attendance': attendance,
        'date_of_entry': date_of_entry
    })
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
