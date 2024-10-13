from flask import Flask, render_template, url_for, request, session, g, abort, flash
from model import User, db  # Ensure the `db` object is also imported from your model.py

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creola.db'  # Database URI (SQLite in this case)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True  # Enable query recording

# Initialize the SQLAlchemy database object
db.init_app(app)  # Ensure that SQLAlchemy is initialized with your Flask app

# Create the tables (ensure tables are created when running)
with app.app_context():
    db.create_all()

# Define route for homepage
@app.route('/')
def index():
    a = User.query.filter_by(name='fayo').first()
    if a:  # Check if 'fayo' exists in the database
       return f"Hello {a.name}, you joined on {a.date_joined.strftime('%Y-%m-%d')}"
    return "User 'ayo' not found."

# Function to log SQL queries after each request
@app.after_request
def sql_debug(response):
    from flask_sqlalchemy.record_queries import get_recorded_queries
    
    queries = list(get_recorded_queries())
    query_str = ''
    total_duration = 0.0
    
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement)
        
        # Here, we manually substitute the parameters into the query string for display purposes
        if q.parameters:
            stmt = stmt % q.parameters
            
        stmt = stmt.replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    print('=' * 80)
    print('SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')

    return response


# Start the app
if __name__ == "__main__":
    app.run(debug=True)
