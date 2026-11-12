from django.shortcuts import render, get_object_or_404

from .models import User, Job, Candidate, Application
from .serializers import JobSerializer, CandidateSerializer, ApplicationSerializer, ApplicationStatusSerializer


from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.




# =========== AUTHENTICATION ===========

"""
# USING SERIALIZERS

from .serializers import RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user_obj = User.objects.create_user(
            username = serializer.validated_data['username'],
            password = serializer.validated_data['password'],
            role = serializer.validated_data['role'],
        )

        if user_obj.role == 'CANDIDATE':
            Candidate.objects.create(user=user_obj, name=user_obj.username)

        token, _ = Token.objects.get_or_create(user=user_obj)
        
        return Response({
            'Message': 'User created Successfully.',
            "username": user_obj.username,
            'role': user_obj.role,
            'token': token.key
            }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""




@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    u_name = request.data.get('username')
    pwd = request.data.get('password')
    role = request.data.get('role')

    if not u_name or not pwd or not role:
        return Response({'Error': "Fields Required."}, status=status.HTTP_400_BAD_REQUEST)

    if role != 'RECRUITER' and role != 'CANDIDATE':
        return Response({'error': 'role must be RECRUITER or CANDIDATE.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=u_name).exists():
        return Response({'Error': "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user_obj = User.objects.create_user(
        username=u_name,
        password=pwd,
        role=role
        )
    token, _ = Token.objects.get_or_create(user=user_obj)

    return Response({
        'Message': 'User created Successfully.',
        "username": user_obj.username,
        'role': user_obj.role,
        'token': token.key
        }, status=status.HTTP_201_CREATED)





@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    u_name = request.data.get('username')
    pwd = request.data.get('password')

    user_obj = authenticate(username=u_name, password=pwd)

    if user_obj is None:
        return Response({'error': 'Invalid Credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user_obj)
    return Response({'Token': token.key, 'username': user_obj.username, 'role': user_obj.role})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully."})






# =========== JOB MANAGEMENT ===========

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def job_list(request):

    # POST : allows recruiters only
    if request.method != 'GET' and request.user.role != 'RECRUITER':
        return Response({'Error': 'Only Recruiters have permission to post Job.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        jobs = Job.objects.all().order_by('-id')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)        # shows username in backend admin when the job is created..
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # MODIFY AND DELETE : recruiter only
    if request.method != 'GET' and request.user.role != 'RECRUITER':
        return Response({'Error': 'You have no permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    # MODIFY AND DELETE : only jobs belongs to posted recruiter
    if request.method != 'GET' and job.created_by != request.user:
        return Response({'Error': 'This job belongs to another Recruiter. You can only modify your own jobs.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





# =========== CANDIDATE MANAGEMENT ===========


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def candidate_profile(request):

    if request.user.role != 'CANDIDATE':
        return Response({'Error': 'Only Candidates are allowed to manage their Profile.'}, status=status.HTTP_403_FORBIDDEN)
    
    candidate = Candidate.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if candidate is not None:
            return Response({'Error': 'Profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if candidate is None:
        return Response({'Error': 'Profile not created yet.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CandidateSerializer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CandidateSerializer(candidate)
    return Response(serializer.data, status=status.HTTP_200_OK)




# =========== JOB APPLICATION ===========

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_apply(request, pk):

    if request.user.role != 'CANDIDATE':
        return Response({'Error': 'Only Candidates allowed to apply for this job.'}, status=status.HTTP_403_FORBIDDEN)

    job = get_object_or_404(Job, pk=pk)
    candidate = Candidate.objects.filter(user=request.user).first()

    if candidate is None:
        return Response({'Error': 'Please complete your profile before applying for a Job.'}, status=status.HTTP_400_BAD_REQUEST)

    if job.status == "Closed":
        return Response({'Error': 'This job is closed and not accepting applications.'}, status=status.HTTP_400_BAD_REQUEST)

    if Application.objects.filter(job=job, candidate=candidate).exists():
        return Response({'Error': 'You have already applied for this job.'}, status=status.HTTP_400_BAD_REQUEST)

    application = Application.objects.create(job=job, candidate=candidate)
    serializer = ApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_list(request):

    if request.user.role != 'CANDIDATE':
        return Response({'Error': 'Only Candidates are allowed to view applications.'}, status=status.HTTP_403_FORBIDDEN)

    candidate = Candidate.objects.filter(user=request.user).first()

    if candidate is None:
        return Response({'Error': 'Candidate profile not found.'}, status=status.HTTP_404_NOT_FOUND)


    applications = Application.objects.filter(candidate=candidate).order_by('-id')

    if not applications:
        return Response({'Message': 'No applications yet.'}, status=status.HTTP_200_OK)
    
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_detail(request, pk):

    if request.user.role != 'CANDIDATE':
        return Response({'Error': 'Only Candidates are allowed to view applications.'}, status=status.HTTP_403_FORBIDDEN)

    candidate = Candidate.objects.filter(user=request.user).first()

    if candidate is None:
        return Response({'Error': 'Candidate profile not found.'}, status=status.HTTP_404_NOT_FOUND)


    application = get_object_or_404(Application, pk=pk, candidate=candidate)

    if not application:
        return Response({'Message': 'No applications yet.'}, status=status.HTTP_200_OK)
    
    serializer = ApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def application_status(request, pk):
    if request.user.role != 'RECRUITER':
        return Response({'Error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)


    application = get_object_or_404(Application, pk=pk)

    if application.job.created_by != request.user:
        return Response({'Error': 'This job is application belong to another Recruiter. You cannot modify it.'}, status=status.HTTP_403_FORBIDDEN)

    new_status = request.data.get('status')

    if not new_status:
        return Response({'Error': 'Status Field required.'}, status=status.HTTP_403_FORBIDDEN)
    
    if new_status not in ['APPLIED', 'SHORTLISTED', 'INTERVIEW', 'SELECTED', 'REJECTED']:
        return Response({'Error': 'Invalid status. Use only APPLIED, SHORTLISTED, INTERVIEW, SELECTED or REJECTED'}, status=status.HTTP_403_FORBIDDEN)


    serializer = ApplicationStatusSerializer(application, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
