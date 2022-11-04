from rest_framework import serializers

from core.models import Record


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = ['id', 'amount', 'is_deleted']
        read_only_fields = ['id']
        extra_kwargs = {'is_deleted': {'write_only': True}}
        

class RecordDetailSerializer(RecordSerializer):
    '''내역 상세 보기에서 memo 확인'''
    class Meta(RecordSerializer.Meta):
        fields = RecordSerializer.Meta.fields + ['memo']
        