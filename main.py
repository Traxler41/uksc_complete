from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://uksc_user:Ebhwtcl_14@localhost/uksc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = b'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR\xa1\xa8\x18'
ADMIN_SECRET_KEY = 'dev-key-123'

class uksc_academy(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phno = db.Column(db.String(20), nullable=False)
    crs = db.Column(db.String(15), nullable=True)
    age = db.Column(db.String(3), nullable=False)
    address = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class uksc_contact(db.Model):
    sno1 = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(200), nullable=False)
    email1 = db.Column(db.String(200), nullable=False)
    phno1 = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class home_page_standings(db.Model):
    position = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(50), nullable=False)
    matches_played = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    draws = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)

class home_page_names(db.Model):
    __tablename__ = 'home_page_names'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    next_away_team_name = db.Column(db.String(100), nullable=False)
    next_home_team_name = db.Column(db.String(100), nullable=False)
    past_away_team_name = db.Column(db.String(100), nullable=False)
    past_home_team_name = db.Column(db.String(100), nullable=False)
    past_score = db.Column(db.String(100), nullable=False)
    upcoming_match_tournament_name = db.Column(db.String(200), nullable=False)
    upcoming_match_date = db.Column(db.String(100), nullable=False)
    upcoming_match_time = db.Column(db.String(100), nullable=False)
    upcoming_match_venue = db.Column(db.String(100), nullable=False)
    home_team_goalscorers = db.Column(db.String(500), nullable=False)
    away_team_goalscorers = db.Column(db.String(500), nullable=False)

class matches_names(db.Model):
    __tablename__ = 'matches_names'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Last match data
    last_match_home_team_name = db.Column(db.String(100))
    last_match_away_team_name = db.Column(db.String(100))
    last_match_score = db.Column(db.String(50))
    last_match_home_team_scorers = db.Column(db.Text)  # Comma-separated
    last_match_away_team_scorers = db.Column(db.Text)  # Comma-separated
    
    # Next match data
    next_match_home_team_name = db.Column(db.String(100))
    next_match_away_team_name = db.Column(db.String(100))
    next_match_tournament_name = db.Column(db.String(100))
    next_match_date = db.Column(db.String(50))
    next_match_time = db.Column(db.String(50))
    next_match_venue = db.Column(db.String(100))
    
    # Upcoming matches (1-4)
    home_team_name_1 = db.Column(db.String(100))
    away_team_name_1 = db.Column(db.String(100))
    tournament_name_1 = db.Column(db.String(100))
    match_date_1 = db.Column(db.String(50))
    match_time_1 = db.Column(db.String(50))
    match_venue_1 = db.Column(db.String(100))
    
    # Repeat for matches 2-4
    home_team_name_2 = db.Column(db.String(100))
    away_team_name_2 = db.Column(db.String(100))
    tournament_name_2 = db.Column(db.String(100))
    match_date_2 = db.Column(db.String(50))
    match_time_2 = db.Column(db.String(50))
    match_venue_2 = db.Column(db.String(100))
    
    home_team_name_3 = db.Column(db.String(100))
    away_team_name_3 = db.Column(db.String(100))
    tournament_name_3 = db.Column(db.String(100))
    match_date_3 = db.Column(db.String(50))
    match_time_3 = db.Column(db.String(50))
    match_venue_3 = db.Column(db.String(100))
    
    home_team_name_4 = db.Column(db.String(100))
    away_team_name_4 = db.Column(db.String(100))
    tournament_name_4 = db.Column(db.String(100))
    match_date_4 = db.Column(db.String(50))
    match_time_4 = db.Column(db.String(50))
    match_venue_4 = db.Column(db.String(100))
    
    # Logo paths (optional - can remain file-based)
    #home_logo_path = db.Column(db.String(200))
    #away_logo_path = db.Column(db.String(200))
    #next_home_logo_path = db.Column(db.String(200))
    #next_away_logo_path = db.Column(db.String(200))

class admin_users(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        print(request.form)
        name = request.form.get('name')
        email = request.form.get('email')
        phno = request.form.get('phone')
        crs = request.form.get('CRS')
        age = request.form.get('age')
        address = request.form.get('address')

        print(f"Name: {name}, Email: {email}, Phone: {phno}, CRS: {crs}, Age: {age}, Address: {address}")

        if crs == "":
            crs = None
        
        new_uksc_academy = uksc_academy(
            name=name,
            email=email,
            phno = phno,
            crs = crs,
            age=age,
            address=address
        )

        db.session.add(new_uksc_academy)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500  # Return an error response

        # Redirect to a success page or the same page
        return redirect(url_for('home'))
    else:
        #Standings Data
        standings_data = home_page_standings.query.order_by(home_page_standings.position).all()

        #Get all the match details from the database
        match_data = home_page_names.query.first()

        if not match_data:
            return "Error: No match data found in database", 500
        
        # Convert goalscorers strings to lists
        home_goalscorers = match_data.home_team_goalscorers.split(', ') if match_data.home_team_goalscorers else []
        away_goalscorers = match_data.away_team_goalscorers.split(', ') if match_data.away_team_goalscorers else []
        
        # Prepare upcoming match details
        upcoming_match_details = [
            match_data.upcoming_match_tournament_name,
            match_data.upcoming_match_date,
            match_data.upcoming_match_time,
            match_data.upcoming_match_venue
        ]



        home_logo_path = os.path.join('docs','home-page', 'past_home_team', 'home-team-logo.png').replace('\\','/')
        away_logo_path = os.path.join('docs', 'home-page', 'past_away_team', 'away-team-logo.png').replace('\\','/')   
        upcoming_home_team_logo_path = os.path.join('docs', 'home-page', 'next_home_team', 'home-team-logo.png').replace('\\','/')
        upcoming_away_team_logo_path = os.path.join('docs', 'home-page', 'next_away_team', 'away-team-logo.png').replace('\\','/')



        return render_template('index.html',
                            standings=standings_data,
                            home_team_name=match_data.past_home_team_name,
                            home_goalscorers=home_goalscorers,
                            home_logo_path=home_logo_path,
                            away_team_name=match_data.past_away_team_name,
                            away_goalscorers=away_goalscorers,
                            away_logo_path=away_logo_path,
                            score=match_data.past_score,
                            upcoming_home_team_name=match_data.next_home_team_name,
                            upcoming_home_team_logo=upcoming_home_team_logo_path,
                            upcoming_away_team_name=match_data.next_away_team_name,
                            upcoming_away_team_logo=upcoming_away_team_logo_path,
                            upcoming_home_page_match_details=upcoming_match_details
        )

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/matches')
def matches():
    # Get all match data from database
    match_data = db.session.query(
        matches_names.last_match_home_team_name,
        matches_names.last_match_away_team_name,
        matches_names.last_match_score,
        matches_names.last_match_home_team_scorers,
        matches_names.last_match_away_team_scorers,
        matches_names.next_match_home_team_name,
        matches_names.next_match_away_team_name,
        matches_names.next_match_tournament_name,
        matches_names.next_match_date,
        matches_names.next_match_time,
        matches_names.next_match_venue,
        matches_names.home_team_name_1,
        matches_names.away_team_name_1,
        matches_names.tournament_name_1,
        matches_names.match_date_1,
        matches_names.match_time_1,
        matches_names.match_venue_1,
        matches_names.home_team_name_2,
        matches_names.away_team_name_2,
        matches_names.tournament_name_2,
        matches_names.match_date_2,
        matches_names.match_time_2,
        matches_names.match_venue_2,
        matches_names.home_team_name_3,
        matches_names.away_team_name_3,
        matches_names.tournament_name_3,
        matches_names.match_date_3,
        matches_names.match_time_3,
        matches_names.match_venue_3,
        matches_names.home_team_name_4,
        matches_names.away_team_name_4,
        matches_names.tournament_name_4,
        matches_names.match_date_4,
        matches_names.match_time_4,
        matches_names.match_venue_4
    ).first()

    if not match_data:
        return "Error: No match data found in database", 500

    # Process last match goalscorers
    home_goalscorers = match_data.last_match_home_team_scorers.split(', ') if match_data.last_match_home_team_scorers else []
    away_goalscorers = match_data.last_match_away_team_scorers.split(', ') if match_data.last_match_away_team_scorers else []

    # Prepare next match details
    match_details = [
        match_data.next_match_tournament_name,
        match_data.next_match_date,
        match_data.next_match_time,
        match_data.next_match_venue
    ]

    # Prepare upcoming matches (1-4)
    upcoming_matches = []
    for i in range(1, 5):
        upcoming_matches.append({
            'home_team_name': getattr(match_data, f'home_team_name_{i}'),
            'away_team_name': getattr(match_data, f'away_team_name_{i}'),
            'match_details': [
                getattr(match_data, f'tournament_name_{i}'),
                getattr(match_data, f'match_date_{i}'),
                getattr(match_data, f'match_time_{i}'),
                getattr(match_data, f'match_venue_{i}')
            ],
            'home_team_logo': os.path.join('docs', 'matches', 'upcoming_matches', str(i), 'Home-Team', 'home-team.png').replace('\\','/'),
            'away_team_logo': os.path.join('docs', 'matches', 'upcoming_matches', str(i), 'Away-Team', 'away-team.png').replace('\\','/')
        })

    # File-based logo paths
    home_logo_path = os.path.join('docs','matches', 'past_home_team', 'home-team-logo.png').replace('\\','/')
    away_logo_path = os.path.join('docs', 'matches', 'past_away_team', 'away-team-logo.png').replace('\\','/')
    next_home_logo_path = os.path.join('docs', 'matches', 'next_home_team', 'home-team-logo.png').replace('\\','/')
    next_away_logo_path = os.path.join('docs', 'matches', 'next_away_team', 'away-team-logo.png').replace('\\','/')

    return render_template('matches.html',
        home_team_name=match_data.last_match_home_team_name,
        home_goalscorers=home_goalscorers,
        home_logo_path=home_logo_path,
        away_team_name=match_data.last_match_away_team_name,
        away_goalscorers=away_goalscorers,
        away_logo_path=away_logo_path,
        score=match_data.last_match_score,
        next_home_team_name=match_data.next_match_home_team_name,
        next_home_logo=next_home_logo_path,
        next_away_team_name=match_data.next_match_away_team_name,
        next_away_logo=next_away_logo_path,
        match_details=match_details,
        upcoming_matches=upcoming_matches
    )

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name1 = request.form.get('name1')
        email1 = request.form.get('email1')
        phno1 = request.form.get('phno1')
        msg = request.form.get('msg')

        new_uksc_contact = uksc_contact(
            name1=name1,
            email1=email1,
            phno1=phno1,
            msg=msg
        )
        db.session.add(new_uksc_contact)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500  # Return an error response

        # Redirect to a success page or the same page
        return redirect(url_for('contact'))
    else:
        return render_template('contact.html')

@app.route('/rahul_news')
def rahul_news():
    return render_template('rahul_article.html')

@app.route('/prasanta_news')
def prasanta_news():
    return render_template('prasanta_news.html')

@app.route('/sameer_news')
def sameer_news():
    return render_template('sameer_news.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/academy', methods=["POST","GET"])
def academy():
    if request.method == 'POST':
        print(request.form)
        name = request.form.get('name')
        email = request.form.get('email')
        phno = request.form.get('phone')
        crs = request.form.get('CRS')
        age = request.form.get('age')
        address = request.form.get('address')

        print(f"Name: {name}, Email: {email}, Phone: {phno}, CRS: {crs}, Age: {age}, Address: {address}")

        if crs == "":
            crs = None
        
        new_uksc_academy = uksc_academy(
            name=name,
            email=email,
            phno = phno,
            crs = crs,
            age=age,
            address=address
        )

        db.session.add(new_uksc_academy)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500  # Return an error response

        # Redirect to a success page or the same page
        return redirect(url_for('academy'))
    else:
        return render_template('academy.html')

@app.route('/coming_soon')
def coming_soon():
    return render_template('coming-soon.html')

# ===========================ADMIN ROUTES===================================
@app.route('/admin_signup', methods=['POST'])
def admin_signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    admin_key = request.form.get('admin_key')

    # Example admin key
    correct_admin_key = 'YOUR_SECRET_KEY'  # replace this

    if admin_key != correct_admin_key:
        return {'success': False, 'message': 'Invalid admin secret key.'}

    if password != confirm_password:
        return {'success': False, 'message': "Passwords don't match."}

    existing_user = admin_users.query.filter_by(email=email).first()
    if existing_user:
        return {'success': False, 'message': 'Email already registered. Please login.'}

    hashed_password = generate_password_hash(password)
    new_user = admin_users(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {'success': True, 'message': 'Account created successfully! Please login.'}

@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = admin_users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        return {'success': True, 'redirect': url_for('admin_dashboard')}
    else:
        return {'success': False, 'message': 'Invalid email or password.'}

@app.route('/admin_dashboard')
def admin_dashboard():

    home_page_names_data = home_page_names.query.all()
    standings = home_page_standings.query.all()
    matches_names_data = matches_names.query.all()
    uksc_academy_data = uksc_academy.query.all()
    uksc_contact_data = uksc_contact.query.all()

    return render_template(
        'admin/admin_dashboard.html',
        user_name=session.get('user_name'),
        home_page_names=home_page_names_data,
        standings=standings,
        matches_names=matches_names_data,
        uksc_academy=uksc_academy_data,
        uksc_contact=uksc_contact_data
    )

@app.route('/signup_login')
def signup_login():
    return render_template('admin/login_signup.html')

@app.route('/update_home_page_names', methods=['POST'])
def update_home_page_names():
    for row in home_page_names:
        new_name = request.form.get(f'name_{row.id}')
        new_photo = request.files.get(f'photo_{row.id}')
        old_photo = request.form.get(f'old_photo_{row.id}')

        # Update name and handle photo upload
        if new_photo:
            # Delete the old photo if new one is uploaded
            os.remove(os.path.join('static', old_photo))
            # Save the new photo
            new_photo_path = os.path.join('static', 'images', new_photo.filename)
            new_photo.save(new_photo_path)
            row.photo = 'images/' + new_photo.filename

        row.name = new_name
        db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/delete_uksc_academy/<int:sno>', methods=['DELETE'])
def delete_uksc_academy(sno):
    row = uksc_academy.query.get(sno)
    db.session.delete(row)
    db.session.commit()
    return '', 204

@app.route('/delete_uksc_contact/<int:sno1>', methods=['DELETE'])
def delete_uksc_contact(sno1):
    row = uksc_contact.query.get(sno1)
    db.session.delete(row)
    db.session.commit()
    return '', 204

@app.route('/update_standings', methods=['POST'])
def update_standings():
    # Handle adding new standings row if requested
    add_new = request.form.get('add_new')  # A flag to check if a new row needs to be added
    
    if add_new:
        # Get new standing data from the form
        team_name = request.form.get('new_team_name')
        matches_played = request.form.get('new_matches_played')
        points = request.form.get('new_points')
        wins = request.form.get('new_wins')
        draws = request.form.get('new_draws')
        losses = request.form.get('new_losses')
        
        # Create a new home_page_standings row
        new_standing = home_page_standings(
            team=team_name,
            matches_played=int(matches_played),
            points=int(points),
            wins=int(wins),
            draws=int(draws),
            losses=int(losses)
        )
        
        db.session.add(new_standing)
        db.session.commit()
    
    # Handle updating existing standings rows
    for row in home_page_standings.query.all():
        new_team_name = request.form.get(f'team_name_{row.position}')
        new_matches_played = request.form.get(f'matches_played_{row.position}')
        new_points = request.form.get(f'points_{row.position}')
        new_wins = request.form.get(f'wins_{row.position}')
        new_draws = request.form.get(f'draws_{row.position}')
        new_losses = request.form.get(f'losses_{row.position}')
        
        # Check if any of the fields have been changed
        if new_team_name and new_matches_played and new_points:
            row.team = new_team_name
            row.matches_played = int(new_matches_played)
            row.points = int(new_points)
            row.wins = int(new_wins)
            row.draws = int(new_draws)
            row.losses = int(new_losses)
            db.session.commit()
    
    # Handle deleting a row (if 'delete' flag is set for any team)
    delete_team = request.form.get('delete_team')
    if delete_team:
        row_to_delete = home_page_standings.query.filter_by(team=delete_team).first()
        if row_to_delete:
            db.session.delete(row_to_delete)
            db.session.commit()
    
    # After handling all updates, redirect to the admin dashboard or appropriate page
    return redirect(url_for('admin_dashboard'))

@app.route('/update_matches_names', methods=['POST'])
def update_matches_names():
    # Retrieve the 'matches_names' data
    match = matches_names.query.first()  # Assume you have a single row in this table
    
    # Last Match Update
    match.last_match_home_team_name = request.form.get('last_match_home_team_name')
    match.last_match_away_team_name = request.form.get('last_match_away_team_name')
    match.last_match_score = request.form.get('last_match_score')
    match.last_match_home_team_scorers = request.form.get('last_match_home_team_scorers')
    match.last_match_away_team_scorers = request.form.get('last_match_away_team_scorers')
    
    # NEW: Last Match Logo Paths
    match.home_logo_path = request.form.get('home_logo_path')
    match.away_logo_path = request.form.get('away_logo_path')

    # Next Match Update
    match.next_match_home_team_name = request.form.get('next_match_home_team_name')
    match.next_match_away_team_name = request.form.get('next_match_away_team_name')
    match.next_match_tournament_name = request.form.get('next_match_tournament_name')
    match.next_match_date = request.form.get('next_match_date')
    match.next_match_time = request.form.get('next_match_time')
    match.next_match_venue = request.form.get('next_match_venue')

    # NEW: Next Match Logo Paths
    match.next_home_logo_path = request.form.get('next_home_logo_path')
    match.next_away_logo_path = request.form.get('next_away_logo_path')

    # Upcoming Matches Update (1-4)
    for i in range(1, 5):  # Matches 1 to 4
        match_home_team = request.form.get(f'home_team_name_{i}')
        match_away_team = request.form.get(f'away_team_name_{i}')
        match_tournament = request.form.get(f'tournament_name_{i}')
        match_date = request.form.get(f'match_date_{i}')
        match_time = request.form.get(f'match_time_{i}')
        match_venue = request.form.get(f'match_venue_{i}')

        setattr(match, f'home_team_name_{i}', match_home_team)
        setattr(match, f'away_team_name_{i}', match_away_team)
        setattr(match, f'tournament_name_{i}', match_tournament)
        setattr(match, f'match_date_{i}', match_date)
        setattr(match, f'match_time_{i}', match_time)
        setattr(match, f'match_venue_{i}', match_venue)

    # Commit changes to the database
    db.session.commit()

    # Redirect back to the admin dashboard or another appropriate page
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_academy/<int:sno>', methods=['POST'])
def delete_academy(sno):
    record = uksc_academy.query.get_or_404(sno)
    db.session.delete(record)
    db.session.commit()
    return '', 204

@app.route('/delete_contact/<int:sno1>', methods=['POST'])
def delete_contact(sno1):
    record = uksc_contact.query.get_or_404(sno1)
    db.session.delete(record)
    db.session.commit()
    return '', 204



app.run(debug=True)
