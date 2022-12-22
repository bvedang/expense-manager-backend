from expense import api
from expense.users.users import CreateNewUser, UserAuth,GetallUser,CurrentUser
from expense.expenseoperations.expenseManager import UserExpense, FilterdUserExpenses
from expense.expenseoperations.expensePreviewReports import MonthPreview,MonthwiseExpense, CatergoryWiseExpense,MonthScatter,PieChart

def init_routes():
    api.add_resource(CreateNewUser, "/user/create_user")
    api.add_resource(UserAuth,"/user/login")
    api.add_resource(GetallUser,"/user/allUsers")
    api.add_resource(CurrentUser,"/user/get_current_user")
    api.add_resource(UserExpense, "/user/expenses")
    api.add_resource(FilterdUserExpenses,"/user/filteredExpenses")
    api.add_resource(MonthPreview,"/user/monthlyPreview")
    api.add_resource(MonthwiseExpense,"/user/yearlyBar")
    api.add_resource(CatergoryWiseExpense,"/user/monthlyCategoryExpense")
    api.add_resource(MonthScatter,"/user/monthlyScatter")
    api.add_resource(PieChart,"/user/pieChart")


    