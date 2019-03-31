import unittest
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

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


    def test_getpassword(self):
        PAGPUZZLE_DB = '../pagpuzzle3.db'

        engine = create_engine('sqlite:///%s' % PAGPUZZLE_DB)

        Base.metadata.create_all(engine, checkfirst=True)

        DBSession = sessionmaker(bind=engine)
        db_session = DBSession()
        username = "testuser3"
        sqlm.addUser(db_session, username, "t3")
        sqlm.addQuestions(db_session, "1", "3")
        sqlm.addQuestions(db_session, "2", "5")
        sqlm.addQuestions(db_session, "3", "8")
        sqlm.addQuestions(db_session, "4", "12")
        db_session.commit()
        print("Checking what all questions we do have.")
        quest = db_session.query(Questions).all()
        for q in quest:
            print(q.id,  q.ans_id)
        print("question bank check finished. ")

        tmp_pass = sqlm.getPassword(db_session, username)
        print("password retrived for username {} ".format(tmp_pass))


if __name__ == '__main__':
    # unittest.main()
    print("Hello Aishwarya")
