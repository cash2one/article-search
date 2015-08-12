# coding: utf-8
from rest_framework import serializers
from employee.models import Operator

class EmployeeDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    perms = serializers.SerializerMethodField(method_name='get_employee_perms')

    def get_employee_perms(self, employee):
        return [perm.split('.')[1] for perm in employee.user.get_all_permissions()
            if perm.split('.')[0] == 'composition']

    class Meta:
        model = Operator
        fields = ('username', 'email', 'qq', 'memo', 'created_count', 'approved_count', 'perms')
        read_only_fields = ('username', 'email', 'qq', 'memo', 'created_count', \
            'approved_count', 'perms')