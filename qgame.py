from flask import Flask,render_template,json,redirect,url_for,session, escape, request

app = Flask(__name__)
app.secret_key = 'sec'
import os
import logging
import pandas as pd
import datetime
from flask import Flask, jsonify

from flask import Flask,render_template,request,json,redirect,url_for
import csv
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models.pandas import Base, Questions, UserStatus, Department, Track, TrackNomination, Team, TeamParticipant, TeamScore
import models.pandas as sqlm
import numpy as np
def read_csv_convert_json(filepath):
	data=pd.read_csv(filepath)
	data.fillna(value=np.nan, inplace=True)
	data=json.loads(data.to_json(orient='records'))
	return data

completed_ratio_path='static/data/completedRatioChart.csv'
# comp_vs_create_data=read_csv_convert_json(completed_ratio_path)
#print comp_vs_create_data
# DEV_PORT = 59999
BLL_DB = 'examples7.db'

PAGPUZZLE_DB = 'pagpuzzle3.db'


@app.after_request
def add_header(response):
	response.headers["Cache-Control"] = "no-cache, must-revalidate" # HTTP 1.1.
	response.headers["Pragma"] = "no-cache" # HTTP 1.0.
	response.headers["Expires"] = "0" # Proxies.
	return response
	
@app.route('/')
def home():
    currentDT = datetime.datetime.now()
    my_home = url_for('home', _external=True)
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b> <b> </b>" +\
                "<b><a href = '/quest'>click here to go to questions</a></b>"


    return "You are not logged in <br><a href = '/login'></b>" + \
       "click here to log in</b></a>" +\
        " home = {}".format(my_home)


@app.route('/input',  methods=["GET"])
def input():
    return render_template('input-form.html')


# this fuction will allow users to enter login details
@app.route('/login')
def login():
    my_home = url_for('home', _external=True)
    return render_template('login.html',home_url = my_home)

@app.route('/leaderBoard')
def test_me():
    engine = create_engine('sqlite:///pagpuzzle3.db')
    Base.metadata.create_all(engine, checkfirst=True)

    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()


    db_session.commit()
    msg = ""
    df = sqlm.getUserStatus(db_session)

    # ustatus = db_session.query(UserStatus).all().order_by(desc(UserStatus.level))
    # for us in ustatus:
    #     msg = str(msg) + str(type(ustatus)) +"test "
    #     msg = str(msg) + '<br>' + " {}  {} {} {}".format(us.id, us.user_id, us.quest_id, us.level)
    #     print(us.id, us.user_id, us.quest_id, us.level)
    df3 = df.sort_values(by='Level', ascending=False)
    df3 = df3.reset_index(drop=True)
    df3.index = np.arange(1,len(df3)+1)
    print(df3)
    df3.to_html(r"templates\leadboardpag.html")
    db_session.close()
    return render_template('leadboardpag.html')



    return msg




#END OF TEST ME FUNCTION

@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == "POST":

        return render_template('registration.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('home'))




@app.route('/login-validate',methods = ['POST', 'GET'])
def login_validate():
    msg = ""
    if request.method == "POST":
        msg = msg + "User : " + request.form["username"]

        username = request.form["username"]
        password = request.form["password"]
        session['username'] = username
    engine = create_engine('sqlite:///%s' % PAGPUZZLE_DB)

    Base.metadata.create_all(engine, checkfirst=True)

    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    sqlm.addUser(db_session,username,password)
    # sqlm.addQuestions(db_session, "1", "3")
    # sqlm.addQuestions(db_session, "2", "5")
    # sqlm.addQuestions(db_session, "3", "8")
    # sqlm.addQuestions(db_session, "4", "12")
    # db_session.commit()
    # print("Checking what all questions we do have.")
    # quest = db_session.query(Questions).all()
    # for q in quest:
    #     print(q.id,  q.ans_id)
    # print("question bank check finished. ")

    tmp_pass = sqlm.getPassword(db_session,username)
    if tmp_pass is None:
        sqlm.addUser(db_session, username, password)
        db_session.commit()
        db_session.close()
    elif tmp_pass == password :
        db_session.close()
        return redirect(url_for('quest'))

    else :
        session.pop('username', None)
        db_session.close()
        return "Incorrect Password <br><a href = '/login'></b>" + \
               "click here to log in</b></a>"
    # userDetails = UserLoginDetails(userid=username, password=password)
    # db_session.add(userDetails)


    if 'username' in session:
        user_session = session['username']

    # uname = db_session.query(UserLoginDetails).filter(UserLoginDetails.userid == username).first()
    # msg = str(msg) + "\nPass : " + sqlm.getPassword(db_session, username)
    # Add Nominations
    # userdetail = sqlm.getNomination(db_session, track.lower(), email.lower(), year)
    # if nomination is not None:
    #     return "Participant with %s email id is already added to the nomination ist for track %s year %s" % (
    #     nomination.participant.email, nomination.track.name, year)

    # sqlm.addUser(db_session, username.lower(),password)
    #
    # db_session.commit()
    # nominations = sqlm.getTrackNomination(db_session, None, None, 2018)
    # db_session.close()
    # engine.dispose()
    msg += "You have logged in as {} ".format(session['username'])

    return redirect(url_for('quest'))



@app.route('/quest',methods = ['POST', 'GET'])
def quest():
    msg = "You have logged in as {} ".format(session['username'])
    engine = create_engine('sqlite:///%s' % PAGPUZZLE_DB)

    Base.metadata.create_all(engine, checkfirst=True)

    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()


    if request.method == "POST":
        user_session = session['username']
        if request.method == "POST":
            ans = request.form["ans"]
            q_id  = request.form['q_id']
            if q_id == "1" and ans =="3":
                msg = str(msg) + "You answered correctly. "
                sqlm.addUserStatus(db_session,user_session,q_id,q_id)
                db_session.commit()
                db_session.close()
                return render_template('Q2.html')
            else:
                print("Calling get")
                correct_ans = sqlm.getAnswer(db_session, q_id)
                if correct_ans == ans :
                    sqlm.updateUserStatus(db_session, user_session, q_id, q_id)
                    db_session.close()
                    return render_template('Q%s.html'%str(int(q_id)+1))
                else :
                    print("Someting went wrong, Check user:{} q_id:{} , level:{}"\
                          .format(user_session, q_id, q_id))
                    return render_template('Q%s.html' % str(int(q_id)))


    else :
        db_session.close()
        return render_template('Q1.html')
    return msg


@app.route('/showusers/<user>', methods=['GET', 'POST'])
def ShowUsers(user: str):
    engine = create_engine('sqlite:///%s' % BLL_DB)
    Base.metadata.create_all(engine, checkfirst=True)
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()

    userDetails = sqlm.getPassword(db_session, user)
    db_session.close()
    engine.dispose()
    return """
                    <html>
                    <body>
               """ + userDetails.to_html() + """
                    <form action = "http://hkgmd1250276:59999/allocation-form" method = "GET">
             				<p><input type = "submit" value = "Allocate Teams" /></p>
         					 </form>          
                    </body>
                    </html>
               """
    db_session.close()
    engine.dispose()



# this fuction will deal with nomination of participants
@app.route('/nomination')
def nomination():
    return render_template('nomination-form.html')



@app.route("/add", methods=["GET", "POST"])
def add():
    errors = ""
    if request.method == "POST":
        number1 = None
        number2 = None
        try:
            number1 = float(request.form["number1"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        try:
            number2 = float(request.form["number2"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        if number1 is not None and number2 is not None:
            result = number1+ number2
            return '''
                <html>
                    <body>
                        <p>The result is {result}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)

    return '''
        <html>
            <body>
                {errors}
                <p>Enter your numbers:
                <form method="post" action=".">
                    <p><input name="number1" /></p>
                    <p><input name="number2" /></p>
                    <p><input type="submit" value="Do calculation" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)


@app.route('/input-form', methods=['GET', 'POST']) #allow both GET and POST requests
def input_form():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        empId = request.form.get('empId')
        empName = request.form['empName']
        empTopic = request.form['empTopic']
        empScore = request.form['empScore']
        empTrack = request.form['empTrack']
        empTeam = request.form['empTeam']

        emp_row = [empId,empName,empTopic,empScore,empTrack, empTeam]
        write_csv(emp_row)
        convertToHtml("Leadership.csv")
        return '''<h1>Congratulations your record has been saved as below </h1>
                  <h1>The Emp Id  is: {}</h1>
                  <h1>The Emp Name  is: {}</h1>
                  <h1>Topic is: {}</h1>
                  <h1>Score is: {}</h1>
                  <h1>Track is: {}</h1>
                  <h1>Team is: {}</h1> <a href="http://hkgmd1250276:59999/leadership">Leadership Board</a> '''.format(add_msg(empId), empName, empTopic,empScore,empTrack, empTeam)

    return '''<form method="POST">
                  emp_id: <input type="text" name="empId"><br>
                  emp_name: <input type="text" name="empName"><br>
                  emp_topic: <input type='test' name="empTopic"><br>
                  emp_score:<input type='test' name="empScore"><br>
                  emp_track:<input type='test' name="empTrack"><br>
                  emp_team:<input type='test' name="empTeam"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


@app.route('/leadership')
def leadership():
   return render_template("leadboardMVP.html")

@app.route('/attendance')
def attendance():
   return render_template("attendance.html")

@app.route('/allocation-form')
def allocationform():
   return render_template("allocation-form.html")

@app.route('/leadershipteam')
def leadershipteam():
   return render_template("leadboardteam.html")


def add_msg(msg):
    return msg

@app.route('/showLeads')
def showLeads():
    body = ""
    rec = {}
    with open("leadboard.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rec[row['Name']] = row['score']

    return render_template("showresult.html", result=rec)

@app.route('/show-nominations', methods=["GET"])
def showNomination():
    # Creating sqllite database

    engine = create_engine('sqlite:///%s'%BLL_DB)
    Base.metadata.create_all(engine, checkfirst=True)
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()

    nominations = sqlm.getTrackNomination(db_session, None, None, 2018)
    db_session.close()
    engine.dispose()
    return """
                <html>
                <body>
           """ + nominations.to_html() +"""
                <form action = "http://hkgmd1250276:59999/allocation-form" method = "GET">
         				<p><input type = "submit" value = "Allocate Teams" /></p>
     					 </form>          
                </body>
                </html>
           """
    db_session.close()
    engine.dispose()

@app.route('/show-participants', methods=["GET"])
def showParticipants():
    # Creating sqllite database

    engine = create_engine('sqlite:///%s'%BLL_DB)
    Base.metadata.create_all(engine, checkfirst=True)
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()

    participants = sqlm.getParticipants(db_session, None, None, 2018)
    db_session.close()
    engine.dispose()
    return """
                <html>
                <body>
           """ + participants.to_html() +"""
                <form action = "http://hkgmd1250276:59999/input" method = "GET">
         				<p><input type = "submit" value = "Mark Course Completion" /></p>
     					 </form>          
                </body>
                </html>
           """
    db_session.close()
    engine.dispose()

# this fuction will deal with nomination of participants
@app.route('/allocate-teams', methods=["POST"])
def allocateTeams():
    result = request.form
    currentDT = datetime.datetime.now()
    str_curr_DT = str(currentDT)

    year = int(request.form['year'])
    python_size = int(request.form['python_size'])
    r_size = int(request.form['r_size'])
    python_teams = []
    r_teams = []
    for i in range(1,5):
        python_teams.append(request.form['python_team%s'%i])
        r_teams.append(request.form['r_team%s'%i])

    engine = create_engine('sqlite:///%s'%BLL_DB)
    Base.metadata.create_all(engine, checkfirst=True)
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    nominations = sqlm.getTrackNomination(db_session, None, None, year)
    results = allocateParticipants(nominations, {'python': python_teams, 'r': r_teams}, {'beginner':10, 'intermediate':3, 'expert':2})
    for idx,row in results.iterrows():
        sqlm.addTeamParticipant(db_session, row['Track'], row['Status'], row['Participant'], row['Email'], row['Department'], row['Year'], row['Level'])
    db_session.commit()
    participants = sqlm.getParticipants(db_session, None, None, year)
    db_session.close()
    engine.dispose()
    return """
                <html>
                <body>
           """ + participants.to_html() +"""
                <form action = "http://hkgmd1250276:59999/input" method = "GET">
         				<p><input type = "submit" value = "Submit scores" /></p>
     					 </form>          
                </body>
                </html>
           """
# get size of data frame
def allocateParticipants(df, teams, level_size):
    df = df[df['Status'] == 'New']
    if df is None: return []
    size = df.shape[0]
    if size == 0: return []

    print("Number of nominations" + str(size))

    tracks = set(df.loc[:, 'Track'])
    levels = set(df.loc[:, 'Level'])

    allocated = 0
    for track in tracks:
        for level in levels:
            current_team = 0
            current_dept = 0
            # Get number of participant in this track and level
            current_df = df[(df['Track'] == track) & (df['Level'] == level) & (df['Status'] == 'New')]
            if current_df is None or current_df.size == 0:
                continue
            max_level = current_df.count()[0]
            max_level = min(max_level, level_size[level] * len(teams[track]))

            rows = current_df.sample(n=max_level)
            for idx in rows.index:
                if current_team == len(teams[track]):
                    current_team = 0
                df.loc[idx, 'Status'] = teams[track][current_team]
                current_team += 1
    return df


@app.route('/save-nomination', methods=["POST"])
def saveNomination():

    result = request.form
    currentDT = datetime.datetime.now()
    str_curr_DT = str(currentDT)

    name = request.form['Name']
    email = request.form['email']
    dept = request.form['dept']
    year = request.form['year']
    track = request.form['track']
    level = request.form['level']
    reason = request.form['reason']
    # Creating sqllite database

    engine = create_engine('sqlite:///%s'%BLL_DB)
    Base.metadata.create_all(engine, checkfirst=True)
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    # Add Nominations
    nomination = sqlm.getNomination(db_session, track.lower(), email.lower(), year)
    if nomination is not None:
        return "Participant with %s email id is already added to the nomination ist for track %s year %s"%(nomination.participant.email, nomination.track.name, year)

    sqlm.addNomination(db_session, track.lower(), name, email.lower(), dept.lower(), year, level.lower(),
                       reason, "New")

    db_session.commit()
    nominations = sqlm.getTrackNomination(db_session, None, None, 2018)
    db_session.close()
    engine.dispose()
    return """
                <html>
                <body>
           """ + nominations.to_html() +"""
                <form action = "http://hkgmd1250276:59999/allocation-form" method = "GET">
         				<p><input type = "submit" value = "Allocate Teams" /></p>
     					 </form>          
                </body>
                </html>
           """


@app.route('/result1',methods = ['POST', 'GET'])
def result1():
   engine = create_engine('sqlite:///%s' % BLL_DB)
   Base.metadata.create_all(engine, checkfirst=True)
   DBSession = sessionmaker(bind=engine)
   db_session = DBSession()
   year = int(request.form['year'])

   if request.method == 'POST':

      result = request.form
      currentDT = datetime.datetime.now()
      str_curr_DT = str(currentDT)

      email = request.form['email']
      team = request.form['team']
      track = request.form['track']

      course = request.form['course']

      certificate = request.form['certificate']
      score = 0
      if(course =="Coursera"):
          score = 100
      elif(course =="ClassRoom"):
          score=10
      elif(course == "CodeAcademy"):
          score=40

      sqlm.addTeamScore(db_session, track.lower(), team, course.lower(), email.lower(), year, score,
                        certificate, str_curr_DT)
      db_session.commit()
      print('Score successfully added for %s'%email)

   team_scores = sqlm.getTeamScores(db_session, None, None, year)
   print(team_scores)
   db_session.close()
   engine.dispose()

   convertToHtmlRes2(team_scores, team, track, email)
   return render_template("showresult.html", result=result, str_curr_DT=str_curr_DT)

# This function will return the result
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':

      result = request.form
      currentDT = datetime.datetime.now()
      str_curr_DT = str(currentDT)

      Name = request.form['Name']
      email = request.form['email']
      team = request.form['team']
      designation = request.form['designation']
      track = request.form['track']
      course = request.form['course']
      certificate = request.form['certificate']
      score = 0
      if(course =="Coursera"):
          score = 100
      elif(course =="ClassRoom"):
          score=10
      elif(course == "CodeAcademy"):
          score=40

      rec = [Name,email,team,designation,track,course,certificate,score,str_curr_DT]
      write_csv(rec)

      convertToHtmlRes('leadboard.csv')
      return render_template("showresult.html",result = result,str_curr_DT=str_curr_DT )




# this function will write the employee record to file
def write_csv(emp_row):
    with open('leadboard.csv', mode='a') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(emp_row)


def write_csv_new(emp_row):
    with open('leadboard.csv', mode='a') as employee_file:
        fieldnames = ['Name','email','function' ,'designation','track','course','certificate','score']
        writer = csv.DictWriter(employee_file, fieldnames=fieldnames)
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(emp_row)


def convertToHtmlRes2(df,team, track, email):
    # new_df = df.sort_values(by='emp_score', ascending=False)
    # new_df = df.reset_index(drop=True)
    df2 = df.groupby(['Email', 'Participant']).sum()
    df3 = df2.sort_values(by='Score', ascending=False)
    df3.to_html(r"templates\leadboardMVP.html")
    df2 = df.groupby(['Team']).sum()
    df3 = df2.sort_values(by='Score', ascending=False)
    df3.to_html(r"templates\leadboardteam.html")
    if email is not None:
        print(email)
        df = df[(df['Email']==email.lower())]
    if team is not None:
        print(team)
        df = df[(df['Team'] == team)]
    if track is not None:
        print(track)
        df = df[(df['Track'] == track.lower())]
    df.to_html(r"templates\attendance.html")

def convertToHtmlRes(file):
    df = pd.read_csv(file)
    # new_df = df.sort_values(by='emp_score', ascending=False)
    # new_df = df.reset_index(drop=True)
    df2 = df.groupby(['email', 'Name']).sum()
    df3 = df2.sort_values(by='score', ascending=False)
    df3.to_html(r"templates\leadboardMVP.html")
    df2 = df.groupby(['team']).sum()
    df3 = df2.sort_values(by='score', ascending=False)
    df3.to_html(r"templates\leadboardteam.html")





def convertToHtml(file):
    df = pd.read_csv(file)
    # new_df = df.sort_values(by='emp_score', ascending=False)
    # new_df = df.reset_index(drop=True)
    df2 = df.groupby(['emp_id', 'emp_name']).sum()
    df3= df2.sort_values(by='emp_score', ascending=False)
    df3.to_html(r"templates\leadership.html")
'''
if __name__ == '__main__':
   app.run(debug=True,port=5000,host='45.12.140.85',threaded=True)
'''
if __name__ == "__main__":
    engine = create_engine('sqlite:///%s' % BLL_DB)
    Base.metadata.create_all(engine, checkfirst=True)
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    sqlm.addNomination(db_session, 'python', 'Aishwarya', 'aish@blk.com', 'bds', 2018, 'expert', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Bindu', 'bind@blk.com', 'fes', 2018, 'expert', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Aruna', 'arun@blk.com', 'apg', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Kapil', 'kapi@blk.com', 'bds', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Nisha', 'nish@blk.com', 'pag', 2018, 'expert', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Prashant', 'pras@blk.com', 'gio', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Deeptanshu', 'deep@blk.com', 'apg', 2018, 'expert', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'python', 'Dushyant', 'dush@blk.com', 'apg', 2018, 'intermediate', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Gagandeep', 'gaga@blk.com', 'apg', 2018, 'expert', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Praveen', 'prav@blk.com', 'bds', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Viral', 'vira@blk.com', 'fes', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Vrushabh', 'vrush@blk.com', 'gap', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Gaurav', 'gaur@blk.com', 'cso', 2018, 'beginner', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Shah Rukh', 'shah@blk.com', 'film', 2018, 'intermediate', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Aamir', 'aami@blk.com', 'film', 2018, 'intermediate', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Virat', 'vira@blk.com', 'cricket', 2018, 'expert', 'I am awesome', "New")
    sqlm.addNomination(db_session, 'r', 'Trump', 'trum@blk.com', 'us', 2018, 'expert', 'I am crazy', "New")
    db_session.commit()
    db_session.close()
    engine.dispose()


    # The 0.0.0.0 means accept requests on all network interfaces
    app.run(host=os.getenv('HOST', '0.0.0.0'),debug=True)
    print("Click http://hkgmd1250276:59999/login to start")
