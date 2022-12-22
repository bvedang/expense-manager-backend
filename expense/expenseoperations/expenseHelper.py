from expense.models import Expense
from datetime import datetime
import datetime
from expense import db
from sqlalchemy import func
import calendar

expenseCategories = ["Entertainment", "Food & Drink", "Home",
                     "Life", "Transportation", "Uncategorized", "Utilities"]


def serializeExpense(expense: Expense) -> dict:
    expenseDict = {
        'id': expense.id, 'userId': expense.userId,
        'title': expense.title, 'amount': expense.amount,
        'category': expense.category,
        'incurred_on': expense.incurred_on.strftime("%Y/%m/%d"), 'notes': expense.notes,
        'updated_at': expense.updated_at, }
    return expenseDict


def getTotalExpensesBetweenDates(userId: int, firstDay: datetime, lastDay: datetime) -> int:
    """This function take 3 paramter 
    1) currentUserId
    2) fromDate or firstDay
    3) toDate or lastDay

    Calculates the total expenditure between fromDate and toDate """
    expenseSum = 0
    result = Expense.query.filter_by(userId=userId).filter(Expense.incurred_on >= firstDay).filter(
        Expense.incurred_on < lastDay).all()
    for expense in result:
        expenseSum += expense.amount
    return expenseSum


def currentMonthCategoryExpense(userId: int, startDate: datetime, endDate: datetime) -> list:
    categoryExpense = db.session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.userId == userId).filter(
        Expense.incurred_on >= startDate).filter(Expense.incurred_on <= endDate).group_by(Expense.category).all()
    res = {}
    for row in categoryExpense:
        res[row[0]] = row[1]
    finalres = []
    for expenseCategory in expenseCategories:
        currentMonthCE = {}
        if expenseCategory not in res:
            currentMonthCE["category"] = expenseCategory
            currentMonthCE["total"] = 0
        else:
            currentMonthCE["category"] = expenseCategory
            currentMonthCE["total"] = res[expenseCategory]
        finalres.append(currentMonthCE)
    return finalres


def getAvgCategroryWiseExpense(userId: int, lastMonthEndDate: datetime.datetime, prevRes:list) -> list:
    avgbyCategories = db.session.query(Expense.category, func.strftime('%Y-%m', Expense.incurred_on), func.sum(Expense.amount)).filter(Expense.userId == userId).filter(Expense.incurred_on <=
                                                                                                                                                                        lastMonthEndDate).group_by(Expense.category, func.strftime('%Y-%m', Expense.incurred_on)).all()
    res = {}
    for row in avgbyCategories:
        if row[0] not in res:
            res[row[0]] = {"value": row[2], "count": 1}
        else:
            res[row[0]]["value"] += row[2]
            res[row[0]]["count"] += 1
    ctr = 0 
    for expenseCategory in expenseCategories:
        if expenseCategory not in res:
            prevRes[ctr]["avg"] = 0

        else:
            prevRes[ctr]["avg"]  = res[expenseCategory]["value"] / \
                res[expenseCategory]["count"]
        ctr += 1
    return prevRes


def getLastMonthEndDate() -> datetime:
    currentDate = datetime.datetime.today().date()
    lastMonth = 0
    lastYear = currentDate.year
    if currentDate.month == 1:
        lastMonth = currentDate.month-1 if currentDate.month > 1 else 12
        lastYear = currentDate.year-1
    else:
        lastMonth = currentDate.month-1 if currentDate.month > 1 else 12
    noofDaysInMonth = calendar.monthrange(lastYear, lastMonth)[1]
    lastDate = datetime.datetime(
        lastYear, lastMonth, noofDaysInMonth).date()
    return lastDate
