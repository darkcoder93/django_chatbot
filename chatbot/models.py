from django.db import models
from django.utils import timezone


class ChatSession(models.Model):
    """Model to store chat sessions"""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """Model to store individual chat messages"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('assistant', 'Assistant Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class QueryResult(models.Model):
    """Model to store SQL query results"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='query_results')
    sql_query = models.TextField()
    result_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Query: {self.sql_query[:50]}..." 