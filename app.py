from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Replace with your Azure SQL Database connection string
conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=gfgc.database.windows.net;DATABASE=gfgc;UID=adminusr;PWD=Wqerty@!gfgc'

class AdmissionForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    fathername = StringField('Father\'s Name', validators=[validators.DataRequired()])
    school_name = StringField('School Name', validators=[validators.DataRequired()])
    college_name = StringField('College Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Submit Admission')

def connect_to_database():
    """Establishes a connection to the Azure SQL database."""
    try:
        conn = pyodbc.connect(conn_string)
        return conn
    except pyodbc.Error as ex:
        print("Connection string error:", ex)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AdmissionForm()
    if form.validate_on_submit():
        name = form.name.data
        fathername = form.fathername.data
        school_name = form.school_name.data
        college_name = form.college_name.data
        email = form.email.data

        conn = None  # Initialize conn to None to handle scope issues

        try:
            # Attempt to create a database connection
            conn = connect_to_database()
            if conn is None:
                return "An error occurred while establishing a database connection."

            cursor = conn.cursor()

            # Perform your database operations here
            # Example: Inserting the form data into the database
            insert_query = """
            INSERT INTO Admissions (name, fathername, school_name, college_name, email)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (name, fathername, school_name, college_name, email))
            conn.commit()  # Commit the transaction

        except pyodbc.Error as ex:
            print("Database error:", ex)
            # Handle database errors gracefully
            return "An error occurred while processing your request."

        finally:
            if conn:
                conn.close()  # Close the connection

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
