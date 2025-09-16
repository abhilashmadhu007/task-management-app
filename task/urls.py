from django.urls import path
from .views import UserTaskListView, TaskUpdateView, TaskReportView

urlpatterns = [
    path("", UserTaskListView.as_view(), name="user-tasks"),           # GET /api/tasks
    path("<int:pk>/", TaskUpdateView.as_view(), name="task-update"),   # PUT
    path("<int:pk>/report/", TaskReportView.as_view(), name="task-report"),
]