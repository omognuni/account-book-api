from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
from django.core.cache import cache

from core.models import Record

from record.serializers import RecordSerializer, RecordDetailSerializer


class RecordViewSet(viewsets.ModelViewSet):
    '''Record View'''
    serializer_class = RecordDetailSerializer
    queryset = Record.objects.all()
    
    def get_queryset(self):
        '''요청한 유저의 삭제되지 않은 내역만 필터'''
        queryset = self.queryset.filter(user=self.request.user).exclude(is_deleted=True)
        
        return queryset
    
    def get_serializer_class(self):
        '''list 일때는 amount만 보여주기'''
        if self.action == 'list':
            return RecordSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(methods=['GET'], detail=True, url_path='delete')
    def delete(self, request, pk=None):
        '''내역 임시 삭제 및 복구'''
        record = Record.objects.get(id=pk)
        record.is_deleted = not record.is_deleted
        record.save()
        
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path='restore')
    def restore(self, request):
        '''복구를 위한 삭제 내역 가져오기'''
        queryset = self.queryset.filter(user=self.request.user).exclude(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        