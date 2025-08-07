# SQL Chatbot - Django Application

A Django-based chatbot application that uses a custom LLM agent to generate SQL queries from natural language prompts and displays the results in a beautiful, interactive interface.

## Features

- **Natural Language to SQL**: Convert natural language questions into SQL queries using OpenAI's LLM
- **Interactive Chat Interface**: Real-time chat interface with message history
- **SQL Query Preview**: View generated SQL queries in real-time
- **Data Visualization**: Display query results in a responsive table format
- **Data Export**: Download results in CSV and Excel formats
- **Session Management**: Maintain chat sessions and query history
- **Responsive Design**: Works on desktop and mobile devices

## Layout

The application features a split-screen layout:
- **Left Half**: Chat window for user interactions
- **Right Half**: 
  - **Upper Section**: SQL query preview
  - **Lower Section**: Data table with download options

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (for production)
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   OPENAI_API_KEY=your-openai-api-key
   
   # Database configuration (for production)
   REGRESSION_DB_HOST=localhost
   REGRESSION_DB_PORT=5432
   REGRESSION_DB_NAME=regression_db
   REGRESSION_DB_USER=postgres
   REGRESSION_DB_PASSWORD=your-password
   ```

5. **Run database migrations**
   ```bash
   uv run python manage.py makemigrations
   uv run python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   uv run python manage.py runserver
   ```

8. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

1. **Start a conversation**: Type your question in natural language
2. **View SQL**: The generated SQL query appears in the upper right panel
3. **See results**: Query results are displayed in the lower right table
4. **Download data**: Use the CSV or Excel buttons to download results
5. **Continue chatting**: Ask follow-up questions to refine your queries

## Example Queries

- "Show me all sales data"
- "What are the top 10 customers by total purchases?"
- "Find products with stock quantity less than 50"
- "Calculate total revenue by region"
- "Show me transactions from last month"

## Project Structure

```
chatbot2/
├── chatbot_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── chatbot/                  # Main chatbot application
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── llm_agent.py
├── templates/
│   └── chatbot/
│       └── chat.html
├── static/
│   └── css/
│       └── style.css
├── manage.py
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat/` - Send chat message
- `GET /api/chat/history/<session_id>/` - Get chat history
- `GET /api/chat/results/<session_id>/` - Get query results
- `POST /api/download/` - Download data in CSV/Excel format
- `GET /api/health/` - Health check endpoint

## Configuration

### Database Setup

For production, configure your PostgreSQL database in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### OpenAI Configuration

Set your OpenAI API key in the `.env` file:

```env
OPENAI_API_KEY=sk-your-openai-api-key
```

## Customization

### Adding New Data Sources

1. Update the `_get_schema_info()` method in `llm_agent.py`
2. Modify the database connection in `settings.py`
3. Update the mock data in `_get_mock_data()` for testing

### Styling

- Modify `static/css/style.css` for custom styling
- Update `templates/chatbot/chat.html` for layout changes

### LLM Agent

- Customize the SQL generation prompt in `llm_agent.py`
- Adjust temperature and max_tokens for different response styles
- Add additional validation or error handling

## Troubleshooting

### Common Issues

1. **OpenAI API Error**: Ensure your API key is valid and has sufficient credits
2. **Database Connection**: Check your database credentials and connection settings
3. **CSRF Token Error**: Ensure CSRF tokens are properly configured
4. **Static Files Not Loading**: Run `python manage.py collectstatic` in production

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG=True
```

## Production Deployment

1. **Set up a production database**
2. **Configure environment variables**
3. **Set `DEBUG=False`**
4. **Run `python manage.py collectstatic`**
5. **Use a production WSGI server (Gunicorn, uWSGI)**
6. **Set up a reverse proxy (Nginx)**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on the GitHub repository. 