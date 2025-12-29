from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.services.binance_service import binance_service
from app.models.schemas import (
    OrdersResponse,
    SummaryResponse,
    CacheStatsResponse,
    P2POrder,
    OrdersSummary
)
from app.core.cache import cache

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/buy", response_model=OrdersResponse)
async def get_buy_orders(
    days: int = Query(default=30, ge=1, le=90, description="Number of days to fetch (1-90)"),
    use_cache: bool = Query(default=True, description="Use cached data if available")
):
    """
    Fetch BUY orders from Binance P2P

    - **days**: Number of days to fetch (1-90)
    - **use_cache**: Whether to use cached data
    """
    try:
        orders = binance_service.get_orders('BUY', days=days, use_cache=use_cache)

        # Check if data came from cache
        cache_key = f"p2p_orders_buy_{days}"
        is_cached = cache.get(cache_key) is not None

        return OrdersResponse(
            success=True,
            message=f"Successfully fetched {len(orders)} BUY orders",
            data=[P2POrder(**order) for order in orders],
            count=len(orders),
            trade_type="BUY",
            cached=is_cached and use_cache
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sell", response_model=OrdersResponse)
async def get_sell_orders(
    days: int = Query(default=30, ge=1, le=90, description="Number of days to fetch (1-90)"),
    use_cache: bool = Query(default=True, description="Use cached data if available")
):
    """
    Fetch SELL orders from Binance P2P

    - **days**: Number of days to fetch (1-90)
    - **use_cache**: Whether to use cached data
    """
    try:
        orders = binance_service.get_orders('SELL', days=days, use_cache=use_cache)

        # Check if data came from cache
        cache_key = f"p2p_orders_sell_{days}"
        is_cached = cache.get(cache_key) is not None

        return OrdersResponse(
            success=True,
            message=f"Successfully fetched {len(orders)} SELL orders",
            data=[P2POrder(**order) for order in orders],
            count=len(orders),
            trade_type="SELL",
            cached=is_cached and use_cache
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=dict)
async def get_all_orders(
    days: int = Query(default=30, ge=1, le=90, description="Number of days to fetch (1-90)"),
    use_cache: bool = Query(default=True, description="Use cached data if available")
):
    """
    Fetch both BUY and SELL orders from Binance P2P

    - **days**: Number of days to fetch (1-90)
    - **use_cache**: Whether to use cached data
    """
    try:
        all_orders = binance_service.get_all_orders(days=days, use_cache=use_cache)

        return {
            "success": True,
            "message": f"Successfully fetched all orders",
            "data": {
                "buy_orders": [P2POrder(**order).dict() for order in all_orders['buy_orders']],
                "sell_orders": [P2POrder(**order).dict() for order in all_orders['sell_orders']]
            },
            "count": {
                "buy": len(all_orders['buy_orders']),
                "sell": len(all_orders['sell_orders']),
                "total": len(all_orders['buy_orders']) + len(all_orders['sell_orders'])
            },
            "cached": use_cache
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/completed", response_model=dict)
async def get_completed_orders(
    trade_type: Optional[str] = Query(
        default=None,
        description="Trade type: 'BUY', 'SELL', or None for both"
    ),
    days: int = Query(default=30, ge=1, le=90, description="Number of days to fetch (1-90)"),
    use_cache: bool = Query(default=True, description="Use cached data if available")
):
    """
    Fetch only COMPLETED orders from Binance P2P

    - **trade_type**: 'BUY', 'SELL', or None for both
    - **days**: Number of days to fetch (1-90)
    - **use_cache**: Whether to use cached data
    """
    try:
        # Validate trade_type if provided
        if trade_type and trade_type.upper() not in ['BUY', 'SELL']:
            raise HTTPException(
                status_code=400,
                detail="trade_type must be 'BUY' or 'SELL'"
            )

        completed_orders = binance_service.get_completed_orders(
            trade_type=trade_type.upper() if trade_type else None,
            days=days,
            use_cache=use_cache
        )

        # Format response
        if trade_type:
            order_list = completed_orders.get(f'{trade_type.lower()}_orders', [])
            return {
                "success": True,
                "message": f"Successfully fetched {len(order_list)} completed {trade_type.upper()} orders",
                "data": [P2POrder(**order).dict() for order in order_list],
                "count": len(order_list),
                "trade_type": trade_type.upper(),
                "cached": use_cache
            }
        else:
            return {
                "success": True,
                "message": "Successfully fetched all completed orders",
                "data": {
                    "buy_orders": [P2POrder(**order).dict() for order in completed_orders['buy_orders']],
                    "sell_orders": [P2POrder(**order).dict() for order in completed_orders['sell_orders']]
                },
                "count": {
                    "buy": len(completed_orders['buy_orders']),
                    "sell": len(completed_orders['sell_orders']),
                    "total": len(completed_orders['buy_orders']) + len(completed_orders['sell_orders'])
                },
                "cached": use_cache
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary", response_model=SummaryResponse)
async def get_orders_summary(
    days: int = Query(default=30, ge=1, le=90, description="Number of days to fetch (1-90)"),
    use_cache: bool = Query(default=True, description="Use cached data if available")
):
    """
    Get summary statistics of P2P orders

    - **days**: Number of days to fetch (1-90)
    - **use_cache**: Whether to use cached data

    Returns total amounts, fees, average prices, and profit/loss calculations
    """
    try:
        # Get completed orders
        completed_orders = binance_service.get_completed_orders(
            trade_type=None,
            days=days,
            use_cache=use_cache
        )

        # Calculate summary
        summary = binance_service.calculate_summary(
            buy_orders=completed_orders['buy_orders'],
            sell_orders=completed_orders['sell_orders']
        )

        return SummaryResponse(
            success=True,
            message="Summary calculated successfully",
            data=OrdersSummary(**summary),
            cached=use_cache
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cache")
async def clear_cache():
    """
    Clear all cached order data

    This will force fresh data to be fetched from Binance API on next request
    """
    try:
        binance_service.clear_cache()
        return {
            "success": True,
            "message": "Cache cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats", response_model=CacheStatsResponse)
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = cache.get_stats()
        return CacheStatsResponse(
            success=True,
            message="Cache stats retrieved successfully",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
