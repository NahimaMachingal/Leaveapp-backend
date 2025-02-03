#api/serializers.py
from .models import Account, LeaveRequest
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type','password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = Account.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_user_type(self, value):
        if value not in dict(Account.USER_TYPE_CHOICES).keys():
            raise serializers.ValidationError("Invalid user type.")
        return value


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    start_date = serializers.DateField(format='%Y-%m-%d')  # Explicitly format start_date
    end_date = serializers.DateField(format='%Y-%m-%d')    # Explicitly format end_date
    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee_name', 'employee_email','leave_type', 'start_date', 'end_date', 'reason', 'status']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("User authentication is required.")

        validated_data["employee"] = request.user  # Assign logged-in user
        return super().create(validated_data)
