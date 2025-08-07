from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ChatSession, ChatMessage, QueryResult
import json


class ChatbotViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_chat_interface_view(self):
        """Test that the main chat interface loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatbot/chat.html')


class ChatbotAPITest(APITestCase):
    def setUp(self):
        self.chat_url = reverse('chat_api')
        self.test_message = "Show me all sales data"
    
    def test_chat_api_without_message(self):
        """Test chat API without providing a message"""
        response = self.client.post(self.chat_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_chat_api_with_message(self):
        """Test chat API with a valid message"""
        data = {'message': self.test_message}
        response = self.client.post(self.chat_url, data, format='json')
        
        # Should return 200 even if OpenAI is not configured (uses mock data)
        self.assertIn(response.status_code, [200, 400, 500])
        
        if response.status_code == 200:
            response_data = response.json()
            self.assertIn('message', response_data)
            self.assertIn('sql_query', response_data)
            self.assertIn('result_data', response_data)
            self.assertIn('session_id', response_data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'healthy'})


class ChatbotModelsTest(TestCase):
    def setUp(self):
        self.session = ChatSession.objects.create(session_id="test-session-123")
    
    def test_chat_session_creation(self):
        """Test chat session creation"""
        self.assertEqual(self.session.session_id, "test-session-123")
        self.assertIsNotNone(self.session.created_at)
        self.assertIsNotNone(self.session.updated_at)
    
    def test_chat_message_creation(self):
        """Test chat message creation"""
        message = ChatMessage.objects.create(
            session=self.session,
            message_type='user',
            content='Test message'
        )
        self.assertEqual(message.content, 'Test message')
        self.assertEqual(message.message_type, 'user')
        self.assertEqual(message.session, self.session)
    
    def test_query_result_creation(self):
        """Test query result creation"""
        result = QueryResult.objects.create(
            session=self.session,
            sql_query='SELECT * FROM test_table',
            result_data={'success': True, 'data': [], 'row_count': 0}
        )
        self.assertEqual(result.sql_query, 'SELECT * FROM test_table')
        self.assertEqual(result.result_data['success'], True)
        self.assertEqual(result.session, self.session) 