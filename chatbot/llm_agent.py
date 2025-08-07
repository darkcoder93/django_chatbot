import os
import json
import pandas as pd
from typing import Dict, Any, Optional
from django.conf import settings
import re


class SQLAgent:
    """Rule-based SQL agent for generating SQL queries from natural language (for testing)"""
    
    def __init__(self):
        # Database connection
        try:
            self.db_config = settings.REGRESSION_DB_CONFIG
        except:
            # Fallback for when Django settings are not configured
            self.db_config = {
                'host': 'localhost',
                'port': '5432',
                'database': 'regression_db',
                'user': 'postgres',
                'password': '',
            }
        self.engine = None
        self._connect_to_db()
        
        # Rule-based patterns for SQL generation
        self.patterns = {
            r'sales|revenue|income': {
                'sql': 'SELECT product_name, quantity, price, date, region FROM sales_data ORDER BY date DESC',
                'data_type': 'sales'
            },
            r'customer|client|buyer': {
                'sql': 'SELECT customer_name, email, total_purchases, registration_date FROM customer_data ORDER BY total_purchases DESC',
                'data_type': 'customer'
            },
            r'product|item|goods': {
                'sql': 'SELECT product_name, category, price, stock_quantity FROM product_data ORDER BY price DESC',
                'data_type': 'product'
            },
            r'transaction|order|purchase': {
                'sql': 'SELECT t.id, c.customer_name, p.product_name, t.quantity, t.total_amount, t.transaction_date FROM transactions t JOIN customer_data c ON t.customer_id = c.id JOIN product_data p ON t.product_id = p.id ORDER BY t.transaction_date DESC',
                'data_type': 'transaction'
            },
            r'top|highest|best|maximum': {
                'sql': 'SELECT product_name, SUM(quantity) as total_sold FROM sales_data GROUP BY product_name ORDER BY total_sold DESC LIMIT 10',
                'data_type': 'top_products'
            },
            r'region|area|location': {
                'sql': 'SELECT region, COUNT(*) as sales_count, SUM(quantity * price) as total_revenue FROM sales_data GROUP BY region ORDER BY total_revenue DESC',
                'data_type': 'region_analysis'
            },
            r'date|time|period|month|year': {
                'sql': 'SELECT DATE(date) as sale_date, COUNT(*) as daily_sales, SUM(quantity * price) as daily_revenue FROM sales_data GROUP BY DATE(date) ORDER BY sale_date DESC LIMIT 30',
                'data_type': 'time_series'
            },
            r'stock|inventory|quantity': {
                'sql': 'SELECT product_name, stock_quantity, category FROM product_data WHERE stock_quantity < 100 ORDER BY stock_quantity ASC',
                'data_type': 'low_stock'
            }
        }
    
    def _connect_to_db(self):
        """Connect to the regression database (mock for demo)"""
        # For demo purposes, we'll use a mock connection
        self.engine = None
        print("Using mock database connection for demo")
    
    def _get_schema_info(self) -> str:
        """Get database schema information for the LLM"""
        if not self.engine:
            # Return mock schema for demo
            return """
            Tables in the database:
            1. sales_data (id, product_name, quantity, price, date, region)
            2. customer_data (id, customer_name, email, registration_date, total_purchases)
            3. product_data (id, product_name, category, price, stock_quantity)
            4. transactions (id, customer_id, product_id, quantity, total_amount, transaction_date)
            """
        
        try:
            # Get actual schema information
            with self.engine.connect() as conn:
                # Get table names
                tables_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
                tables = conn.execute(text(tables_query)).fetchall()
                
                schema_info = "Tables in the database:\n"
                for table in tables:
                    table_name = table[0]
                    # Get columns for each table
                    columns_query = f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position
                    """
                    columns = conn.execute(text(columns_query)).fetchall()
                    
                    schema_info += f"{table_name} ("
                    schema_info += ", ".join([f"{col[0]} ({col[1]})" for col in columns])
                    schema_info += ")\n"
                
                return schema_info
        except Exception as e:
            print(f"Error getting schema info: {e}")
            return "Error retrieving schema information"
    
    def generate_sql_query(self, user_query: str) -> str:
        """Generate SQL query from user query using rule-based patterns"""
        try:
            user_query_lower = user_query.lower()
            
            # Check patterns in order of specificity
            for pattern, response in self.patterns.items():
                if re.search(pattern, user_query_lower):
                    return response['sql']
            
            # Default query if no pattern matches
            return "SELECT 'No specific pattern matched' as message, COUNT(*) as total_records FROM sales_data"
            
        except Exception as e:
            print(f"Error generating SQL query: {e}")
            return "SELECT 1 as error;"
    
    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query and return results (mock for demo)"""
        try:
            # Return mock data for demo
            return self._get_mock_data(sql_query)
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "columns": []
            }
    
    def _get_mock_data(self, sql_query: str) -> Dict[str, Any]:
        """Generate mock data for demo purposes based on SQL query patterns"""
        sql_lower = sql_query.lower()
        
        # Sales data
        if "sales_data" in sql_lower and "product_name" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"product_name": "Gaming Laptop", "quantity": 25, "price": 1299.99, "date": "2024-01-15", "region": "North"},
                    {"product_name": "Wireless Mouse", "quantity": 150, "price": 39.99, "date": "2024-01-16", "region": "South"},
                    {"product_name": "Mechanical Keyboard", "quantity": 80, "price": 149.99, "date": "2024-01-17", "region": "East"},
                    {"product_name": "4K Monitor", "quantity": 30, "price": 599.99, "date": "2024-01-18", "region": "West"},
                    {"product_name": "USB-C Hub", "quantity": 200, "price": 49.99, "date": "2024-01-19", "region": "North"},
                ],
                "columns": ["product_name", "quantity", "price", "date", "region"],
                "row_count": 5
            }
        
        # Customer data
        elif "customer_data" in sql_lower and "customer_name" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"customer_name": "John Doe", "email": "john.doe@email.com", "total_purchases": 2500.00, "registration_date": "2023-01-15"},
                    {"customer_name": "Jane Smith", "email": "jane.smith@email.com", "total_purchases": 3800.00, "registration_date": "2023-02-20"},
                    {"customer_name": "Bob Johnson", "email": "bob.johnson@email.com", "total_purchases": 1200.00, "registration_date": "2023-03-10"},
                    {"customer_name": "Alice Brown", "email": "alice.brown@email.com", "total_purchases": 4500.00, "registration_date": "2023-01-05"},
                    {"customer_name": "Charlie Wilson", "email": "charlie.wilson@email.com", "total_purchases": 1800.00, "registration_date": "2023-04-12"},
                ],
                "columns": ["customer_name", "email", "total_purchases", "registration_date"],
                "row_count": 5
            }
        
        # Product data
        elif "product_data" in sql_lower and "product_name" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"product_name": "Gaming Laptop", "category": "Electronics", "price": 1299.99, "stock_quantity": 45},
                    {"product_name": "Wireless Mouse", "category": "Accessories", "price": 39.99, "stock_quantity": 120},
                    {"product_name": "Mechanical Keyboard", "category": "Accessories", "price": 149.99, "stock_quantity": 65},
                    {"product_name": "4K Monitor", "category": "Electronics", "price": 599.99, "stock_quantity": 25},
                    {"product_name": "USB-C Hub", "category": "Accessories", "price": 49.99, "stock_quantity": 180},
                    {"product_name": "Gaming Headset", "category": "Accessories", "price": 89.99, "stock_quantity": 75},
                ],
                "columns": ["product_name", "category", "price", "stock_quantity"],
                "row_count": 6
            }
        
        # Transaction data
        elif "transactions" in sql_lower and "customer_name" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"id": 1001, "customer_name": "John Doe", "product_name": "Gaming Laptop", "quantity": 1, "total_amount": 1299.99, "transaction_date": "2024-01-15"},
                    {"id": 1002, "customer_name": "Jane Smith", "product_name": "4K Monitor", "quantity": 2, "total_amount": 1199.98, "transaction_date": "2024-01-16"},
                    {"id": 1003, "customer_name": "Bob Johnson", "product_name": "Wireless Mouse", "quantity": 3, "total_amount": 119.97, "transaction_date": "2024-01-17"},
                    {"id": 1004, "customer_name": "Alice Brown", "product_name": "Mechanical Keyboard", "quantity": 1, "total_amount": 149.99, "transaction_date": "2024-01-18"},
                    {"id": 1005, "customer_name": "Charlie Wilson", "product_name": "USB-C Hub", "quantity": 2, "total_amount": 99.98, "transaction_date": "2024-01-19"},
                ],
                "columns": ["id", "customer_name", "product_name", "quantity", "total_amount", "transaction_date"],
                "row_count": 5
            }
        
        # Top products analysis
        elif "total_sold" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"product_name": "Wireless Mouse", "total_sold": 150},
                    {"product_name": "USB-C Hub", "total_sold": 200},
                    {"product_name": "Gaming Laptop", "total_sold": 25},
                    {"product_name": "Mechanical Keyboard", "total_sold": 80},
                    {"product_name": "4K Monitor", "total_sold": 30},
                ],
                "columns": ["product_name", "total_sold"],
                "row_count": 5
            }
        
        # Region analysis
        elif "region" in sql_lower and "total_revenue" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"region": "North", "sales_count": 55, "total_revenue": 67499.45},
                    {"region": "South", "sales_count": 150, "total_revenue": 5998.50},
                    {"region": "East", "sales_count": 80, "total_revenue": 11999.20},
                    {"region": "West", "sales_count": 30, "total_revenue": 17999.70},
                ],
                "columns": ["region", "sales_count", "total_revenue"],
                "row_count": 4
            }
        
        # Time series data
        elif "sale_date" in sql_lower and "daily_revenue" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"sale_date": "2024-01-19", "daily_sales": 2, "daily_revenue": 149.97},
                    {"sale_date": "2024-01-18", "daily_sales": 1, "daily_revenue": 149.99},
                    {"sale_date": "2024-01-17", "daily_sales": 3, "daily_revenue": 119.97},
                    {"sale_date": "2024-01-16", "daily_sales": 2, "daily_revenue": 1199.98},
                    {"sale_date": "2024-01-15", "daily_sales": 1, "daily_revenue": 1299.99},
                ],
                "columns": ["sale_date", "daily_sales", "daily_revenue"],
                "row_count": 5
            }
        
        # Low stock alert
        elif "stock_quantity" in sql_lower and "stock_quantity <" in sql_lower:
            return {
                "success": True,
                "data": [
                    {"product_name": "4K Monitor", "stock_quantity": 25, "category": "Electronics"},
                    {"product_name": "Gaming Laptop", "stock_quantity": 45, "category": "Electronics"},
                    {"product_name": "Mechanical Keyboard", "stock_quantity": 65, "category": "Accessories"},
                    {"product_name": "Gaming Headset", "stock_quantity": 75, "category": "Accessories"},
                ],
                "columns": ["product_name", "stock_quantity", "category"],
                "row_count": 4
            }
        
        # Default fallback
        else:
            return {
                "success": True,
                "data": [
                    {"message": "Query executed successfully", "total_records": 485},
                    {"message": "No specific pattern matched", "total_records": 485},
                ],
                "columns": ["message", "total_records"],
                "row_count": 2
            }
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Main method to process user query and return results"""
        # Generate SQL query
        sql_query = self.generate_sql_query(user_query)
        
        # Execute query
        result = self.execute_query(sql_query)
        
        return {
            "sql_query": sql_query,
            "result": result,
            "user_query": user_query
        } 