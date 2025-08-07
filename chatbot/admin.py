from django.contrib import admin
from .models import ChatSession, ChatMessage, QueryResult


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'updated_at', 'message_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_id']
    readonly_fields = ['created_at', 'updated_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp', 'session']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(QueryResult)
class QueryResultAdmin(admin.ModelAdmin):
    list_display = ['session', 'sql_preview', 'row_count', 'created_at']
    list_filter = ['created_at', 'session']
    search_fields = ['sql_query', 'session__session_id']
    readonly_fields = ['created_at']
    
    def sql_preview(self, obj):
        return obj.sql_query[:50] + '...' if len(obj.sql_query) > 50 else obj.sql_query
    sql_preview.short_description = 'SQL Query'
    
    def row_count(self, obj):
        if obj.result_data and 'row_count' in obj.result_data:
            return obj.result_data['row_count']
        return 0
    row_count.short_description = 'Rows' 