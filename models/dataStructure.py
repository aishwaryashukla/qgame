"""
HeadURL:  $HeadURL$
Last changed by:  $Author$
Last changed on:  $Date$

(c)  2018 BlackRock.  All rights reserved.

Description:

description
"""
__version__ = '$Revision$'

import pprint
from sqlalchemy import Column, ForeignKey, Integer, String, Float, and_
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dateutil import parser
import pandas as pd

Base = declarative_base()

class USERLOGIN(Base):
    __tablename__ = 'userlogin'
    id = Column(Integer, primary_key=True)
    userid = Column(String(250))
    password = Column(String(250))


class UserLoginDetails(Base):
    __tablename__ = 'userlogindetails'
    id = Column(Integer, primary_key=True)
    userid = Column(String(250), nullable=False)
    password = Column(String(250),nullable=False)

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    quest_id = Column(String(250), nullable=False)
    ans_id = Column(String(250),nullable=False)


class UserStatus(Base):
    __tablename__ = 'userstatus'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    quest_id = Column(String(250),nullable=False)
    level = Column(Integer, nullable=False)




class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(Department)


class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    year = Column(Integer, nullable=False)
    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship(Track)


class TrackNomination(Base):
    __tablename__ = 'track_nomination'
    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('track.id'))
    participant_id = Column(Integer, ForeignKey('participant.id'))
    year = Column(Integer, nullable=False)
    level = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    reason = Column(String(1000))
    track = relationship(Track)
    participant = relationship(Participant)


class TeamParticipant(Base):
    __tablename__ = 'team_participant'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    participant_id = Column(Integer, ForeignKey('participant.id'), nullable=False)
    level = Column(String(250))
    team = relationship(Team)
    participant = relationship(Participant)


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    max_score = Column(Float)


class TrackSession(Base):
    __tablename__ = 'track_session'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    track_id = Column(Integer, ForeignKey('track.id'))
    session_id = Column(Integer, ForeignKey('session.id'))
    track = relationship(Track)
    session = relationship(Session)


class TeamScore(Base):
    __tablename__ = 'team_score'
    id = Column(Integer, primary_key=True)
    team_participant_id = Column(Integer, ForeignKey('team_participant.id'))
    session_id = Column(Integer, ForeignKey('session.id'))
    score = Column(Float)
    certificate_link = Column(String(250))
    submitted = Column(DATETIME)
    team_participant = relationship(TeamParticipant)
    session = relationship(Session)

def getNomination(session, track_name, part_email, year):
    # Create track if it doesnot exist
    track = session.query(Track).filter(Track.name == track_name).first()
    if track is None:
        return None

    # Create participant if it doesnot exist
    part = session.query(Participant).filter(Participant.email == part_email).first()
    if part is None:
        return None

    conditions = []
    if track_name is not None:
        conditions.append(TrackNomination.track_id == track.id)
    if part_email is not None:
        conditions.append(TrackNomination.participant_id == part.id)
    if year is not None:
        conditions.append(TrackNomination.year == year)

    condition = and_(*conditions)
    nomination = session.query(TrackNomination).filter(condition).first()
    return nomination

def addUser(session, user_id, passwd):
    """

    :param session:
    :param user_id:
    :param password:
    :return:
    """
    userid = session.query(UserLoginDetails).filter(UserLoginDetails.userid == user_id).first()
    pprint.pprint(userid)
    if userid is None:
        userid = UserLoginDetails(userid=user_id,password=passwd)
        session.add(userid)

    else :
        return "User {} already exists".format(user_id)


def getPassword(session, user_id):
    print("getPassword :requesting user id {}".format(user_id))
    return session.query(UserLoginDetails).filter(UserLoginDetails.userid == user_id).first().password

def addQuestions(session, q_id, a_id):
   '''

   :param session:
   :param q_id:
   :param a_id:
   :return:
   '''
   qid = session.query(Questions).filter(Questions.quest_id == q_id).first()

   if qid is None:
       qid = Questions(quest_id = q_id, ans_id = a_id)
       session.add(qid)

   else :
        print("This question already exists {}".format(q_id))
        return "Question {} already exists".format(q_id)

def getAnswer(session, q_id):
    print("getAnswer: {}".format(q_id))
    # quest = session.query(Questions).all()
    # for q in quest:
    #     print(q.id, q.quest_id, q.ans_id)
    if session is None:
        print("Got NONE as session, Please check. ")
    else:

        ans = session.query(Questions).filter(Questions.quest_id == q_id).first()
        if ans is not None:
            return ans.ans_id
        else:
            print("No Answer for this question.  ")



def addUserStatus(session, u_id, q_id, lvl):
   '''
   :param session:
   :param u_id:
   :param q_id:
   :param lvl:
   :return:
   '''

   ustatus = session.query(UserStatus).filter(UserStatus.user_id == u_id).first()
   print("adding user status {} {} {}".format(u_id, q_id, lvl  ))
   if ustatus is None:
       ustatus = UserStatus(user_id = u_id,quest_id = q_id, level=lvl)
       session.add(ustatus)
       # session.commit()
       print("Recode updated user_di: {} quest_id: {} level: {}".format(u_id, q_id, lvl))
       return True

   else :
       print("User {} already exists in UserStatus Table, please run update query".format(u_id))
       return False

def updateUserStatus(session, u_id, q_id, lvl):
   '''
   :param session:
   :param u_id:
   :param q_id:
   :param lvl:
   :return:
   '''
   try:

       print("updateUserStatus: ",u_id, q_id, lvl)
       ustatus = session.query(UserStatus).filter(UserStatus.user_id == u_id).\
           update({"level":lvl, "quest_id":q_id})

       if ustatus is None:
           print(" Record does not exists in table UserStatus for user {}".format(u_id))
           return False
       else :
           # ustatus = UserStatus(user_id=u_id, quest_id=q_id, level=lvl)
           # ustatus.level = lvl
           # ustatus.quest_id = q_id
           session.commit()

           # return True
   except:
       print("something wrong heppen in updateUserSatatus function while updating the record. ")

   userStatus = session.query(UserStatus).all()
   print("updateUserStatus")
   for q in userStatus:
       print(q.id, q.user_id, q.quest_id, q.level)


def getUserStatusLevel(session, u_id):
    return session.query(UserStatus).filter(UserStatus.user_id == u_id).first().level

def getUserStatus(db_session):
    '''

    :param session:
    :return:
    '''
    ustatus = db_session.query(UserStatus).all()
    pd_list = []
    for us in ustatus:
        pd_list.append([us.user_id, us.quest_id])

    df = pd.DataFrame(pd_list)
    df.columns = ['User', 'Level']
    return df
def addNomination(session, track_name, part_name, part_email, part_dept, year, level, reason, status):
    """
    add a nomination. Tracks,departments and participants will be created if they don't exist already. Participant email should be unique
    :params: This is the set of parameters specified
    """
    # Create track if it doesnot exist
    track = session.query(Track).filter(Track.name == track_name).first()
    if track is None:
        track = Track(name=track_name)
        session.add(track)

    # Create dept if it doesnot exist
    dept = session.query(Department).filter(Department.name == part_dept).first()
    if dept is None:
        dept = Department(name=part_dept)
        session.add(dept)

    # Create participant if it doesnot exist
    part = session.query(Participant).filter(Participant.email == part_email).first()
    if part is None:
        part = Participant(name=part_name, email=part_email, department=dept)
        session.add(part)

    conditions = []
    if track_name is not None:
        conditions.append(TrackNomination.track_id == track.id)
    if part_email is not None:
        conditions.append(TrackNomination.participant_id == part.id)
    if year is not None:
        conditions.append(TrackNomination.year == year)

    condition = and_(*conditions)
    nomination = session.query(TrackNomination).filter(condition).first()
    if nomination is None:
        nomination = TrackNomination(track=track, participant=part, year=year, level=level, status=status, reason=reason)
        session.add(nomination)
    else:
        nomination.level = level
        nomination.status = status
        nomination.reason = reason
        session.add(nomination)



def getTrack(session, track_name):
    return session.query(Track).filter(Track.name == track_name).first()


def getParticipant(session, part_email):
    return session.query(Participant).filter(Participant.email == part_email).first()


def getTeam(session, track_id, team_name, year):
    # Create team if it doesnot exist
    conditions = []
    if track_id is not None:
        conditions.append(Team.track_id == track_id)
    if team_name is not None:
        conditions.append(Team.name == team_name)
    if year is not None:
        conditions.append(Team.year == year)
    team = session.query(Team).filter(and_(*conditions)).first()
    return team


def getTeamParticipant(session, team_id, part_id):
    # Create team if it doesnot exist
    conditions = []
    if team_id is not None:
        conditions.append(TeamParticipant.team_id == team_id)
    if part_id is not None:
        conditions.append(TeamParticipant.participant_id == part_id)
    team_participant = session.query(TeamParticipant).filter(and_(*conditions)).first()
    return team_participant

def getParticipants(session, team_name, part_email, year):
    team = getTeam(session, None, team_name, year)
    part = getParticipant(session, part_email)

    conditions = []
    if team_name is not None:
        conditions.append(TeamParticipant.team_id == team_name)
    if part_email is not None:
        conditions.append(TeamParticipant.participant_id == part_email)
    team_participants= session.query(TeamParticipant).filter(and_(*conditions)).all()

    pd_list = []
    for team_participant in team_participants:
        pd_list.append([team_participant.team.track.name, team_participant.team.name,
                       team_participant.team.year, team_participant.participant.department.name,
                        team_participant.participant.name,team_participant.participant.email, team_participant.level])

    df = pd.DataFrame(pd_list)
    df.columns = ['Track', 'Team', 'Year', 'Department', 'Participant', 'Email', 'Level']
    return df


def getTrackNomination(session, track_name, part_email, year):
    track = getTrack(session, track_name)
    part = getParticipant(session, part_email)

    conditions = []
    if track_name is not None:
        conditions.append(TrackNomination.track_id == track.id)
    if part_email is not None:
        conditions.append(TrackNomination.participant_id == part.id)
    if year is not None:
        conditions.append(TrackNomination.year == year)

    nominations = session.query(TrackNomination).filter((conditions))
    pd_list = []
    for nomination in nominations:
        pd_list.append([nomination.track.name, nomination.participant.name, nomination.participant.email, nomination.participant.department.name, nomination.level, nomination.year, nomination.status, nomination.reason])
    df = pd.DataFrame(pd_list)
    df.columns = ['Track', 'Participant', 'Email', 'Department', 'Level', 'Year', 'Status', 'Reason']
    return df


def getTeamScores(session, team_name, part_email, year, course_name=None):
    team = getTeam(session, None, team_name, year)
    part = getParticipant(session, part_email)
    course = None
    if course_name is not None:
        course = session.query(Session).filter(Session.name == course_name)

    tp_query = session.query(TeamParticipant).subquery()
    conditions = []
    if team_name is not None:
        conditions.append(tp_query.c.team_id == team.id)
    if part_email is not None:
        conditions.append(tp_query.c.participant_id == part.id)
    if course_name is not None:
        conditions.append(TeamScore.session_id == course.id)
    scores = session.query(TeamScore).join(
        tp_query, TeamScore.team_participant_id == tp_query.c.id).filter(and_(*conditions))

    pd_list = []
    for score in scores:
        pd_list.append([score.team_participant.team.track.name, score.team_participant.team.name,
                       score.team_participant.participant.name,score.team_participant.participant.email,
                       score.session.name, score.score, score.certificate_link, score.submitted])

    df = pd.DataFrame(pd_list)
    df.columns = ['Track', 'Team', 'Participant', 'Email', 'Course', 'Score', 'Certification Link', 'Submitted']
    return df


def addTeamParticipant(session, track_name, team_name, part_name, part_email, part_dept, year, level):
    """
    add a nomination. Tracks,departments and participants will be created if they don't exist already. Participant email should be unique
    :params: This is the set of parameters specified
    """

    # Create track if it doesnot exist
    track = session.query(Track).filter(Track.name == track_name).first()
    if track is None:
        track = Track(name=track_name)
        session.add(track)

    # Create team if it doesnot exist
    team = getTeam(session, track.id, team_name, year)
    if team is None:
        team = Team(name=team_name, track=track, year=year)
        session.add(team)

    # Create dept if it doesnot exist
    dept = session.query(Department).filter(Department.name == part_dept).first()
    if dept is None:
        dept = Department(name=part_dept)
        session.add(dept)

    # Create participant if it doesnot exist
    part = session.query(Participant).filter(Participant.email == part_email).first()
    if part is None:
        part = Participant(name=part_name, email=part_email, department=dept)
        session.add(part)

    # Find if a participation exists already
    conditions = []
    if team_name is not None:
        conditions.append(TeamParticipant.team_id == team.id)
    if part_email is not None:
        conditions.append(TeamParticipant.participant_id == part.id)

    condition = and_(*conditions)
    participation = session.query(TeamParticipant).filter(condition).first()
    if participation is None:
        participation = TeamParticipant(team=team, participant=part, level=level)
        session.add(participation)
    else:
        participation.level = level
        session.add(participation)


def addTeamScore(session, track_name, team_name, course_name, part_email, year, score, certificate_link, submitted):
    # Get track if it exists
    track = session.query(Track).filter(Track.name == track_name).first()
    if track is None:
        raise ValueError("Cannot find track name %s", track_name)

    # Get team if it exists
    team = getTeam(session, track.id, team_name, year)
    if team is None:
        raise ValueError("Cannot find team name %s" % team_name)

    # Get participant if it exists
    part = session.query(Participant).filter(Participant.email == part_email).first()
    if part is None:
        raise ValueError("Cannot find participant by email %s" % part_email)

    course = session.query(Session).filter(Session.name == course_name).first()
    if course is None:
        course = Session(name=course_name)
        session.add(course)
        track_course = TrackSession(track=track, session=course, year=year)
        session.add(track_course)

    team_participant = getTeamParticipant(session, team.id, part.id)
    if team_participant is None:
        raise ValueError("%s is not part of team %s for year %d" % (part.name, team.name, team.year))

    # Find if a score exists already
    conditions = []
    if team_name is not None and part_email is not None:
        conditions.append(TeamScore.team_participant_id == team_participant.id)
    if course_name is not None:
        conditions.append(TeamScore.session_id == course.id)
    team_score = session.query(TeamScore).filter(and_(*conditions)).first()
    sub_dt = parser.parse(submitted).date()
    if team_score is None:
        team_score = TeamScore(team_participant=team_participant, session=course, score=score, certificate_link=certificate_link, submitted=sub_dt)
        session.add(team_score)
    else:
        team_score.score = score
        team_score.certificate_link = certificate_link
        team_score.submitted = sub_dt
        session.add(team_score)
