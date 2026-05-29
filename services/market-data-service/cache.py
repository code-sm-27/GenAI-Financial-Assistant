import os
import json
import logging
from typing import Optional, Dict, Any
import redis
from redis import ConnectionPool

logger = logging.getLogger(__name__)

class RedisCache:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisCache, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self) -> None:
        """Initializes the Redis connection pool."""
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        try:
            self.pool = ConnectionPool.from_url(redis_url, decode_responses=True)
            self.client = redis.Redis(connection_pool=self.pool)
            # Test connection
            self.client.ping()
            logger.info(f"Successfully connected to Redis at {redis_url}")
            self.is_connected = True
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis at {redis_url}: {e}")
            self.is_connected = False
            self.client = None

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves and deserializes data from Redis."""
        if not self.is_connected or not self.client:
            return None
            
        try:
            data = self.client.get(key)
            if data:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(data)
            logger.info(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.warning(f"Error reading from Redis cache: {e}")
            return None

    def set(self, key: str, value: Dict[str, Any], ttl_seconds: int = 60) -> bool:
        """Serializes and stores data in Redis with a TTL."""
        if not self.is_connected or not self.client:
            return False
            
        try:
            serialized_data = json.dumps(value)
            self.client.setex(key, ttl_seconds, serialized_data)
            logger.debug(f"Successfully cached data for key: {key} (TTL: {ttl_seconds}s)")
            return True
        except Exception as e:
            logger.warning(f"Error writing to Redis cache: {e}")
            return False
