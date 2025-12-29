# 🚀 Quick Setup Guide

আপনার backend server চালু করার জন্য এই steps follow করুন:

## ⚡ Quick Start (3 Steps)

### 1️⃣ Virtual Environment তৈরি করুন

```bash
python3 -m venv .venv
```

### 2️⃣ Virtual Environment Activate করুন

**Mac/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

আপনার terminal এ `(.venv)` দেখা যাবে - এটা activate হয়েছে বুঝায়।

### 3️⃣ Dependencies Install করুন

```bash
pip install -r requirements.txt
```

এটা install করবে:
- ✅ FastAPI
- ✅ Uvicorn
- ✅ Pydantic
- ✅ Requests
- ✅ Python-dotenv

---

## 🎯 Server চালু করুন

এখন server start করতে পারবেন:

```bash
# Method 1: Startup script use করুন (Recommended)
./start_server.sh          # Mac/Linux
start_server.bat           # Windows

# Method 2: Direct command
python -m app.main

# Method 3: Uvicorn command
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Verify Installation

Server চালু হলে browser এ এই URLs visit করুন:

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **ReDoc:** http://localhost:8000/redoc

---

## 🔧 .env File Setup (প্রথমবার করতে হবে)

1. `.env.example` copy করুন:
   ```bash
   cp .env.example .env
   ```

2. `.env` file edit করে আপনার Binance API credentials দিন:
   ```env
   apiKey=YOUR_ACTUAL_API_KEY
   secretKey=YOUR_ACTUAL_SECRET_KEY
   ```

---

## 🐛 Common Issues

### Issue: "No module named 'fastapi'"

**Solution:** Virtual environment activate করে dependencies install করুন:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: ".env file not found"

**Solution:** `.env` file তৈরি করুন:
```bash
cp .env.example .env
# Then edit .env with your API keys
```

### Issue: "Permission denied: ./start_server.sh"

**Solution:** Script executable করুন:
```bash
chmod +x start_server.sh
```

---

## 📝 Next Steps

Server চালু হওয়ার পর:

1. ✅ http://localhost:8000/docs তে যান
2. ✅ "Try it out" button click করে endpoints test করুন
3. ✅ আপনার frontend থেকে API call করুন

---

**Need Help?** Full documentation: [README.md](README.md)
