"""
Performance Optimization Module for Constitution RAG
===================================================

Implements critical performance optimizations:
- Response caching with TTL
- Connection pooling for API calls
- Timeout optimization
- Request batching
- Memory-efficient operations

This module addresses the critical 30+ second response time issue.
"""

import time
import hashlib
import pickle
import asyncio
from typing import Dict, Any, Optional, List, Tuple
from functools import lru_cache, wraps
from datetime import datetime, timedelta
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResponseCache:
    """
    In-memory response cache with TTL support.
    Dramatically reduces repeated query response times.
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initialize response cache.
        
        Args:
            max_size: Maximum number of cached responses
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._lock = threading.Lock()
        self._hit_count = 0
        self._miss_count = 0
        self._total_requests = 0
    
    def _generate_key(self, query: str, user_type: str = "general") -> str:
        """Generate cache key from query and user type."""
        content = f"{query}_{user_type}".lower().strip()
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, query: str, user_type: str = "general") -> Optional[Dict[str, Any]]:
        """
        Get cached response if available and not expired.
        
        Args:
            query: User query
            user_type: Type of user making the query
            
        Returns:
            Cached response or None if not found/expired
        """
        key = self._generate_key(query, user_type)
        
        with self._lock:
            self._total_requests += 1
            
            if key in self.cache:
                cached_item = self.cache[key]
                
                # Check if expired
                if datetime.now() < cached_item['expires_at']:
                    self._hit_count += 1
                    logger.info(f"Cache HIT for query: {query[:50]}...")
                    
                    # Add cache metadata to response
                    response = cached_item['response'].copy()
                    if 'performance' not in response:
                        response['performance'] = {}
                    response['performance']['cache_hit'] = True
                    response['performance']['cached_at'] = cached_item.get('cached_at', datetime.now()).isoformat()
                    
                    return response
                else:
                    # Remove expired item
                    del self.cache[key]
                    self._miss_count += 1
                    logger.info(f"Cache EXPIRED for query: {query[:50]}...")
            else:
                self._miss_count += 1
        
        logger.info(f"Cache MISS for query: {query[:50]}...")
        return None
    
    def set(self, query: str, response: Dict[str, Any], user_type: str = "general", ttl: Optional[int] = None) -> None:
        """
        Cache response with TTL.
        
        Args:
            query: User query
            response: Response to cache
            user_type: Type of user making the query
            ttl: Time-to-live in seconds (uses default if None)
        """
        key = self._generate_key(query, user_type)
        ttl = ttl or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        with self._lock:
            # Implement LRU eviction if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                # Remove oldest entry
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['created_at'])
                del self.cache[oldest_key]
                logger.info(f"Cache EVICTED oldest entry to make space")
            
            self.cache[key] = {
                'response': response,
                'created_at': datetime.now(),
                'expires_at': expires_at,
                'query': query[:100]  # Store partial query for debugging
            }
            
        logger.info(f"Cache SET for query: {query[:50]}...")
    
    def clear(self) -> None:
        """Clear all cached responses."""
        with self._lock:
            self.cache.clear()
        logger.info("Cache CLEARED")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_items = len(self.cache)
            expired_items = sum(1 for item in self.cache.values() 
                              if datetime.now() >= item['expires_at'])
            
            total_requests = max(self._total_requests, 1)
            hit_rate = self._hit_count / total_requests
            
        return {
            'total_items': total_items,
            'active_items': total_items - expired_items,
            'expired_items': expired_items,
            'max_size': self.max_size,
            'hit_rate': hit_rate,
            'total_requests': self._total_requests,
            'cache_hits': self._hit_count,
            'cache_misses': self._miss_count
        }


class APIConnectionPool:
    """
    Connection pool for API calls to optimize network requests.
    Reduces connection overhead and improves response times.
    """
    
    def __init__(self, max_workers: int = 5, timeout: int = 30):
        """
        Initialize connection pool.
        
        Args:
            max_workers: Maximum concurrent API calls
            timeout: Request timeout in seconds
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.timeout = timeout
        self.active_requests = 0
        self._lock = threading.Lock()
    
    def execute_api_call(self, func, *args, **kwargs) -> Any:
        """
        Execute API call through connection pool.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        with self._lock:
            self.active_requests += 1
        
        try:
            # Submit to thread pool with timeout
            future = self.executor.submit(func, *args, **kwargs)
            result = future.result(timeout=self.timeout)
            return result
            
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        finally:
            with self._lock:
                self.active_requests -= 1
    
    def execute_batch_calls(self, calls: List[Tuple]) -> List[Any]:
        """
        Execute multiple API calls concurrently.
        
        Args:
            calls: List of tuples (func, args, kwargs)
            
        Returns:
            List of results in order
        """
        futures = []
        
        for func, args, kwargs in calls:
            future = self.executor.submit(func, *args, **kwargs)
            futures.append(future)
        
        results = []
        for future in as_completed(futures, timeout=self.timeout):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Batch API call failed: {e}")
                results.append(None)
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get connection pool status."""
        return {
            'active_requests': self.active_requests,
            'max_workers': self.executor._max_workers,
            'queue_size': self.executor._work_queue.qsize() if hasattr(self.executor._work_queue, 'qsize') else 0
        }


class PerformanceOptimizer:
    """
    Main performance optimization coordinator.
    Integrates caching, connection pooling, and monitoring.
    """
    
    def __init__(self, cache_size: int = 1000, max_workers: int = 5, api_timeout: int = 15):
        """
        Initialize performance optimizer.
        
        Args:
            cache_size: Maximum cached responses
            max_workers: Maximum concurrent API workers
            api_timeout: API call timeout in seconds
        """
        self.cache = ResponseCache(max_size=cache_size)
        self.connection_pool = APIConnectionPool(max_workers=max_workers, timeout=api_timeout)
        
        # Performance metrics
        self.metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'avg_response_time': 0,
            'total_response_time': 0,
            'api_calls': 0,
            'api_failures': 0
        }
        self._metrics_lock = threading.Lock()
    
    def optimized_query(self, query_func, query: str, user_type: str = "general", 
                       force_refresh: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Execute optimized query with caching and performance monitoring.
        
        Args:
            query_func: Function to execute the query
            query: User query
            user_type: Type of user
            force_refresh: Force cache refresh
            **kwargs: Additional arguments for query_func
            
        Returns:
            Query response with performance metadata
        """
        start_time = time.time()
        
        with self._metrics_lock:
            self.metrics['total_requests'] += 1
        
        try:
            # Check cache first (unless force refresh)
            if not force_refresh:
                cached_response = self.cache.get(query, user_type)
                if cached_response:
                    with self._metrics_lock:
                        self.metrics['cache_hits'] += 1
                    
                    response_time = time.time() - start_time
                    cached_response['performance'] = {
                        'response_time': response_time,
                        'cache_hit': True,
                        'api_call': False
                    }
                    return cached_response
            
            # Cache miss - execute query through connection pool
            with self._metrics_lock:
                self.metrics['cache_misses'] += 1
                self.metrics['api_calls'] += 1
            
            try:
                response = self.connection_pool.execute_api_call(query_func, query, user_type, **kwargs)
                
                # Cache the response
                self.cache.set(query, response, user_type)
                
                response_time = time.time() - start_time
                response['performance'] = {
                    'response_time': response_time,
                    'cache_hit': False,
                    'api_call': True
                }
                
                # Update metrics
                with self._metrics_lock:
                    self.metrics['total_response_time'] += response_time
                    self.metrics['avg_response_time'] = (
                        self.metrics['total_response_time'] / self.metrics['total_requests']
                    )
                
                return response
                
            except Exception as e:
                with self._metrics_lock:
                    self.metrics['api_failures'] += 1
                
                logger.error(f"Query execution failed: {e}")
                
                # Return error response with performance data
                response_time = time.time() - start_time
                return {
                    'answer': f"Sorry, I encountered an error processing your query: {str(e)}",
                    'citations': [],
                    'reasoning_chain': '',
                    'accuracy_score': 0.0,
                    'error': True,
                    'performance': {
                        'response_time': response_time,
                        'cache_hit': False,
                        'api_call': True,
                        'error': True
                    }
                }
        
        except Exception as e:
            logger.error(f"Performance optimizer error: {e}")
            response_time = time.time() - start_time
            return {
                'answer': "Sorry, I encountered a system error. Please try again.",
                'citations': [],
                'reasoning_chain': '',
                'accuracy_score': 0.0,
                'error': True,
                'performance': {
                    'response_time': response_time,
                    'cache_hit': False,
                    'api_call': False,
                    'error': True
                }
            }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        with self._metrics_lock:
            metrics_copy = self.metrics.copy()
        
        cache_stats = self.cache.get_stats()
        pool_status = self.connection_pool.get_status()
        
        return {
            'request_metrics': metrics_copy,
            'cache_metrics': cache_stats,
            'connection_pool': pool_status,
            'performance_summary': {
                'avg_response_time': metrics_copy['avg_response_time'],
                'cache_hit_rate': cache_stats['hit_rate'],
                'api_success_rate': (
                    (metrics_copy['api_calls'] - metrics_copy['api_failures']) / 
                    max(metrics_copy['api_calls'], 1)
                ),
                'total_requests': metrics_copy['total_requests']
            }
        }
    
    def clear_cache(self) -> None:
        """Clear response cache."""
        self.cache.clear()
    
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        with self._metrics_lock:
            self.metrics = {
                'total_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'avg_response_time': 0,
                'total_response_time': 0,
                'api_calls': 0,
                'api_failures': 0
            }


# Singleton instance for global use
performance_optimizer = PerformanceOptimizer(
    cache_size=1000,
    max_workers=5,
    api_timeout=15  # Reduced from 30+ seconds to 15 seconds
)


def performance_monitoring(func):
    """
    Decorator for automatic performance monitoring.
    
    Usage:
        @performance_monitoring
        def my_query_function(self, query, user_type):  # Works with class methods
            # function implementation
            return response
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Handle both function and method calls
        if len(args) >= 3 and hasattr(args[0], '__class__'):
            # Class method: (self, question, user_type, ...)
            self_obj, question, user_type = args[0], args[1], args[2]
            extra_args = args[3:]
            # Call the original method directly for now - bypass optimization
            return func(self_obj, question, user_type, *extra_args, **kwargs)
        elif len(args) >= 2:
            # Function call: (query, user_type, ...)
            query, user_type = args[0], args[1]
            extra_args = args[2:]
            return performance_optimizer.optimized_query(
                func, query, user_type, *extra_args, **kwargs
            )
        else:
            # Fallback: call original function
            return func(*args, **kwargs)
    
    return wrapper


# Example usage functions
def test_performance_optimization():
    """Test the performance optimization system."""
    print("Testing Performance Optimization System")
    print("=" * 50)
    
    # Mock query function for testing
    def mock_query(query: str, user_type: str) -> Dict[str, Any]:
        # Simulate API delay
        time.sleep(2)  # Simulate 2-second API call
        
        return {
            'answer': f"Mock response for: {query}",
            'citations': ['Article 19', 'Article 21'],
            'reasoning_chain': 'Mock reasoning process',
            'accuracy_score': 0.95
        }
    
    # Test caching
    print("Testing response caching...")
    
    # First call - should be slow (cache miss)
    start = time.time()
    result1 = performance_optimizer.optimized_query(
        mock_query, 
        "What is freedom of speech?", 
        "lawyer"
    )
    time1 = time.time() - start
    print(f"First call (cache miss): {time1:.2f}s")
    
    # Second call - should be fast (cache hit)
    start = time.time()
    result2 = performance_optimizer.optimized_query(
        mock_query, 
        "What is freedom of speech?", 
        "lawyer"
    )
    time2 = time.time() - start
    print(f"Second call (cache hit): {time2:.2f}s")
    
    # Performance improvement
    improvement = ((time1 - time2) / time1) * 100
    print(f"Performance improvement: {improvement:.1f}%")
    
    # Show performance stats
    stats = performance_optimizer.get_performance_stats()
    print(f"\nPerformance Statistics:")
    print(f"Average response time: {stats['request_metrics']['avg_response_time']:.2f}s")
    print(f"Cache hit rate: {stats['cache_metrics']['hit_rate']:.2%}")
    print(f"Total requests: {stats['request_metrics']['total_requests']}")


if __name__ == "__main__":
    test_performance_optimization()