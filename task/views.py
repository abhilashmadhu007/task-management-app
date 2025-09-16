from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, TaskReportSerializer
from .permissions import IsAssignedUser, IsAdminOrSuperAdmin

# GET /api/tasks  (list tasks for logged-in user)
class UserTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by("-due_date")

# PUT /api/tasks/{id}  (update status)
class TaskUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAssignedUser]

    # ensure only allowed fields updated; assigned user can't reassign etc
    def perform_update(self, serializer):
        serializer.save()

# GET /api/tasks/{id}/report  (Admins & SuperAdmins can view reports)
from rest_framework.views import APIView
class TaskReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)

        # only for completed tasks
        if task.status != Task.STATUS_COMPLETED:
            return Response({"detail":"Report available only for completed tasks."}, status=status.HTTP_400_BAD_REQUEST)

        # If Admin (not SuperAdmin), ensure admin is assigned to this user
        if request.user.role == "Admin":
            if task.assigned_to.assigned_admin_id != request.user.id:
                return Response({"detail":"Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskReportSerializer(task)
        return Response(serializer.data)

