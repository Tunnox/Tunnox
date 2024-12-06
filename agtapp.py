from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import oracledb
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    return oracledb.connect(
        user='ADMIN', 
        password='vUcW96AC.gd.d4y', 
        dsn='a1z2qbbh602iu73y_medium', 
        config_dir="C:\\ChukProj\\config_dir",
        wallet_location="C:\\ChukProj\\config_dir", 
        wallet_password='gHpt468/Chuk.VGA.Lli.ps'
    )

# Initialize DataFrames
attendance_df = pd.DataFrame(columns=['FIRST_NAME', 'ATTENDANCE'])
data_df = pd.DataFrame(columns=['FIRST_NAME', 'LAST_NAME', 'AGE', 'GENDER', 'DATE_OF_BIRTH', 'DATE_OF_ENTRY'])

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM AGT_CHILDREN_DATA_RECORDS")
    names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', names=names)

@app.route('/take_attendance', methods=['POST'])
def take_attendance():
    first_name = request.form['first_name']
    attendance = request.form['attendance']
    attendance_df.loc[len(attendance_df)] = [first_name, attendance]
    return redirect(url_for('index'))

@app.route('/add_data', methods=['POST'])
def add_data():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    dob = request.form['dob']
    date_of_entry = request.form['date_of_entry']
    data_df.loc[len(data_df)] = [first_name, last_name, age, gender, dob, date_of_entry]
    return redirect(url_for('index'))

@app.route('/download_attendance', methods=['POST'])
def download_attendance():
    download_path = request.form['download_path']
    attendance_df.to_excel(download_path + '/attendance.xlsx', index=False)
    return send_file(download_path + '/attendance.xlsx', as_attachment=True)

@app.route('/download_data', methods=['POST'])
def download_data():
    download_path = request.form['download_path']
    data_df.to_excel(download_path + '/data_records.xlsx', index=False)
    return send_file(download_path + '/data_records.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
