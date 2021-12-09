import os
import unittest
from unittest.case import expectedFailure
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models
import datetime

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        new_user = models.User(username="test", email="test@test.com",
         password="sha256$C0xgBN1DOvgxFEB5$956c83621cf2de8ab6676ca73a31fb20d2e368327acf24a10490635671207b87")
        new_expense_type = models.ExpenseType(name="Rent/Utilities", color="#FAFFC7")
        db.session.add(new_user)
        db.session.add(new_expense_type)
        db.session.commit()
        new_expense = models.Expense(date=datetime.date.today(), amount=12.01, 
                                    user_id=1, expense_id=1)
        db.session.add(new_expense)
        db.session.commit()
        pass

    #chek the views
    def test_addloginroute(self):
        response = self.app.get('/login',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_addsinguproute(self):
        response = self.app.get('/signup',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_adddashboardroute(self):
        response = self.app.get('/dashboard',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_addexpenseroute(self):
        response = self.app.get('/addExpenses',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_addstatsroute(self):
        response = self.app.get('/statistics',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # check the username is currectly stored
    def test_returnusername(self):
        user = models.User.query.get(1)
        self.assertEqual('test', user.username)

    # check the total amount spend by user
    def test_usertotalamount(self):
        user = models.User.query.get(1)
        self.assertEqual(12.01, user.expenses[0].amount)

    # check the type of the expense
    def test_usertotalamount(self):
        user = models.User.query.get(1)
        expense_type = models.User.query.get(1)
        self.assertEqual(expense_type.id, user.expenses[0].expense_type.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()