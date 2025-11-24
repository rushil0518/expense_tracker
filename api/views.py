from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Category, Expense, Budget
from .serializers import CategorySerializer, ExpenseSerializer, BudgetSerializer, RegisterSerializer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_category_colors(uid):
    # Fetch both global categories (user_id=None) and user categories
    cats = Category.objects(user_id__in=[None, uid])
    color_map = {c.name: (c.color or "#999999") for c in cats}
    return color_map



# Create your views here.
class TestAuthView(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        return Response({"message": "You are logged in"})

class CategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        
        uid = str(request.user.id)

        global_cats = Category.objects(user_id=None)

         # user categories
        user_cats = Category.objects(user_id=uid)

    # merge but avoid duplicates by name
        merged = {}
        for cat in global_cats:
           merged[cat.name] = cat

        for cat in user_cats:
           merged[cat.name] = cat  # user overrides global if same name

    # return as list
        final = [
        {"id": str(cat.id), "name": cat.name, "color": cat.color}
        for cat in merged.values()
    ]

        return Response(final)

        # # Fetch global categories (user_id=None) + user categories
        # categories = Category.objects.filter(
        #     __raw__={
        #         "$or": [
        #             {"user_id": None},
        #             {"user_id": uid}
        #         ]
        #     }
        # )

        # data = [c.to_dict() for c in categories]
        # return Response(data)
    def post(self, request):
        uid = str(request.user.id)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Check duplicate category for this user
            exists = Category.objects(
                name=data["name"],
                user_id=uid
            ).first()

            if exists:
                return Response({"detail": "Category already exists"}, status=400)

            # Create category
            cat = Category(
                name=data["name"],
                user_id=uid,
                color=data.get("color", "#4BC0C0"),
                icon=data.get("icon", "")
            )
            cat.save()

            return Response(cat.to_dict(), status=201)

        return Response(serializer.errors, status=400)

class ExpenseListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uid = str(request.user.id)

        expenses = Expense.objects(user_id=uid).order_by("-date")

        data = [e.to_dict() for e in expenses]
        return Response(data)
    
    def post(self, request):
        uid = str(request.user.id)

        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Validate category exists (global or user)
            category_name = data["category"]

            valid = Category.objects.filter(
                __raw__={
                    "$or": [
                        {"name": category_name, "user_id": None},
                        {"name": category_name, "user_id": uid}
                    ]
                }
            ).first()

            if not valid:
                return Response({"detail": "Invalid category"}, status=400)

            exp = Expense(
                user_id=uid,
                category=data["category"],
                amount=data["amount"],
                date=data.get("date"),
                note=data.get("note", ""),
                tags=data.get("tags", [])
            )
            exp.save()

            return Response(exp.to_dict(), status=201)

        return Response(serializer.errors, status=400)
    

class ExpenseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, uid):
        try:
            return Expense.objects.get(id=pk, user_id=uid)
        except:
            return None
        
    def get(self, request, pk):
        uid = str(request.user.id)
        exp = self.get_object(pk, uid)

        if not exp:
            return Response({"detail": "Not found"}, status=404)

        return Response(exp.to_dict())
    
    def put(self, request, pk):
        uid = str(request.user.id)
        exp = self.get_object(pk, uid)

        if not exp:
            return Response({"detail": "Not found"}, status=404)

        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            exp.category = data["category"]
            exp.amount = data["amount"]
            exp.date = data.get("date", exp.date)
            exp.note = data.get("note", "")
            exp.tags = data.get("tags", [])

            exp.save()

            return Response(exp.to_dict())

        return Response(serializer.errors, status=400)
    def delete(self, request, pk):
        uid = str(request.user.id)
        exp = self.get_object(pk, uid)

        if not exp:
            return Response({"detail": "Not found"}, status=404)

        exp.delete()
        return Response(status=204)
    
# class BudgetListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         uid = str(request.user.id)
#         budgets = Budget.objects(user_id=uid)

#         data = [b.to_dict() for b in budgets]
#         return Response(data)
    
#     def post(self, request):
#         uid = str(request.user.id)

#         serializer = BudgetSerializer(data=request.data)
#         if serializer.is_valid():
#             d = serializer.validated_data

#             budget = Budget(
#                 user_id=uid,
#                 category=d.get("category"),
#                 limit=d["limit"],
#                 month=d["month"]
#             )
#             budget.save()

#             return Response(budget.to_dict(), status=201)

#         return Response(serializer.errors, status=400)

# class BudgetDetailView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self, pk, uid):
#         try:
#             return Budget.objects.get(id=pk, user_id=uid)
#         except:
#             return None
    
#     def put(self, request, pk):
#         uid = str(request.user.id)
#         budget = self.get_object(pk, uid)

#         if not budget:
#             return Response({"detail": "Not found"}, status=404)

#         serializer = BudgetSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data

#             budget.category = data.get("category", budget.category)
#             budget.limit = data.get("limit", budget.limit)
#             budget.month = data.get("month", budget.month)
#             budget.save()

#             return Response(budget.to_dict())

#         return Response(serializer.errors, status=400)
    
#     def delete(self, request, pk):
#         uid = str(request.user.id)
#         budget = self.get_object(pk, uid)

#         if not budget:
#             return Response({"detail": "Not found"}, status=404)

#         budget.delete()
#         return Response(status=204)

class BudgetListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uid = str(request.user.id)
        month_key = datetime.now().strftime("%Y-%m")

        budget = Budget.objects(user_id=uid, month=month_key).first()
        total_budget = budget.amount if budget else 0

        start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        expenses = Expense.objects(user_id=uid, date__gte=start)
        total_spent = sum(e.amount for e in expenses)

        return Response({
            "total_budget": total_budget,
            "total_spent": total_spent
        })

    def post(self, request):
        uid = str(request.user.id)
        serializer = BudgetSerializer(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            month_key = datetime.now().strftime("%Y-%m")

            budget = Budget.objects(user_id=uid, month=month_key).first()

            if budget:
                budget.amount = amount
                budget.save()
                return Response({"message": "Budget updated"})

            Budget(user_id=uid, amount=amount, month=month_key).save()
            return Response({"message": "Budget created"})

        return Response(serializer.errors, status=400)


    
# class CategoryPieChart(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         uid = str(request.user.id)
#         month = request.GET.get("month")

#         # Default = current month
#         if not month:
#             month = datetime.now().strftime("%Y-%m")

#         # Filter expenses for the selected month
#         expenses = Expense.objects(
#             user_id=uid,
#             date__gte=datetime.strptime(month, "%Y-%m"),
#             date__lt=(datetime.strptime(month, "%Y-%m") + relativedelta(months=1))
#         )

#         if not expenses:
#             return Response({"detail": "No expenses for this month"}, status=400)

#         category_totals = {}
#         for exp in expenses:
#             category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

#         labels = list(category_totals.keys())
#         values = list(category_totals.values())

#         plt.figure(figsize=(6, 6))
#         plt.pie(values, labels=labels, autopct="%1.1f%%")
#         plt.title(f"Category-wise Spending ({month})")

#         filename = f"pie_{uid}_{int(datetime.now().timestamp())}.png"
#         filepath = os.path.join(settings.MEDIA_ROOT, "charts")
#         os.makedirs(filepath, exist_ok=True)
#         plt.savefig(os.path.join(filepath, filename), bbox_inches="tight")
#         plt.close()

#         chart_url = request.build_absolute_uri(settings.MEDIA_URL + "charts/" + filename)
#         return Response({"chart_url": chart_url})

    
# class MonthlyBarChart(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         uid = str(request.user.id)

#         expenses = Expense.objects(user_id=uid)

#         monthly_totals = {}

#         for exp in expenses:
#             month = exp.date.strftime("%Y-%m")
#             monthly_totals[month] = monthly_totals.get(month, 0) + exp.amount

#         if not monthly_totals:
#             return Response({"detail": "No data available"}, status=400)

#         # Sort by month
#         labels = sorted(monthly_totals.keys())
#         values = [monthly_totals[m] for m in labels]

#         plt.figure(figsize=(10, 5))
#         plt.bar(labels, values)
#         plt.xticks(rotation=45)
#         plt.title("Monthly Spending (Year Overview)")
#         plt.xlabel("Month")
#         plt.ylabel("Amount")

#         filename = f"bar_{uid}_{int(datetime.now().timestamp())}.png"
#         filepath = os.path.join(settings.MEDIA_ROOT, "charts")
#         os.makedirs(filepath, exist_ok=True)

#         plt.savefig(os.path.join(filepath, filename), bbox_inches="tight")
#         plt.close()

#         chart_url = request.build_absolute_uri(settings.MEDIA_URL + "charts/" + filename)
#         return Response({"chart_url": chart_url})

# class DailyTrendChart(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         uid = str(request.user.id)
#         month = request.GET.get("month")

#         if not month:
#             month = datetime.now().strftime("%Y-%m")

#         start = datetime.strptime(month, "%Y-%m")
#         end = start + relativedelta(months=1)

#         expenses = Expense.objects(
#             user_id=uid,
#             date__gte=start,
#             date__lt=end
#         )

#         if not expenses:
#             return Response({"detail": "No data for this month"}, status=400)

#         daily_totals = {}

#         for exp in expenses:
#             day = exp.date.strftime("%d")
#             daily_totals[day] = daily_totals.get(day, 0) + exp.amount

#         labels = sorted(daily_totals.keys())
#         values = [daily_totals[d] for d in labels]

#         plt.figure(figsize=(10, 5))
#         plt.plot(labels, values, marker='o')
#         plt.title(f"Daily Spending Trend ({month})")
#         plt.xlabel("Day")
#         plt.ylabel("Amount")

#         filename = f"trend_{uid}_{int(datetime.now().timestamp())}.png"
#         filepath = os.path.join(settings.MEDIA_ROOT, "charts")
#         os.makedirs(filepath, exist_ok=True)
#         plt.savefig(os.path.join(filepath, filename), bbox_inches="tight")
#         plt.close()

#         chart_url = request.build_absolute_uri(settings.MEDIA_URL + "charts/" + filename)
#         return Response({"chart_url": chart_url})

# class CategoryMonthlyChart(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         uid = str(request.user.id)
#         month = request.GET.get("month")

#         if not month:
#             month = datetime.now().strftime("%Y-%m")

#         start = datetime.strptime(month, "%Y-%m")
#         end = start + relativedelta(months=1)

#         expenses = Expense.objects(
#             user_id=uid,
#             date__gte=start,
#             date__lt=end
#         )

#         category_totals = {}

#         for exp in expenses:
#             category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

#         if not category_totals:
#             return Response({"detail": "No expenses found for this month"}, status=400)

#         labels = list(category_totals.keys())
#         values = list(category_totals.values())

#         plt.figure(figsize=(10, 5))
#         plt.bar(labels, values)
#         plt.title(f"Category-wise Spending for {month}")
#         plt.xlabel("Category")
#         plt.ylabel("Amount")
#         plt.xticks(rotation=45)

#         filename = f"category_month_{uid}_{int(datetime.now().timestamp())}.png"
#         filepath = os.path.join(settings.MEDIA_ROOT, "charts")
#         os.makedirs(filepath, exist_ok=True)
#         plt.savefig(os.path.join(filepath, filename), bbox_inches="tight")
#         plt.close()

#         chart_url = request.build_absolute_uri(settings.MEDIA_URL + "charts/" + filename)
#         return Response({"chart_url": chart_url})

    
class RegisterView(APIView):
    permission_classes = []  # public endpoint

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# CATEGORY DETAIL (GET single, PUT update, DELETE)
class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        cat = Category.objects(id=id).first()
        if not cat:
            return Response({"error": "Category not found"}, status=404)

        return Response({
            "id": str(cat.id),
            "name": cat.name,
            "color": cat.color,
            "user_id": cat.user_id
        })

    def put(self, request, id):
        cat = Category.objects(id=id).first()
        if not cat:
            return Response({"error": "Category not found"}, status=404)

        # Only user-defined categories can be edited
        if cat.user_id is None:
            return Response({"error": "Default categories cannot be edited"}, status=400)

        data = request.data

        cat.name = data.get("name", cat.name)
        cat.color = data.get("color", cat.color)
        cat.save()

        return Response({"message": "Category updated"}, status=200)

    def delete(self, request, id):
        cat = Category.objects(id=id).first()
        if not cat:
            return Response({"error": "Category not found"}, status=404)

        # Default categories cannot be deleted
        if cat.user_id is None:
            return Response({"error": "Default categories cannot be deleted"}, status=400)

        cat.delete()
        return Response({"message": "Category deleted"})

    
class CategoryPieChart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uid = str(request.user.id)
        month = request.GET.get("month") or datetime.now().strftime("%Y-%m")

        try:
            start = datetime.strptime(month, "%Y-%m")
        except ValueError:
            return Response({"error": "month must be YYYY-MM"}, status=400)

        end = start + relativedelta(months=1)

        expenses = Expense.objects(user_id=uid, date__gte=start, date__lt=end)

        category_totals = {}
        for e in expenses:
            cat = e.category or "Uncategorized"
            category_totals[cat] = category_totals.get(cat, 0) + float(e.amount)

        labels = list(category_totals.keys())
        values = [category_totals[l] for l in labels]

        if not labels:
            return Response({"labels": [], "values": [], "colors": [], "message": "No expenses for this month"})

        # fetch colors from category db
        color_map = get_category_colors(uid)
        colors = [color_map.get(cat, "#999999") for cat in labels]

        return Response({
            "labels": labels,
            "values": values,
            "colors": colors,
            "title": f"Category-wise Spending ({month})"
        })

        
class CategoryMonthlyChart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uid = str(request.user.id)
        month = request.GET.get("month") or datetime.now().strftime("%Y-%m")

        try:
            start = datetime.strptime(month, "%Y-%m")
        except ValueError:
            return Response({"error": "month must be YYYY-MM"}, status=400)

        end = start + relativedelta(months=1)

        expenses = Expense.objects(user_id=uid, date__gte=start, date__lt=end)

        totals = {}
        for e in expenses:
            cat = e.category or "Uncategorized"
            totals[cat] = totals.get(cat, 0) + float(e.amount)

        labels = list(totals.keys())
        values = [totals[l] for l in labels]

        if not labels:
            return Response({"labels": [], "values": [], "colors": [], "message": "No expenses for this month"})

        # apply category colors
        color_map = get_category_colors(uid)
        colors = [color_map.get(cat, "#999999") for cat in labels]

        return Response({
            "labels": labels,
            "values": values,
            "colors": colors,
            "title": f"Category totals for {month}"
        })


class DailyTrendChart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uid = str(request.user.id)
        month = request.GET.get("month") or datetime.now().strftime("%Y-%m")

        try:
            start = datetime.strptime(month, "%Y-%m")
        except ValueError:
            return Response({"error": "month must be YYYY-MM"}, status=400)

        end = start + relativedelta(months=1)

        expenses = Expense.objects(user_id=uid, date__gte=start, date__lt=end)

        daily = {}
        for e in expenses:
            day = e.date.strftime("%d")
            daily[day] = daily.get(day, 0) + float(e.amount)

        if not daily:
            return Response({"labels": [], "values": [], "message": "No expenses for this month"})

        labels = sorted(daily.keys(), key=lambda x: int(x))
        values = [daily[d] for d in labels]

        return Response({
            "labels": labels,
            "values": values,
            "title": f"Daily spending trend ({month})"
        })

class MonthlyBarChart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uid = str(request.user.id)
        expenses = Expense.objects(user_id=uid)

        monthly = {}
        for e in expenses:
            m = e.date.strftime("%Y-%m")
            monthly[m] = monthly.get(m, 0) + float(e.amount)

        if not monthly:
            return Response({"labels": [], "values": [], "message": "No data available"})

        labels = sorted(monthly.keys())
        values = [monthly[m] for m in labels]

        return Response({
            "labels": labels,
            "values": values,
            "title": "Month-over-Month Spending"
        })
