# Amazon SP-API Chatbot with CrewAI

A sophisticated chatbot that integrates with Amazon's Selling Partner API (SP-API) using CrewAI for intelligent data analysis and conversation management.

## 🏗️ Project Structure

```
spapi-crewai-chatbot/
├── .gitignore
├── README.md
├── docker-compose.yml
│
├── backend/                    # Python backend with CrewAI
│   ├── venv/                   # Python virtual environment
│   ├── spapi_crewai_chatbot.py # Main chatbot entry point
│   ├── advanced_chatbot.py     # Enhanced chatbot with context
│   ├── web_interface.py        # Flask web interface
│   ├── config.py               # Configuration management
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (don't commit!)
│   └── .env.example           # Environment template
│
├── frontend/                   # React frontend
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatBot.tsx     # Main chat component
│   │   ├── services/
│   │   ├── config.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── .env
│
└── sp-api-mcp-server/          # MCP server for SP-API integration
    ├── node_modules/
    ├── src/
    │   └── index.js            # MCP server implementation
    ├── package.json
    └── ... (MCP server files)
```

## 🚀 Features

- **Context-Aware Conversations**: Maintains conversation history and context
- **Multi-Turn Dialogues**: Supports follow-up questions and clarifications
- **Report Generation**: Creates formatted reports from your Amazon data
- **Data Caching**: Intelligent caching for improved performance
- **Web Interface**: Modern React-based chat interface
- **MCP Integration**: Model Context Protocol server for SP-API access

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Amazon SP-API credentials
- AWS credentials

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

5. Run the chatbot:
   ```bash
   python spapi_crewai_chatbot.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### MCP Server Setup

1. Navigate to the MCP server directory:
   ```bash
   cd sp-api-mcp-server
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the server:
   ```bash
   npm start
   ```

## 🐳 Docker Setup

Use the included `docker-compose.yml` to run all services:

```bash
docker-compose up -d
```

## 📝 Usage

### Basic Chat Interface

Start a conversation with natural language queries:

- "Show me sales from last week"
- "What are my top-selling products?"
- "Generate a sales report for Q1"
- "How many orders did I get yesterday?"

### Advanced Features

- **Context Awareness**: The chatbot remembers previous queries and can answer follow-up questions
- **Report Generation**: Ask for detailed reports and the bot will format the data appropriately
- **Multi-Marketplace Support**: Query data across different Amazon marketplaces

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```
MCP_SERVER_URL=http://localhost:3000
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
SP_API_REFRESH_TOKEN=your_refresh_token
SP_API_CLIENT_ID=your_client_id
SP_API_CLIENT_SECRET=your_client_secret
```

#### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=ws://localhost:5000
```

## 🤖 CrewAI Integration

The chatbot uses CrewAI for intelligent task management:

- **Query Parser**: Extracts intent and entities from natural language
- **Endpoint Selector**: Chooses appropriate SP-API endpoints
- **Data Processor**: Handles and formats API responses
- **Report Generator**: Creates formatted reports

## 📊 API Endpoints

### Backend API
- `POST /chat` - Send chat messages
- `GET /health` - Health check

### MCP Server
- `GET /health` - Server health
- `POST /mcp/call` - Call MCP tools

## 🔒 Security

- Never commit `.env` files
- Use environment variables for all sensitive data
- Implement proper authentication for production use
- Follow AWS security best practices

## 📈 Monitoring

- Health check endpoints for all services
- Logging for debugging and monitoring
- Error handling and user feedback

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔄 Updates

Stay updated with the latest Amazon SP-API changes and CrewAI improvements by regularly updating dependencies and checking for new features.

