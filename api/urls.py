from django.urls import path
from .views import (
    CategoryListCreateView,
    ExpenseListCreateView,
    ExpenseDetailView,
    BudgetListCreateView,
    TestAuthView,
    # BudgetDetailView,
    CategoryPieChart,
    MonthlyBarChart,
    DailyTrendChart,
    CategoryMonthlyChart,
    RegisterView,
    CategoryDetail,
)


urlpatterns = [
    path("test-auth/", TestAuthView.as_view()),
    path("categories/", CategoryListCreateView.as_view()),
    path("categories/<id>/", CategoryDetail.as_view()),
    path("expenses/", ExpenseListCreateView.as_view()),
    path("expenses/<str:pk>/", ExpenseDetailView.as_view()),
    path("budgets/", BudgetListCreateView.as_view()),
    # path("budgets/<str:pk>/", BudgetDetailView.as_view()),
    path("analytics/category-pie/", CategoryPieChart.as_view()),
    path("analytics/monthly-bar/", MonthlyBarChart.as_view()),
    path("analytics/daily-trend/", DailyTrendChart.as_view()),
    path("analytics/category-monthly/", CategoryMonthlyChart.as_view()),
    path("register/", RegisterView.as_view()),
]