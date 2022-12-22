from expense import db
import json
import datetime
import calendar
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity
from expense.models import Expense, UsersModel
from flask import jsonify
from expense.expenseoperations.expenseHelper import serializeExpense, getTotalExpensesBetweenDates, expenseCategories, currentMonthCategoryExpense
from expense.expenseoperations.expenseHelper import getLastMonthEndDate, getAvgCategroryWiseExpense
from flask_restful import Resource, reqparse

# this class return 3 values (current month spending, todays spending, yesterdays spendings)

expenseInfo = reqparse.RequestParser()
expenseInfo.add_argument("date")
expenseInfo.add_argument("startDate")
expenseInfo.add_argument("endDate")

months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]


class MonthPreview(Resource):
    @jwt_required()
    def get(self):
        currentUserId = get_jwt_identity()
        current_user = UsersModel.query.filter_by(
            public_id=currentUserId).first()
        today = datetime.datetime.today().date()
        tommorow = today + datetime.timedelta(days=1)
        yesterday = today - datetime.timedelta(days=1)
        totalDays = calendar.monthrange(today.year, today.month)[1]
        firstDay = today.replace(day=1)
        lastDay = today.replace(day=totalDays)
        monthlyExpenses = getTotalExpensesBetweenDates(
            current_user.id, firstDay=firstDay, lastDay=lastDay)
        currentDayExpense = getTotalExpensesBetweenDates(
            current_user.id, today, tommorow)
        yesterDayExpense = getTotalExpensesBetweenDates(
            current_user.id, yesterday, today)
        return jsonify({"monthlyExpenses": monthlyExpenses, "currentDayExpense": currentDayExpense, "yesterDayExpense": yesterDayExpense})


class MonthwiseExpense(Resource):
    @jwt_required()
    def post(self):
        args = expenseInfo.parse_args()
        giveDate = datetime.datetime.strptime(
            args['date'], "%Y").date()
        endDate = giveDate.replace(day=31, month=12)
        currentUserId = get_jwt_identity()
        current_user = UsersModel.query.filter_by(
            public_id=currentUserId).first()
        monthlyexpense = db.session.query(func.strftime('%Y-%m', Expense.incurred_on), func.sum(Expense.amount)).filter(
            Expense.userId == current_user.id).filter(Expense.incurred_on >= giveDate).filter(Expense.incurred_on <= endDate).group_by(func.strftime('%Y-%m', Expense.incurred_on)).all()
        res = []
        monthAvailable = {}
        for t in monthlyexpense:
            recoredDict = {"x": t[0], "y": t[1]}
            monthAvailable[t[0]] = 1
            res.append(recoredDict)
        for i in range(1, 13):
            tempDate = giveDate.replace(month=i).strftime('%Y-%m')
            if tempDate not in monthAvailable:
                res.append({"x": tempDate, "y": 0})
        res = sorted(res, key=lambda i: i["x"])
        for i in range(0, 12):
            res[i]["x"] = months[i]
        return jsonify(res)


class MonthScatter(Resource):
    @jwt_required()
    def post(self):
        args = expenseInfo.parse_args()
        currentUserId = get_jwt_identity()
        current_user = UsersModel.query.filter_by(
            public_id=currentUserId).first()
        giveDate = datetime.datetime.strptime(
            args['date'], "%d-%m-%Y").date()
        totalDays = calendar.monthrange(giveDate.year, giveDate.month)[1]
        firstDay = giveDate.replace(day=1)
        lastDay = giveDate.replace(day=totalDays)
        monthlyScatter = db.session.query(func.strftime('%Y-%m-%d', Expense.incurred_on), func.sum(Expense.amount)).filter(
            Expense.userId == current_user.id).filter(Expense.incurred_on >= firstDay).filter(Expense.incurred_on <= lastDay).group_by(func.strftime('%Y-%m-%d', Expense.incurred_on)).all()
        res = []
        for t in monthlyScatter:
            resDict = {"x": t[0], "y": t[1]}
            res.append(resDict)
        return jsonify(res)


class CatergoryWiseExpense(Resource):
    @jwt_required()
    def get(self):
        currentUserId = get_jwt_identity()
        current_user = UsersModel.query.filter_by(
            public_id=currentUserId).first()
        currentDate = datetime.datetime.today().date()
        noofDaysInMonth = calendar.monthrange(
            currentDate.year, currentDate.month)[1]
        startDate = currentDate.replace(day=1)
        lastDate = currentDate.replace(day=noofDaysInMonth)
        currMonthExpense = currentMonthCategoryExpense(
            current_user.id, startDate, lastDate)
        lastMonthEndDate = getLastMonthEndDate()
        prevMonthAvgExpense = getAvgCategroryWiseExpense(
            current_user.id, lastMonthEndDate, currMonthExpense)
        return jsonify({"currMonthExpense": prevMonthAvgExpense})


class PieChart(Resource):
    @jwt_required()
    def post(self):
        currentUserId = get_jwt_identity()
        current_user = UsersModel.query.filter_by(
            public_id=currentUserId).first()
        args = expenseInfo.parse_args()
        startDate = datetime.datetime.strptime(
            args['startDate'], "%d-%m-%Y").date()
        endDate = datetime.datetime.strptime(
            args['endDate'], "%d-%m-%Y").date()
        pieChartExpense = db.session.query(Expense.category, func.sum(Expense.amount)).filter(
            Expense.userId == current_user.id).filter(Expense.incurred_on >= startDate).filter(Expense.incurred_on <= endDate).group_by(Expense.category).all()
        res = []
        for row in pieChartExpense:
            res.append({"x": row[0], "y": row[1]})
        return jsonify(res)
