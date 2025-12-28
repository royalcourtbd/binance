# 🚀 Quick Start Guide - Binance P2P Tracker

## ⚡ 5-Minute Setup

### Step 1: Dependencies Install করুন

```bash
pip install -r requirements.txt
```

### Step 2: API Credentials Setup করুন

1. `.env.example` file টি copy করে `.env` নামে rename করুন
2. Binance account থেকে API Key এবং Secret Key নিন
3. `.env` file এ paste করুন

```bash
cp .env.example .env
nano .env  # অথবা যেকোনো text editor দিয়ে edit করুন
```

### Step 3: Script Run করুন

```bash
python3 p2p_orders.py
```

That's it! 🎉

---

## 📝 Basic Commands

### Default (Last 30 days, all completed orders)

```bash
python3 p2p_orders.py
```

### Custom Time Period (কোড modify করে)

```python
# p2p_orders.py এর main() function এ change করুন:
orders_data = fetch_all_p2p_orders(days=7)  # Last 7 days
```

---

## 🔧 Troubleshooting - সমস্যা সমাধান

### ❌ Problem: "API Key পাওয়া যায়নি"

**Solution:**

1. Check করুন `.env` file আছে কিনা
2. File name ঠিক আছে কিনা (`.env`, not `.env.txt`)
3. API key এবং secret key সঠিকভাবে paste করেছেন কিনা
4. Extra spaces নেই কিনা

### ❌ Problem: "Invalid signature"

**Solution:**

1. Secret key সঠিক আছে কিনা double-check করুন
2. `.env` file এ কোনো extra space বা newline নেই কিনা verify করুন
3. API key এর permissions check করুন Binance এ

### ❌ Problem: "Module not found"

**Solution:**

```bash
pip install requests python-dotenv
# অথবা
pip install -r requirements.txt
```

### ❌ Problem: "No orders found"

**Possible Reasons:**

1. Last 30 days এ কোনো P2P trade হয়নি
2. API permissions সঠিক নয়
3. Time period বাড়িয়ে দেখুন (e.g., 60 days)

---

## 📊 Output Explanation

### Order Details যা Display হয়:

```
Order Type: BUY/SELL
Order Number: Unique order ID
Asset: যা trade করেছেন (e.g., USDT)
Fiat: যা দিয়ে কিনেছেন/বেচেছেন (e.g., BDT)
Amount: কত crypto
Total Price: মোট দাম
Unit Price: per unit দাম
Created: কখন order হয়েছিল
Status: COMPLETED/CANCELLED etc.
```

### Summary Section:

- Total Completed BUY Orders: কতগুলো BUY order সম্পন্ন হয়েছে
- Total Completed SELL Orders: কতগুলো SELL order সম্পন্ন হয়েছে
- Total Completed Orders: মোট সম্পন্ন orders
- Total All Orders: সব orders including cancelled

---

## 🔐 Security Tips

### ✅ DO:

- `.env` file কে `.gitignore` এ রাখুন
- API Key তে শুধু প্রয়োজনীয় permissions enable করুন
- Regular interval এ API key rotate করুন
- Secret key কখনো share করবেন না

### ❌ DON'T:

- `.env` file commit করবেন না
- API credentials screenshot share করবেন না
- Public repositories তে credentials push করবেন না
- Withdrawal permission enable করবেন না (unless absolutely needed)

---

## 📚 File Structure

```
binance/
├── .env                    # Your API credentials (SECRET!)
├── .env.example           # Template file for setup
├── .gitignore            # Prevents committing sensitive files
├── p2p_orders.py         # Main script
├── requirements.txt      # Python dependencies
├── README.md            # Full documentation
├── ANALYSIS.md          # Deep technical analysis
└── QUICKSTART.md        # This file
```

---

## 🎯 Common Use Cases

### 1. Daily Check করতে চাই

```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * cd /path/to/binance && python3 p2p_orders.py > daily_report.txt
```

### 2. Weekly Summary চাই

```python
# Modify main() function:
orders_data = fetch_all_p2p_orders(days=7)
```

### 3. Specific Date Range চাই

```python
# এটা future enhancement - currently fixed time period
# ANALYSIS.md file এ implementation ideas আছে
```

---

## 💡 Pro Tips

### Tip 1: Output Save করুন

```bash
python3 p2p_orders.py > report.txt
python3 p2p_orders.py | tee report_$(date +%Y%m%d).txt
```

### Tip 2: Quick Check Without Full Output

```python
# main() function এ এই line টা comment out করুন:
# display_order_details(order, 'BUY')
# শুধু summary দেখাবে
```

### Tip 3: Different Currencies Track করুন

```python
# Currently auto-detects all currencies
# Filter করতে চাইলে:
buy_orders = [o for o in buy_orders if o['fiat'] == 'BDT']
```

### Tip 4: Price Monitoring

```python
# Average price calculate করতে:
avg_buy_price = sum(float(o['unitPrice']) for o in buy_orders) / len(buy_orders)
print(f"Average BUY price: {avg_buy_price:.2f}")
```

---

## 🔗 Useful Links

- **Binance API Docs:** https://binance-docs.github.io/apidocs/
- **Python Requests:** https://docs.python-requests.org/
- **python-dotenv:** https://pypi.org/project/python-dotenv/
- **Project GitHub:** [Your Repo URL]

---

## 🆘 Need Help?

### Check These First:

1. ✅ Python 3.6+ installed?
2. ✅ Dependencies installed?
3. ✅ `.env` file properly configured?
4. ✅ Internet connection working?
5. ✅ Binance API working? (check status.binance.com)

### Still Having Issues?

1. Read the full [README.md](README.md)
2. Check [ANALYSIS.md](ANALYSIS.md) for technical details
3. Enable debug mode:
   ```python
   # Add this at the top of p2p_orders.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## ⚙️ Customization Examples

### Example 1: Only BUY Orders চাই

```python
# main() function এ:
# SELL orders section টা comment out করে দিন
```

### Example 2: Minimum Amount Filter

```python
# display করার আগে filter করুন:
buy_orders = [o for o in buy_orders if float(o['amount']) >= 10]
```

### Example 3: Today's Orders Only

```python
from datetime import datetime, timedelta

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
today_timestamp = int(today.timestamp() * 1000)

buy_orders = [o for o in buy_orders if o['createTime'] >= today_timestamp]
```

---

## 📈 Next Steps

একবার basic setup কাজ করছে, তখন explore করতে পারেন:

1. **📊 Statistics:** ANALYSIS.md এর statistics section দেখুন
2. **📁 Export:** CSV/Excel export functionality add করুন
3. **📧 Alerts:** Price alert system implement করুন
4. **🌐 Dashboard:** Web-based dashboard তৈরি করুন
5. **💾 Database:** Historical data store করার জন্য database integration

সব implementation ideas [ANALYSIS.md](ANALYSIS.md) file এ পাবেন!

---

**Ready to track your P2P trades? Let's go! 🚀**
