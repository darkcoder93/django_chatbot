import uuid
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession, ChatMessage, QueryResult
from .serializers import ChatRequestSerializer, ChatResponseSerializer
from .llm_agent import SQLAgent
import pandas as pd
from io import BytesIO
import base64


def chat_interface(request):
    """Main chat interface view"""
    return render(request, 'chatbot/chat.html')


@api_view(['POST'])
@csrf_exempt
def chat_api(request):
    """API endpoint for chat interactions"""
    serializer = ChatRequestSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id')
        
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session, created = ChatSession.objects.get_or_create(session_id=session_id)
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message
        )
        
        # Process with LLM agent
        agent = SQLAgent()
        result = agent.process_query(message)
        
        # Save assistant response
        assistant_message = f"I've generated a SQL query for your request: {result['sql_query']}"
        if result['result']['success']:
            assistant_message += f"\n\nFound {result['result']['row_count']} rows of data."
        else:
            assistant_message += f"\n\nError: {result['result']['error']}"
        
        ChatMessage.objects.create(
            session=session,
            message_type='assistant',
            content=assistant_message
        )
        
        # Save query result
        QueryResult.objects.create(
            session=session,
            sql_query=result['sql_query'],
            result_data=result['result']
        )
        
        response_data = {
            'message': assistant_message,
            'sql_query': result['sql_query'],
            'result_data': result['result'],
            'session_id': session_id
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_chat_history(request, session_id):
    """Get chat history for a session"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.all()
        
        history = []
        for message in messages:
            history.append({
                'type': message.message_type,
                'content': message.content,
                'timestamp': message.timestamp.isoformat()
            })
        
        return Response({'history': history}, status=status.HTTP_200_OK)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_query_results(request, session_id):
    """Get query results for a session"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        results = session.query_results.all()
        
        query_results = []
        for result in results:
            query_results.append({
                'sql_query': result.sql_query,
                'result_data': result.result_data,
                'created_at': result.created_at.isoformat()
            })
        
        return Response({'query_results': query_results}, status=status.HTTP_200_OK)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def download_data(request):
    """Download data in Excel or CSV format"""
    try:
        data = request.data.get('data', [])
        columns = request.data.get('columns', [])
        format_type = request.data.get('format', 'csv')
        
        if not data or not columns:
            return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        if format_type.lower() == 'excel':
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            output.seek(0)
            
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            
        else:
            # Create CSV file
            output = BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            response = HttpResponse(output.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="data.csv"'
        
        return response
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK) 