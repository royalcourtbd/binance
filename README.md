# Binance P2P Orders Tracker

## 📌 Overview

এই project টি Binance P2P trading এর completed orders track করার জন্য তৈরি করা হয়েছে। এটি আপনার last 30 days এর সমস্ত completed BUY এবং SELL orders fetch করে এবং details সহ display করে।

## 🔧 Features

- ✅ Last 30 days এর সব completed P2P orders fetch করা
- ✅ BUY এবং SELL orders আলাদাভাবে display করা
- ✅ Order details: Amount, Price, Unit Price, Timestamp, Status
- ✅ Secure API authentication using HMAC SHA256 signature
- ✅ Environment variables থেকে API credentials load করা
- ✅ Beautiful console output with Bangla text

## 📁 Project Structure

```
binance/
├── .env                 # API credentials (gitignore করা)
├── p2p_orders.py       # Main Python script
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## 🚀 Setup Instructions

### 1. Dependencies Install করা

```bash
pip install -r requirements.txt
```

অথবা manually:

```bash
pip install requests python-dotenv
```

### 2. Environment Variables Setup

`.env` file এ আপনার Binance API credentials add করুন:

```
apiKey=YOUR_API_KEY_HERE
secretKey=YOUR_SECRET_KEY_HERE
```

**⚠️ Security Note:** `.env` file টি কখনো public repository তে push করবেন না!

### 3. Script Run করা

```bash
python3 p2p_orders.py
```

## 🎯 Code Explanation

### Main Functions:

#### 1. `create_signature(params, secret_key)`

- Binance API request এর জন্য HMAC SHA256 signature তৈরি করে
- Security এর জন্য প্রতিটি request এ unique signature লাগে

#### 2. `fetch_all_p2p_orders(days=30)`

- BUY এবং SELL উভয় type এর orders fetch করে
- Last 30 days এর data retrieve করে
- API response থেকে orders data extract করে

#### 3. `display_order_details(order, order_type)`

- একটি order এর সব details beautifully format করে display করে
- Timestamp কে human-readable format এ convert করে

#### 4. `main()`

- Complete workflow orchestrate করে:
  1. API credentials verify করা
  2. Orders fetch করা
  3. Completed orders filter করা
  4. Details display করা
  5. Summary দেখানো

## 📊 Output Example

```
🔄 Binance P2P Orders Fetching Started...
📅 Period: Last 30 days
🔑 API Key: TWZIN3cMLP... (loaded from .env)

✅ Total Completed BUY Orders: 3
✅ Total Completed SELL Orders: 3

📈 SUMMARY:
   Total Completed BUY Orders: 3
   Total Completed SELL Orders: 3
   Total Completed Orders: 6
   Total All Orders (including cancelled): 10
```

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

## 📝 Customization

### Different Time Period

Script এ days parameter change করতে পারেন:

```python
orders_data = fetch_all_p2p_orders(days=7)  # Last 7 days
```

### Filter by Status

অন্য status এর orders দেখতে চাইলে filter modify করুন:

```python
cancelled_orders = [order for order in orders if order.get('orderStatus') == 'CANCELLED']
```

## ⚠️ Important Notes

1. API Key এবং Secret Key secure রাখুন
2. `.env` file কখনো commit করবেন না
3. API rate limits খেয়াল রাখুন
4. Orders data sensitive, careful handle করুন

## 🐛 Troubleshooting

### API Error

যদি API error আসে, check করুন:

- API Key এবং Secret Key সঠিক আছে কিনা
- API permissions enabled আছে কিনা (P2P Trading)
- Internet connection ঠিক আছে কিনা

### No Orders Found

যদি কোনো orders না পায়:

- Last 30 days এ আসলেই কোনো P2P trade হয়েছে কিনা check করুন
- Time period increase করে দেখুন
- Binance account এ manually check করুন

## 📚 Dependencies

- `requests`: HTTP requests এর জন্য
- `python-dotenv`: Environment variables load করার জন্য
- Standard library: `os`, `time`, `hmac`, `hashlib`, `datetime`, `urllib.parse`

## 🎓 Learning Points

এই project থেকে শিখতে পারবেন:

1. REST API authentication (HMAC SHA256)
2. Environment variables ব্যবহার
3. Timestamp handling
4. Data filtering এবং processing
5. Console output formatting
6. Error handling

## 📞 Support

কোনো সমস্যা হলে Binance API documentation check করুন:
https://binance-docs.github.io/apidocs/spot/en/

---

**Made with ❤️ for Binance P2P Traders**
