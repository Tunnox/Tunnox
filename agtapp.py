from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the Excel file into a DataFrame
def load_data():
    return pd.read_excel(r"C:\ChukProj\flask_proj\AGT_Attendacne_Register.xlsx")

# Save the DataFrame back to Excel
def save_data(df):
    df.to_excel(r"C:\ChukProj\flask_proj\AGT_Attendacne_Register.xlsx", index=False)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == "AGT" and password == "agtchildren":
        session['logged_in'] = True
        return redirect(url_for('attendance'))
    return "Invalid credentials, please try again."


@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    df = load_data()
    names = df[['First Name', 'Last Name']].values.tolist()

    if request.method == 'POST':
        selected_name = request.form['name']
        if selected_name:
            row = df[df['First Name'] == selected_name].iloc[0]
            # Update the DataFrame with new data
            df.loc[df['First Name'] == selected_name, 'Age'] = request.form['age']
            df.loc[df['First Name'] == selected_name, 'Gender'] = request.form['gender']
            df.loc[df['First Name'] == selected_name, 'Tag Number'] = request.form['tag number']
            df.loc[df['First Name'] == selected_name, 'Attendance'] = request.form['attendance']
            df.loc[df['First Name'] == selected_name, 'Time'] = request.form['time']
            save_data(df)

        # Send email functionality
        if 'send_email' in request.form:
            send_email(df)

    return render_template('attendance.html', names=names)

def send_email(df):
    msg = MIMEText(df.to_html())
    msg['Subject'] = 'Attendance Data'
    msg['From'] = 'realgeoemy@gmail.com'
    msg['To'] = 'chukwuemekaumunna@gmail.com'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('realgeoemy@gmail.com', 'Oluwaseun1')
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
    
