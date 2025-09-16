from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("assigned_to", "created_at", "updated_at")

    def validate(self, data):
        status = data.get("status") or self.instance and self.instance.status
        if status == Task.STATUS_COMPLETED:
            completion_report = data.get("completion_report") if "completion_report" in data else getattr(self.instance, "completion_report", None)
            worked_hours = data.get("worked_hours") if "worked_hours" in data else getattr(self.instance, "worked_hours", None)
            if not completion_report:
                raise serializers.ValidationError({"completion_report":"Required when marking Completed."})
            if worked_hours is None:
                raise serializers.ValidationError({"worked_hours":"Required when marking Completed."})
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id","title","assigned_to","status","completion_report","worked_hours","due_date")
