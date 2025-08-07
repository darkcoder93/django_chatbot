from rest_framework import serializers
from .models import ChatSession, ChatMessage, QueryResult


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message_type', 'content', 'timestamp']


class QueryResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryResult
        fields = ['id', 'sql_query', 'result_data', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    query_results = QueryResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'created_at', 'updated_at', 'messages', 'query_results']


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100, required=False)


class ChatResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    sql_query = serializers.CharField()
    result_data = serializers.JSONField()
    session_id = serializers.CharField() 