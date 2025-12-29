import time
import hmac
import hashlib
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urlencode

from app.core.config import settings
from app.core.cache import cache


class BinanceP2PService:
    """Service for interacting with Binance P2P API"""

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.api_key = settings.API_KEY
        self.secret_key = settings.SECRET_KEY
        self.endpoint = '/sapi/v1/c2c/orderMatch/listUserOrderHistory'

    def _create_signature(self, params: Dict[str, Any]) -> str:
        """
        Create HMAC SHA256 signature for API request

        Parameters:
        -----------
        params : dict
            Request parameters

        Returns:
        --------
        str : HMAC SHA256 signature
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make authenticated request to Binance API

        Parameters:
        -----------
        params : dict
            Request parameters

        Returns:
        --------
        dict or None : API response data or None if error
        """
        url = self.base_url + self.endpoint

        # Add signature
        params['signature'] = self._create_signature(params)

        # Headers
        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Binance API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = f"Binance API error: {error_data.get('msg', str(e))}"
                except Exception:
                    error_msg = f"Binance API error: {e.response.text}"
            raise Exception(error_msg)

    def get_orders(
        self,
        trade_type: str,
        days: int = 30,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch P2P orders by trade type

        Parameters:
        -----------
        trade_type : str
            'BUY' or 'SELL'
        days : int
            Number of days to fetch (default: 30)
        use_cache : bool
            Whether to use cached data (default: True)

        Returns:
        --------
        list : List of orders
        """
        # Check cache first
        cache_key = f"p2p_orders_{trade_type.lower()}_{days}"
        if use_cache:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        # Calculate timestamps
        current_time = int(time.time() * 1000)
        start_time = current_time - (days * 24 * 60 * 60 * 1000)

        # Request parameters
        params = {
            'tradeType': trade_type.upper(),
            'timestamp': current_time,
            'startTimestamp': start_time
        }

        # Make API request
        response_data = self._make_request(params)

        # Extract orders from response
        orders = []
        if response_data and 'data' in response_data:
            orders = response_data['data']

        # Cache the result
        if use_cache:
            cache.set(cache_key, orders, ttl=settings.CACHE_TTL)

        return orders

    def get_all_orders(
        self,
        days: int = 30,
        use_cache: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch both BUY and SELL orders

        Parameters:
        -----------
        days : int
            Number of days to fetch (default: 30)
        use_cache : bool
            Whether to use cached data (default: True)

        Returns:
        --------
        dict : {'buy_orders': [...], 'sell_orders': [...]}
        """
        buy_orders = self.get_orders('BUY', days, use_cache)
        sell_orders = self.get_orders('SELL', days, use_cache)

        return {
            'buy_orders': buy_orders,
            'sell_orders': sell_orders
        }

    def get_completed_orders(
        self,
        trade_type: Optional[str] = None,
        days: int = 30,
        use_cache: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch only completed orders

        Parameters:
        -----------
        trade_type : str or None
            'BUY', 'SELL', or None for both
        days : int
            Number of days to fetch (default: 30)
        use_cache : bool
            Whether to use cached data (default: True)

        Returns:
        --------
        dict : Completed orders by type
        """
        if trade_type:
            orders = self.get_orders(trade_type, days, use_cache)
            completed = [order for order in orders if order.get('orderStatus') == 'COMPLETED']
            return {f'{trade_type.lower()}_orders': completed}

        # Get both types
        all_orders = self.get_all_orders(days, use_cache)

        completed_buy = [
            order for order in all_orders['buy_orders']
            if order.get('orderStatus') == 'COMPLETED'
        ]
        completed_sell = [
            order for order in all_orders['sell_orders']
            if order.get('orderStatus') == 'COMPLETED'
        ]

        return {
            'buy_orders': completed_buy,
            'sell_orders': completed_sell
        }

    def calculate_summary(
        self,
        buy_orders: List[Dict[str, Any]],
        sell_orders: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate summary statistics from orders

        Parameters:
        -----------
        buy_orders : list
            List of buy orders
        sell_orders : list
            List of sell orders

        Returns:
        --------
        dict : Summary statistics
        """
        # Calculate totals
        total_buy_amount = sum(float(order.get('amount', 0)) for order in buy_orders)
        total_sell_amount = sum(float(order.get('amount', 0)) for order in sell_orders)
        total_buy_value = sum(float(order.get('totalPrice', 0)) for order in buy_orders)
        total_sell_value = sum(float(order.get('totalPrice', 0)) for order in sell_orders)
        total_buy_fees = sum(float(order.get('commission', 0)) for order in buy_orders)
        total_sell_fees = sum(float(order.get('commission', 0)) for order in sell_orders)

        # Calculate averages
        avg_buy_price = None
        if total_buy_amount > 0:
            avg_buy_price = total_buy_value / total_buy_amount

        avg_sell_price = None
        if total_sell_amount > 0:
            avg_sell_price = total_sell_value / total_sell_amount

        # Calculate profit/loss
        net_profit_bdt = None
        net_profit_percentage = None
        if total_buy_amount > 0 and total_sell_amount > 0:
            net_profit_bdt = total_sell_value - total_buy_value
            if total_buy_value > 0:
                net_profit_percentage = (net_profit_bdt / total_buy_value) * 100

        return {
            'total_buy_orders': len(buy_orders),
            'total_sell_orders': len(sell_orders),
            'total_completed_orders': len(buy_orders) + len(sell_orders),
            'total_buy_amount': round(total_buy_amount, 2),
            'total_sell_amount': round(total_sell_amount, 2),
            'total_buy_value': round(total_buy_value, 2),
            'total_sell_value': round(total_sell_value, 2),
            'total_buy_fees': round(total_buy_fees, 2),
            'total_sell_fees': round(total_sell_fees, 2),
            'total_fees': round(total_buy_fees + total_sell_fees, 2),
            'average_buy_price': round(avg_buy_price, 2) if avg_buy_price else None,
            'average_sell_price': round(avg_sell_price, 2) if avg_sell_price else None,
            'net_profit_bdt': round(net_profit_bdt, 2) if net_profit_bdt is not None else None,
            'net_profit_percentage': round(net_profit_percentage, 2) if net_profit_percentage is not None else None
        }

    def clear_cache(self) -> None:
        """Clear all cached order data"""
        cache.clear()


# Global service instance
binance_service = BinanceP2PService()
