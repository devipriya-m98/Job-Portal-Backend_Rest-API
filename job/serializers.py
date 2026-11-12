from rest_framework import serializers

from . models import User, Job, Candidate, Application



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']



class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'skills', 'location', 'experience', 'min_salary', 'max_salary', 'status', 'created_at']



class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'phone', 'qualification', 'skills', 'experience']



class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_location = serializers.CharField(source='job.location', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job_title', 'job', 'job_location', 'candidate', 'status', 'applied_at' ]
        read_only_fields = ['job', 'candidate', 'status', 'applied_at']



class ApplicationStatusSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job_title', 'job', 'candidate_name', 'status' ]
        read_only_fields = ['job', 'candidate']