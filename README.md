# Binance P2P Orders API

## 📌 Overview

এই project টি একটি **FastAPI-based REST API backend** যা Binance P2P trading এর orders track করার জন্য তৈরি করা হয়েছে। এটি একটি server হিসেবে run করতে পারবেন এবং যেকোনো frontend application থেকে API call করে data fetch করতে পারবেন।

## 🔧 Features

### Backend API Features:
- ✅ **RESTful API** - FastAPI দিয়ে তৈরি modern REST API
- ✅ **Multiple Endpoints** - BUY, SELL, All, Completed orders, Summary
- ✅ **Caching System** - In-memory caching (5 min TTL) for better performance
- ✅ **CORS Support** - Frontend থেকে access করার জন্য
- ✅ **Auto API Docs** - Swagger UI এবং ReDoc built-in
- ✅ **Error Handling** - Proper HTTP status codes এবং error messages
- ✅ **Type Safety** - Pydantic models দিয়ে data validation
- ✅ **Logging** - Request/response logging

### Business Features:
- ✅ Last 30-90 days এর P2P orders fetch করা
- ✅ BUY এবং SELL orders আলাদাভাবে fetch করা
- ✅ Order details: Amount, Price, Unit Price, Timestamp, Status, Fees
- ✅ Summary statistics: Total amounts, fees, average prices, profit/loss
- ✅ Secure API authentication using HMAC SHA256 signature
- ✅ Environment variables থেকে API credentials load করা

## 📁 Project Structure

```
binance/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration and settings
│   │   └── cache.py           # In-memory caching system
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models for request/response
│   ├── routes/
│   │   ├── __init__.py
│   │   └── orders.py          # API endpoints for orders
│   └── services/
│       ├── __init__.py
│       └── binance_service.py # Binance API integration
├── p2p_orders.py              # Legacy CLI script (still works)
├── .env                       # API credentials (gitignore করা)
├── .env.example               # Example environment variables
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd binance
```

### 2. Virtual Environment তৈরি করা (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# অথবা
.venv\Scripts\activate  # Windows
```

### 3. Dependencies Install করা

```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup

`.env.example` file কে copy করে `.env` নামে save করুন:

```bash
cp .env.example .env
```

তারপর `.env` file এ আপনার Binance API credentials add করুন:

```env
apiKey=YOUR_API_KEY_HERE
secretKey=YOUR_SECRET_KEY_HERE

# Optional configuration
DEBUG=False
CACHE_TTL=300
MAX_REQUESTS_PER_MINUTE=60
```

**⚠️ Security Note:** `.env` file টি কখনো public repository তে push করবেন না!

### 5. Backend Server Run করা

```bash
# Development mode (auto-reload enabled)
python -m app.main

# অথবা uvicorn দিয়ে
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server start হলে এই URLs এ access করতে পারবেন:
- **API Base:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 6. (Optional) Legacy CLI Script Run করা

পুরনো CLI script এখনও কাজ করবে:

```bash
python3 p2p_orders.py
```

## 📚 API Documentation

### Available Endpoints

#### 1. Health Check
```http
GET /
GET /health
```
Server running কিনা check করার জন্য।

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Binance P2P Orders API",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00",
  "binance_api_configured": true
}
```

---

#### 2. Get BUY Orders
```http
GET /api/orders/buy?days=30&use_cache=true
```

**Query Parameters:**
- `days` (optional): Number of days (1-90), default: 30
- `use_cache` (optional): Use cached data, default: true

**Response:**
```json
{
  "success": true,
  "message": "Successfully fetched 10 BUY orders",
  "data": [...],
  "count": 10,
  "trade_type": "BUY",
  "cached": true
}
```

---

#### 3. Get SELL Orders
```http
GET /api/orders/sell?days=30&use_cache=true
```

Same as BUY orders but for SELL type.

---

#### 4. Get All Orders
```http
GET /api/orders/all?days=30&use_cache=true
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully fetched all orders",
  "data": {
    "buy_orders": [...],
    "sell_orders": [...]
  },
  "count": {
    "buy": 10,
    "sell": 8,
    "total": 18
  },
  "cached": true
}
```

---

#### 5. Get Completed Orders Only
```http
GET /api/orders/completed?trade_type=BUY&days=30&use_cache=true
```

**Query Parameters:**
- `trade_type` (optional): 'BUY', 'SELL', or null for both
- `days` (optional): Number of days (1-90), default: 30
- `use_cache` (optional): Use cached data, default: true

---

#### 6. Get Summary Statistics
```http
GET /api/orders/summary?days=30&use_cache=true
```

**Response:**
```json
{
  "success": true,
  "message": "Summary calculated successfully",
  "data": {
    "total_buy_orders": 10,
    "total_sell_orders": 8,
    "total_completed_orders": 18,
    "total_buy_amount": 1000.00,
    "total_sell_amount": 950.00,
    "total_buy_value": 120000.00,
    "total_sell_value": 114000.00,
    "total_buy_fees": 1.00,
    "total_sell_fees": 0.95,
    "total_fees": 1.95,
    "average_buy_price": 120.00,
    "average_sell_price": 120.00,
    "net_profit_bdt": -6000.00,
    "net_profit_percentage": -5.00
  },
  "cached": true
}
```

---

#### 7. Clear Cache
```http
DELETE /api/orders/cache
```

Force fresh data fetch on next request.

---

#### 8. Get Cache Statistics
```http
GET /api/orders/cache/stats
```

**Response:**
```json
{
  "success": true,
  "message": "Cache stats retrieved successfully",
  "data": {
    "total_entries": 2,
    "active_entries": 2,
    "expired_entries": 0
  }
}
```

---

### Example API Calls

#### Using cURL:
```bash
# Get buy orders
curl http://localhost:8000/api/orders/buy?days=30

# Get summary
curl http://localhost:8000/api/orders/summary?days=7

# Clear cache
curl -X DELETE http://localhost:8000/api/orders/cache
```

#### Using JavaScript (fetch):
```javascript
// Get all orders
const response = await fetch('http://localhost:8000/api/orders/all?days=30');
const data = await response.json();
console.log(data);

// Get summary
const summary = await fetch('http://localhost:8000/api/orders/summary');
const summaryData = await summary.json();
console.log(summaryData.data);
```

#### Using Python (requests):
```python
import requests

# Get buy orders
response = requests.get('http://localhost:8000/api/orders/buy', params={'days': 30})
data = response.json()
print(data)

# Get summary
summary = requests.get('http://localhost:8000/api/orders/summary')
print(summary.json())
```

---

## 🎯 Architecture Overview

### Backend Components:

#### 1. **app/main.py** - FastAPI Application
- Entry point for the server
- CORS configuration
- Global exception handling
- Router registration

#### 2. **app/core/config.py** - Configuration Management
- Environment variables loading
- Settings validation
- API credentials management

#### 3. **app/core/cache.py** - Caching System
- In-memory cache with TTL
- Automatic expiration
- Cache statistics

#### 4. **app/models/schemas.py** - Data Models
- Pydantic models for type safety
- Request/response validation
- API documentation

#### 5. **app/services/binance_service.py** - Business Logic
- Binance API integration
- HMAC SHA256 signature generation
- Order fetching and filtering
- Summary calculations

#### 6. **app/routes/orders.py** - API Endpoints
- RESTful API routes
- Query parameter validation
- Error handling

## 📊 Server Output Example

```bash
$ python -m app.main

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     2024-01-01 12:00:00 - __main__ - INFO - Starting Binance P2P Orders API v1.0.0
INFO:     2024-01-01 12:00:00 - __main__ - INFO - API credentials validated successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

তারপর browser এ http://localhost:8000/docs তে গিয়ে interactive API documentation দেখতে পারবেন।

## 🔐 API Authentication

Script টি Binance API এর নিচের endpoint ব্যবহার করে:

- **Endpoint:** `/sapi/v1/c2c/orderMatch/listUserOrderHistory`
- **Method:** GET
- **Authentication:** API Key + Signature (HMAC SHA256)

### Required Headers:

- `X-MBX-APIKEY`: Your API key

### Required Parameters:

- `tradeType`: BUY অথবা SELL
- `timestamp`: Current timestamp (milliseconds)
- `startTimestamp`: Start time (30 days ago)
- `signature`: HMAC SHA256 signature

## 🚀 Deployment

### Production Deployment

#### Using systemd (Linux):

1. Create service file: `/etc/systemd/system/binance-p2p-api.service`

```ini
[Unit]
Description=Binance P2P Orders API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/binance
Environment="PATH=/path/to/binance/.venv/bin"
ExecStart=/path/to/binance/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable binance-p2p-api
sudo systemctl start binance-p2p-api
sudo systemctl status binance-p2p-api
```

#### Using Docker:

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t binance-p2p-api .
docker run -d -p 8000:8000 --env-file .env binance-p2p-api
```

#### Using PM2 (Node.js process manager):

```bash
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name binance-p2p-api
pm2 save
pm2 startup
```

---

## 📝 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `apiKey` | Binance API Key | - | ✅ Yes |
| `secretKey` | Binance Secret Key | - | ✅ Yes |
| `DEBUG` | Enable debug mode | `False` | ❌ No |
| `CACHE_TTL` | Cache TTL in seconds | `300` | ❌ No |
| `MAX_REQUESTS_PER_MINUTE` | Rate limit | `60` | ❌ No |

### CORS Origins

Default allowed origins (edit in [app/core/config.py](app/core/config.py)):
```python
CORS_ORIGINS = [
    "http://localhost:3000",   # React default
    "http://localhost:5173",   # Vite default
    "http://localhost:8080",   # Vue default
]
```

আপনার frontend URL add করতে পারেন।

## ⚠️ Important Notes

1. API Key এবং Secret Key secure রাখুন
2. `.env` file কখনো commit করবেন না
3. API rate limits খেয়াল রাখুন
4. Orders data sensitive, careful handle করুন

## 🐛 Troubleshooting

### Server Won't Start

**Problem:** Server start হচ্ছে না
```bash
ValueError: API_KEY and SECRET_KEY must be set in .env file
```

**Solution:**
- `.env` file আছে কিনা check করুন
- `.env` file এ `apiKey` এবং `secretKey` সঠিকভাবে set আছে কিনা verify করুন

---

### Import Errors

**Problem:** Import errors দেখাচ্ছে
```
ImportError: No module named 'fastapi'
```

**Solution:**
```bash
# Virtual environment activate করুন
source .venv/bin/activate

# Dependencies install করুন
pip install -r requirements.txt
```

---

### Binance API Errors

**Problem:** API error response
```json
{
  "success": false,
  "message": "Binance API error: Signature for this request is not valid"
}
```

**Solution:**
- API Key এবং Secret Key সঠিক আছে কিনা check করুন
- API permissions enabled আছে কিনা (P2P Trading, Enable Reading)
- System time সঠিক আছে কিনা (timestamp issues এর জন্য)

---

### No Orders Found

**Problem:** Empty orders list return হচ্ছে

**Solution:**
- Last 30 days এ আসলেই কোনো P2P trade হয়েছে কিনা Binance account এ check করুন
- `days` parameter increase করে try করুন: `/api/orders/all?days=90`
- Binance P2P তে manually কিছু trade complete করুন test করার জন্য

---

### CORS Errors (Frontend থেকে call করলে)

**Problem:**
```
Access to fetch at 'http://localhost:8000/api/orders/buy' from origin
'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
[app/core/config.py](app/core/config.py) file এ আপনার frontend URL add করুন:
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://your-frontend-url.com",  # Add this
]
```

---

### Cache Issues

**Problem:** Stale/old data পাচ্ছেন

**Solution:**
```bash
# Cache clear করুন
curl -X DELETE http://localhost:8000/api/orders/cache

# অথবা use_cache=false করে request করুন
curl http://localhost:8000/api/orders/buy?use_cache=false
```

## 📚 Dependencies

### Core:
- **requests** - HTTP requests এর জন্য (Binance API calls)
- **python-dotenv** - Environment variables load করার জন্য

### Backend:
- **fastapi** - Modern web framework for building APIs
- **uvicorn** - ASGI server for running FastAPI
- **pydantic** - Data validation এবং type hints

### Standard Library:
- `os`, `time`, `hmac`, `hashlib`, `datetime`, `urllib.parse`, `typing`, `logging`

---

## 🎓 Learning Points

এই project থেকে শিখতে পারবেন:

### Backend Development:
1. **FastAPI** - Modern async web framework
2. **RESTful API Design** - Proper endpoint structure
3. **API Documentation** - Auto-generated Swagger/OpenAPI docs
4. **CORS Configuration** - Cross-origin resource sharing
5. **Middleware** - Request/response processing
6. **Error Handling** - Global exception handlers
7. **Logging** - Application logging best practices

### Architecture Patterns:
1. **Service Layer Pattern** - Business logic separation
2. **Repository Pattern** - Data access abstraction
3. **Configuration Management** - Environment-based settings
4. **Caching Strategy** - In-memory caching with TTL
5. **Type Safety** - Pydantic models and type hints

### API Integration:
1. **HMAC SHA256 Authentication** - Secure API authentication
2. **Signature Generation** - Request signing
3. **Timestamp Handling** - Time-based requests
4. **Rate Limiting** - API request throttling
5. **Error Recovery** - Graceful error handling

### Development Best Practices:
1. **Code Organization** - Modular project structure
2. **Environment Variables** - Secure credential management
3. **Virtual Environments** - Dependency isolation
4. **Documentation** - Comprehensive API docs
5. **Version Control** - Git best practices

## 🔮 Future Enhancements

এই features গুলো ভবিষ্যতে add করা যেতে পারে:

### Database Integration:
- [ ] SQLite/PostgreSQL integration
- [ ] Historical data storage
- [ ] Analytics and trends
- [ ] Order history tracking

### Advanced Features:
- [ ] Real-time websocket updates
- [ ] Email/SMS alerts for new orders
- [ ] Profit/loss tracking dashboard
- [ ] Multi-currency support
- [ ] User authentication and multi-user support
- [ ] API key management interface

### Performance:
- [ ] Redis caching instead of in-memory
- [ ] Background task queue (Celery)
- [ ] Pagination for large datasets
- [ ] GraphQL endpoint

### Monitoring:
- [ ] Prometheus metrics
- [ ] Health check endpoints
- [ ] Request logging to database
- [ ] Error tracking (Sentry integration)

---

## 📞 Support & Resources

### Binance API Documentation:
- **Official Docs:** https://binance-docs.github.io/apidocs/spot/en/
- **P2P API:** https://binance-docs.github.io/apidocs/spot/en/#c2c-endpoints

### FastAPI Documentation:
- **Official Docs:** https://fastapi.tiangolo.com/
- **Tutorial:** https://fastapi.tiangolo.com/tutorial/

### Questions?
যদি কোনো সমস্যা হয় বা প্রশ্ন থাকে, GitHub Issues তে জানান।

---

## 📄 License

This project is open source. Feel free to use and modify as needed.

---

**Made with ❤️ for Binance P2P Traders**

**Stack:** Python • FastAPI • Uvicorn • Pydantic • Binance API
