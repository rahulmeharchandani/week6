import csv
import io
import threading
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['age']
    search_fields = ['name', 'email']
    ordering_fields = ['age', 'name', 'email']

    def perform_create(self, serializer):
        student = serializer.save()
        threading.Thread(target=self.send_creation_email, args=(student.email,)).start()

    def send_creation_email(self, to_email):
        send_mail(
            'Welcome Student',
            'You have been successfully registered.',
            'admin@example.com',
            [to_email],
            fail_silently=True,
        )

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def upload_csv(self, request):
        csv_file = request.FILES['file']
        decoded = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)
        students = [Student(**row) for row in reader]
        Student.objects.bulk_create(students)
        return Response({'status': 'CSV uploaded and students created.'})

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=students.csv'
        writer = csv.writer(response)
        writer.writerow(['name', 'email', 'age'])
        for student in Student.objects.all():
            writer.writerow([student.name, student.email, student.age])
        return response