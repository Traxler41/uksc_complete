from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://uksc:Ebhwtcl_14@localhost/uksc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    name1 = db.column(db.String(200))
    email1 = db.Column(db.String(200))
    phno1 = db.Column(db.String(20))
    msg = db.Column(db.String(5000))
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

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
        return redirect(url_for('academy'))
    else:

        df = pd.read_excel('static/docs/home-page/standings.xlsx')
        standings_data = df.to_dict(orient='records')

        base_path = os.path.join('static', 'docs', 'home-page')

        #Past Home-Team Data
        home_team_name_path = os.path.join(base_path, 'past_home_team', 'home-team.txt')
        home_goalscorers_path = os.path.join(base_path, 'past_home_team', 'home-team-goalscorers.txt')
        home_logo_path = os.path.join('docs','home-page', 'past_home_team', 'home-team-logo.png').replace('\\','/')

        #Past Away-Team Data
        away_team_name_path = os.path.join(base_path, 'past_away_team', 'away-team.txt')
        away_goalscorers_path = os.path.join(base_path,'past_away_team', 'away-team-goalscorers.txt')
        away_logo_path = os.path.join('docs', 'home-page', 'past_away_team', 'away-team-logo.png').replace('\\','/')   

        #Score Data
        score_path = os.path.join(base_path, 'past_score.txt')

        #Upcoming Match Details
        upcoming_home_page_match_details_path = os.path.join(base_path, 'upcoming-match-details.txt')

        #Upcoming Home Team Details
        upcoming_home_team_name_path = os.path.join(base_path, 'next_home_team', 'home-team.txt')
        upcoming_home_team_logo_path = os.path.join('docs', 'home-page', 'next_home_team', 'home-team-logo.png')

        #Upcoming Away Match Details
        upcoming_away_team_name_path = os.path.join(base_path, 'next_away_team', 'away-team.txt')
        upcoming_away_team_logo_path = os.path.join('docs', 'home-page', 'next_away_team', 'away-team-logo.png')

        #Read from the files
        try:
            with open(home_team_name_path, 'r') as file:
                home_team_name = file.read().strip() 

            with open(home_goalscorers_path, 'r') as file:
                    home_goalscorers = file.read().strip().split('\n') if os.path.getsize(home_goalscorers_path) > 0 else []

            with open(away_team_name_path, 'r') as file:
                away_team_name = file.read().strip()
            
            with open(away_goalscorers_path, 'r') as file:
                    away_goalscorers = file.read().strip().split('\n') if os.path.getsize(away_goalscorers_path) > 0 else []

            with open(score_path, 'r') as file:
                score = file.read().strip()

            with open(upcoming_home_page_match_details_path, 'r') as file:
                upcoming_home_page_match_details = file.read().strip().split('\n')

            with open(upcoming_home_team_name_path, 'r') as file:
                upcoming_home_team_name = file.read().strip()

            with open(upcoming_away_team_name_path, 'r') as file:
                upcoming_away_team_name = file.read().strip()


        except FileNotFoundError as e:
            return f"Error: {e}. Please ensure all files exist.", 



        return render_template('index.html',
                            standings=standings_data,
                            home_team_name=home_team_name,
                            home_goalscorers=home_goalscorers,
                            home_logo_path=home_logo_path,
                            away_team_name=away_team_name,
                            away_goalscorers=away_goalscorers,
                            away_logo_path=away_logo_path,
                            score=score,
                            upcoming_home_team_name=upcoming_home_team_name,
                            upcoming_home_team_logo = upcoming_home_team_logo_path.replace('\\','/'),
                            upcoming_away_team_name=upcoming_away_team_name,
                            upcoming_away_team_logo=upcoming_away_team_logo_path.replace('\\','/'),
                            upcoming_home_page_match_details=upcoming_home_page_match_details
                            )

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/matches')
def matches():

    base_path = os.path.join('static', 'docs', 'matches')

    #Past Home-Team Data
    home_team_name_path = os.path.join(base_path, 'past_home_team', 'home-team.txt')
    home_goalscorers_path = os.path.join(base_path, 'past_home_team', 'home-team-goalscorers.txt')
    home_logo_path = os.path.join('docs','matches', 'past_home_team', 'home-team-logo.png').replace('\\','/')

    #Past Away-Team Data
    away_team_name_path = os.path.join(base_path, 'past_away_team', 'away-team.txt')
    away_goalscorers_path = os.path.join(base_path,'past_away_team', 'away-team-goalscorers.txt')
    away_logo_path = os.path.join('docs', 'matches', 'past_away_team', 'away-team-logo.png').replace('\\','/')   

    #Score Data
    score_path = os.path.join(base_path, 'past_score.txt')

    #Next Home-Team Data
    next_home_team_name_path = os.path.join(base_path, 'next_home_team', 'next-home-team.txt')
    next_home_team_logo_path = os.path.join('docs', 'matches', 'next_home_team', 'home-team-logo.png').replace('\\','/')

    #Next Away-Team Details
    next_away_team_name_path = os.path.join(base_path, 'next_away_team', 'next-away-team.txt')
    next_away_team_logo_path = os.path.join('docs', 'matches', 'next_away_team', 'away-team-logo.png').replace('\\','/')

    #Next Match Details
    next_match_details_path = os.path.join(base_path, 'next-match-details.txt')

    upcoming_matches_base_path = os.path.join('static', 'docs', 'matches', 'upcoming_matches')

    upcoming_matches = [] #To store the list of upcoming matches

    for i in range(1,5):
        match_folder = os.path.join(upcoming_matches_base_path, str(i))
        upcoming_images_path = os.path.join('docs', 'matches', 'upcoming_matches', str(i))

        #Upcoming Match Details
        upcoming_match_details_path = os.path.join(match_folder, 'upcoming_match_details.txt')

        #Home Team
        upcoming_home_team_name_path = os.path.join(match_folder, 'Home-Team', 'home-team-name.txt')
        upcoming_home_team_logo_path = os.path.join(upcoming_images_path, 'Home-Team', 'home-team.png')

        #Away Team
        upcoming_away_team_name_path = os.path.join(match_folder, 'Away-Team', 'away-team-name.txt')
        upcoming_away_team_logo_path = os.path.join(upcoming_images_path, 'Away-Team', 'away-team.png')

        try:
            with open(upcoming_home_team_name_path, 'r') as file:
                upcoming_home_team_name = file.read().strip()

            with open(upcoming_away_team_name_path, 'r') as file:
                upcoming_away_team_name = file.read().strip()

            with open(upcoming_match_details_path, 'r') as file:
                upcoming_match_details = file.read().strip().split('\n')
        
            upcoming_matches.append({
                'home_team_logo': upcoming_home_team_logo_path.replace('\\','/'),
                'home_team_name': upcoming_home_team_name,
                'away_team_logo': upcoming_away_team_logo_path.replace('\\','/'),
                'away_team_name': upcoming_away_team_name,
                'match_details': upcoming_match_details
        })
        except:
            return f"Error: {e}. Please ensure all files exist.", 500


    #Read from the files
    try:
        with open(home_team_name_path, 'r') as file:
            home_team_name = file.read().strip() 

        with open(home_goalscorers_path, 'r') as file:
                home_goalscorers = file.read().strip().split('\n') if os.path.getsize(home_goalscorers_path) > 0 else []

        with open(away_team_name_path, 'r') as file:
            away_team_name = file.read().strip()
        
        with open(away_goalscorers_path, 'r') as file:
                away_goalscorers = file.read().strip().split('\n') if os.path.getsize(away_goalscorers_path) > 0 else []

        with open(score_path, 'r') as file:
            score = file.read().strip()

        with open(next_home_team_name_path, 'r') as file:
            next_home_team_name = file.read().strip()

        with open(next_away_team_name_path, 'r') as file:
            next_away_team_name = file.read().strip()

        with open(next_match_details_path, 'r') as file:
            match_details = file.read().strip().split('\n')
        
    


    except FileNotFoundError as e:
        return f"Error: {e}. Please ensure all files exist.", 500

    return render_template('matches.html',
                           home_team_name=home_team_name,
                           home_goalscorers=home_goalscorers,
                           home_logo_path=home_logo_path,
                           away_team_name=away_team_name,
                           away_goalscorers=away_goalscorers,
                           away_logo_path=away_logo_path,
                           score=score,
                           next_home_team_name=next_home_team_name,
                           next_home_logo=next_home_team_logo_path,
                           next_away_team_name=next_away_team_name,
                           next_away_logo=next_away_team_logo_path,
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

app.run(debug=True)
