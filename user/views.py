from django.shortcuts import render
from .serializers import AccountSerializer, LeaveRequestSerializer
from rest_framework.views import APIView
from .models import Account, LeaveRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            user_type = serializer.validated_data.get('user_type', 'employee')
            user = Account.objects.create_user(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                password=password,
                last_name=serializer.validated_data['last_name'],
                user_type=user_type,
                
            )

            
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = Account.objects.filter(email=email).first()
        # Check if user exists
        if user is None:
            return Response(
                {'error': 'Incorrect username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )        
        # Check if the password is correct
        if not user.check_password(password):
            return Response(
                {'error': 'Incorrect username or password'},
                status=status.HTTP_401_UNAUTHORIZED            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=200)

class LeaveRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type == 'manager':  # If the logged-in user is a manager
            leave_requests = LeaveRequest.objects.all()  # Show all requests
        else:
            leave_requests = LeaveRequest.objects.filter(employee=request.user)  # Show only their own requests

        serializer = LeaveRequestSerializer(leave_requests, many=True)
        print(serializer.data)  # Debugging: Check if pending requests are included
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        today = date.today()
        max_future_date = today + timedelta(days=45)  # Max 45 days into the future
        
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        
        if not start_date or not end_date:
            return Response({"error": "Start date and end date are required"}, status=status.HTTP_400_BAD_REQUEST)

        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        if start_date < today:
            return Response({"error": "Start date cannot be in the past"}, status=status.HTTP_400_BAD_REQUEST)

        if end_date < start_date:
            return Response({"error": "End date must be after the start date"}, status=status.HTTP_400_BAD_REQUEST)

        if end_date > max_future_date:
            return Response({"error": "Leave cannot be applied more than 45 days in advance"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LeaveRequestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MleaveRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee_name = request.query_params.get('employee_name', None)
        status_filter = request.query_params.get('status', None)

        leave_requests = LeaveRequest.objects.all()

        if employee_name:
            leave_requests = leave_requests.filter(employee__username=employee_name)

        if status_filter:
            leave_requests = leave_requests.filter(status=status_filter)

        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateLeaveStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, leave_id):
        try:
            leave_request = LeaveRequest.objects.get(id=leave_id)

            # Only a manager should be able to update the leave status
            if request.user.user_type != 'manager':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            new_status = request.data.get('status')
            if new_status not in ['pending', 'approved', 'rejected']:
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

            leave_request.status = new_status
            leave_request.save()

            serializer = LeaveRequestSerializer(leave_request)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except LeaveRequest.DoesNotExist:
            return Response({'error': 'Leave request not found'}, status=status.HTTP_404_NOT_FOUND)
