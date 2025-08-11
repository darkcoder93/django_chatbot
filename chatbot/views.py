from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime, timezone
import json


def chat_interface(request):
    """Main chat interface view for frontend demo"""
    # Generate session ID in the format: ddMMyyHHmmss.ffffff
    now = datetime.now(timezone.utc)
    session_id = now.strftime("%d%m%y%H%M%S.%f")
    
    context = {
        'session_id': session_id
    }
    return render(request, 'chatbot/chat.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API endpoint for chat interactions - always returns same example response in LLM agent format"""
    try:
        # Parse JSON data
        data = json.loads(request.body)
        user_message = data.get('message', '')
        session_id = data.get('session_id', '')
        
        # Always return the same example response in LLM agent format
        example_response = {
            "SQL Query": "SELECT product_name, quantity, price, date, region FROM sales_data ORDER BY date DESC LIMIT 5",
            "Output columns": [
                "product_name",
                "quantity", 
                "price",
                "date",
                "region"
            ],
            "Query Result": [
                ["Gaming Laptop", 25, 1299.99, "2024-01-15", "North"],
                ["Wireless Mouse", 150, 39.99, "2024-01-16", "South"],
                ["Mechanical Keyboard", 80, 149.99, "2024-01-17", "East"],
                ["4K Monitor", 30, 599.99, "2024-01-18", "West"],
                ["USB-C Hub", 200, 49.99, "2024-01-19", "North"]
            ],
            "summary": "# Sales Data Analysis 📊\n\nHere's your **sales data**! I've pulled the latest product sales information.\n\n## Summary:\n- **Total Sales**: $45,000\n- **Products Sold**: 5\n- **Date Range**: Jan 15-19, 2024\n\n## Key Insights:\n1. **Gaming Laptop** is the highest revenue generator\n2. **Wireless Mouse** has the highest volume\n3. **North Region** shows strong performance\n\n*Data retrieved successfully from sales_data table*"
        }
        
        return JsonResponse(example_response, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 