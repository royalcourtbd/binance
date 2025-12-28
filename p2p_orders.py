import os
import time
import hmac
import hashlib
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import urlencode

# .env file থেকে environment variables load করা
load_dotenv()

# API credentials
API_KEY = os.getenv('apiKey')
SECRET_KEY = os.getenv('secretKey')
BASE_URL = 'https://api.binance.com'


def create_signature(params, secret_key):
    """
    API request এর জন্য HMAC SHA256 signature তৈরি করা
    """
    query_string = urlencode(params)
    signature = hmac.new(
        secret_key.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature


def get_p2p_orders(days=30):
    """
    Last 30 days এর completed P2P orders fetch করা
    
    Parameters:
    -----------
    days : int
        কত দিনের orders দেখতে চান (default: 30)
    
    Returns:
    --------
    list : P2P orders এর list
    """
    # Endpoint
    endpoint = '/sapi/v1/c2c/orderMatch/listUserOrderHistory'
    url = BASE_URL + endpoint
    
    # Timestamp calculation - last 30 days
    current_time = int(time.time() * 1000)
    start_time = current_time - (days * 24 * 60 * 60 * 1000)
    
    # Parameters
    params = {
        'tradeType': 'BUY',  # BUY or SELL - উভয়ের জন্য আলাদা আলাদা call করতে হবে
        'timestamp': current_time,
        'startTimestamp': start_time
    }
    
    # Signature তৈরি করা
    params['signature'] = create_signature(params, SECRET_KEY)
    
    # Headers
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    
    try:
        # API request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None


def fetch_all_p2p_orders(days=30):
    """
    BUY এবং SELL উভয় type এর P2P orders fetch করা
    
    Parameters:
    -----------
    days : int
        কত দিনের orders দেখতে চান (default: 30)
    
    Returns:
    --------
    dict : {'buy_orders': [], 'sell_orders': []} format এ data
    """
    endpoint = '/sapi/v1/c2c/orderMatch/listUserOrderHistory'
    url = BASE_URL + endpoint
    
    # Timestamp calculation
    current_time = int(time.time() * 1000)
    start_time = current_time - (days * 24 * 60 * 60 * 1000)
    
    # Headers
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    
    all_orders = {
        'buy_orders': [],
        'sell_orders': []
    }
    
    # BUY orders fetch করা
    print("Fetching BUY orders...")
    buy_params = {
        'tradeType': 'BUY',
        'timestamp': current_time,
        'startTimestamp': start_time
    }
    buy_params['signature'] = create_signature(buy_params, SECRET_KEY)
    
    try:
        buy_response = requests.get(url, params=buy_params, headers=headers)
        buy_response.raise_for_status()
        buy_data = buy_response.json()
        if buy_data.get('data'):
            all_orders['buy_orders'] = buy_data['data']
    except requests.exceptions.RequestException as e:
        print(f"BUY orders fetch করতে error: {e}")
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
    
    # SELL orders fetch করা
    print("Fetching SELL orders...")
    current_time = int(time.time() * 1000)  # Fresh timestamp
    sell_params = {
        'tradeType': 'SELL',
        'timestamp': current_time,
        'startTimestamp': start_time
    }
    sell_params['signature'] = create_signature(sell_params, SECRET_KEY)
    
    try:
        sell_response = requests.get(url, params=sell_params, headers=headers)
        sell_response.raise_for_status()
        sell_data = sell_response.json()
        if sell_data.get('data'):
            all_orders['sell_orders'] = sell_data['data']
    except requests.exceptions.RequestException as e:
        print(f"SELL orders fetch করতে error: {e}")
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
    
    return all_orders


def display_order_details(order, order_type):
    """
    একটি order এর details beautifully display করা
    
    Parameters:
    -----------
    order : dict
        Order এর data
    order_type : str
        'BUY' or 'SELL'
    """
    print("\n" + "="*60)
    print(f"Order Type: {order_type}")
    print(f"Order Number: {order.get('orderNumber', 'N/A')}")
    print(f"Advertisement No: {order.get('advNo', 'N/A')}")
    print(f"Asset: {order.get('asset', 'N/A')}")
    print(f"Fiat: {order.get('fiat', 'N/A')} ({order.get('fiatSymbol', '')})")
    print(f"Amount: {order.get('amount', 'N/A')} {order.get('asset', '')}")
    print(f"Total Price: {order.get('totalPrice', 'N/A')} {order.get('fiat', '')}")
    print(f"Unit Price: {order.get('unitPrice', 'N/A')} {order.get('fiat', '')}/{order.get('asset', '')}")
    
    # Fee/Commission Details
    commission = order.get('commission', '0')
    taker_commission = order.get('takerCommission', '0')
    taker_commission_rate = order.get('takerCommissionRate', '0')
    print(f"\n💰 Fee Details:")
    print(f"   Commission: {commission} {order.get('asset', '')}")
    if float(taker_commission) > 0:
        print(f"   Taker Commission: {taker_commission} {order.get('asset', '')}")
        print(f"   Taker Commission Rate: {taker_commission_rate}%")
        print(f"   Taker Amount: {order.get('takerAmount', '0')} {order.get('asset', '')}")
    
    # Payment Method
    if order.get('payMethodName'):
        print(f"\n💳 Payment Method: {order.get('payMethodName')}")
    
    # Counterparty Info
    if order.get('counterPartNickName'):
        print(f"👤 Counterparty: {order.get('counterPartNickName')}")
    
    # Additional KYC
    if order.get('additionalKycVerify'):
        print(f"🔐 Additional KYC: Required")
    
    # Timestamp convert করা readable format এ
    if order.get('createTime'):
        create_time = datetime.fromtimestamp(order['createTime'] / 1000)
        print(f"\n⏰ Created: {create_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if order.get('orderStatus'):
        status_emoji = "✅" if order.get('orderStatus') == 'COMPLETED' else "❌"
        print(f"{status_emoji} Status: {order.get('orderStatus')}")
    
    print("="*60)


def main():
    """
    Main function - P2P orders fetch এবং display করা
    """
    print("\n🔄 Binance P2P Orders Fetching Started...")
    print(f"📅 Period: Last 30 days")
    if API_KEY:
        print(f"🔑 API Key: {API_KEY[:10]}... (loaded from .env)")
    print("\n")
    
    # Check করা API credentials আছে কিনা
    if not API_KEY or not SECRET_KEY:
        print("❌ Error: API Key অথবা Secret Key .env file এ পাওয়া যায়নি!")
        print("Please check your .env file.")
        return
    
    # P2P orders fetch করা
    orders_data = fetch_all_p2p_orders(days=30)
    
    # শুধুমাত্র COMPLETED orders filter করা
    buy_orders = orders_data.get('buy_orders', [])
    completed_buy_orders = [order for order in buy_orders if order.get('orderStatus') == 'COMPLETED']
    
    sell_orders = orders_data.get('sell_orders', [])
    completed_sell_orders = [order for order in sell_orders if order.get('orderStatus') == 'COMPLETED']
    
    # BUY orders display করা
    print(f"\n✅ Total Completed BUY Orders: {len(completed_buy_orders)}")
    if completed_buy_orders:
        print("\n📊 COMPLETED BUY ORDERS DETAILS:")
        for order in completed_buy_orders:
            display_order_details(order, 'BUY')
    else:
        print("কোনো completed BUY order পাওয়া যায়নি।")
    
    # SELL orders display করা
    print(f"\n✅ Total Completed SELL Orders: {len(completed_sell_orders)}")
    if completed_sell_orders:
        print("\n📊 COMPLETED SELL ORDERS DETAILS:")
        for order in completed_sell_orders:
            display_order_details(order, 'SELL')
    else:
        print("কোনো completed SELL order পাওয়া যায়নি।")
    
    # Calculate total fees and amounts
    total_buy_amount = sum(float(order.get('amount', 0)) for order in completed_buy_orders)
    total_sell_amount = sum(float(order.get('amount', 0)) for order in completed_sell_orders)
    total_buy_value = sum(float(order.get('totalPrice', 0)) for order in completed_buy_orders)
    total_sell_value = sum(float(order.get('totalPrice', 0)) for order in completed_sell_orders)
    total_buy_fees = sum(float(order.get('commission', 0)) for order in completed_buy_orders)
    total_sell_fees = sum(float(order.get('commission', 0)) for order in completed_sell_orders)
    
    # Summary
    print("\n" + "="*60)
    print("📈 SUMMARY:")
    print(f"\n💵 BUY Orders:")
    print(f"   Count: {len(completed_buy_orders)}")
    print(f"   Total Amount: {total_buy_amount:.2f} USDT")
    print(f"   Total Value: {total_buy_value:.2f} BDT")
    print(f"   Total Fees: {total_buy_fees:.2f} USDT")
    if completed_buy_orders:
        avg_buy_price = total_buy_value / total_buy_amount if total_buy_amount > 0 else 0
        print(f"   Average Price: {avg_buy_price:.2f} BDT/USDT")
    
    print(f"\n💸 SELL Orders:")
    print(f"   Count: {len(completed_sell_orders)}")
    print(f"   Total Amount: {total_sell_amount:.2f} USDT")
    print(f"   Total Value: {total_sell_value:.2f} BDT")
    print(f"   Total Fees: {total_sell_fees:.2f} USDT")
    if completed_sell_orders:
        avg_sell_price = total_sell_value / total_sell_amount if total_sell_amount > 0 else 0
        print(f"   Average Price: {avg_sell_price:.2f} BDT/USDT")
    
    print(f"\n📊 Overall:")
    print(f"   Total Completed Orders: {len(completed_buy_orders) + len(completed_sell_orders)}")
    print(f"   Total All Orders (including cancelled): {len(buy_orders) + len(sell_orders)}")
    print(f"   Total Fees Paid: {total_buy_fees + total_sell_fees:.2f} USDT")
    
    # Net profit/loss calculation
    if total_buy_amount > 0 and total_sell_amount > 0:
        net_profit_bdt = total_sell_value - total_buy_value
        net_profit_percentage = (net_profit_bdt / total_buy_value * 100) if total_buy_value > 0 else 0
        print(f"\n💰 Net Profit/Loss:")
        profit_emoji = "🟢" if net_profit_bdt >= 0 else "🔴"
        print(f"   {profit_emoji} P&L: {net_profit_bdt:.2f} BDT ({net_profit_percentage:.2f}%)")
    
    print("="*60)


if __name__ == "__main__":
    main()
