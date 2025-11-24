from rest_framework import serializers
from django.contrib.auth.models import User

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    user_id = serializers.CharField(required=False, allow_null=True)
    color = serializers.CharField(required=False, allow_blank=True)
    icon = serializers.CharField(required=False, allow_blank=True)

class ExpenseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    category = serializers.CharField()
    amount = serializers.FloatField()
    date = serializers.DateTimeField(required=False)
    note = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

# class BudgetSerializer(serializers.Serializer):
#     id = serializers.CharField(read_only=True)
#     category = serializers.CharField(required=False, allow_null=True)
#     limit = serializers.FloatField()
#     month = serializers.CharField()  

class BudgetSerializer(serializers.Serializer):
    amount = serializers.FloatField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user