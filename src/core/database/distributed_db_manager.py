# V3-001: Cloud Infrastructure Setup - Distributed Database Manager
# Agent-1: Architecture Foundation Specialist
# 
# Distributed database management for the V2_SWARM system

import os
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import asyncpg
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class DatabaseType(Enum):
    """Database type enumeration."""
    POSTGRESQL = "postgresql"
    REDIS = "redis"
    MONGODB = "mongodb"


@dataclass
class DatabaseConfig:
    """Database configuration."""
    db_type: DatabaseType
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_mode: str = "prefer"
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600


@dataclass
class QueryResult:
    """Database query result."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    affected_rows: Optional[int] = None


class DistributedDatabaseManager:
    """Distributed database management for V2_SWARM system."""
    
    def __init__(self):
        self.configs: Dict[str, DatabaseConfig] = {}
        self.connections: Dict[str, Any] = {}
        self.engines: Dict[str, Any] = {}
        self.sessions: Dict[str, Any] = {}
        self._initialize_configurations()
    
    def _initialize_configurations(self) -> None:
        """Initialize database configurations from environment."""
        # PostgreSQL configuration
        postgres_config = DatabaseConfig(
            db_type=DatabaseType.POSTGRESQL,
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "swarm_db"),
            username=os.getenv("POSTGRES_USER", "swarm_user"),
            password=os.getenv("POSTGRES_PASSWORD", "swarm123"),
            ssl_mode=os.getenv("POSTGRES_SSL_MODE", "prefer")
        )
        
        # Redis configuration
        redis_config = DatabaseConfig(
            db_type=DatabaseType.REDIS,
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            database=os.getenv("REDIS_DB", "0"),
            username=os.getenv("REDIS_USER", ""),
            password=os.getenv("REDIS_PASSWORD", ""),
            pool_size=20,
            max_overflow=30
        )
        
        self.configs = {
            "postgres": postgres_config,
            "redis": redis_config
        }
    
    async def initialize_connections(self) -> None:
        """Initialize database connections."""
        for name, config in self.configs.items():
            try:
                if config.db_type == DatabaseType.POSTGRESQL:
                    await self._init_postgres_connection(name, config)
                elif config.db_type == DatabaseType.REDIS:
                    await self._init_redis_connection(name, config)
            except Exception as e:
                print(f"Failed to initialize {name} connection: {e}")
    
    async def _init_postgres_connection(self, name: str, config: DatabaseConfig) -> None:
        """Initialize PostgreSQL connection."""
        # Create async engine
        database_url = (
            f"postgresql+asyncpg://{config.username}:{config.password}"
            f"@{config.host}:{config.port}/{config.database}"
        )
        
        engine = create_async_engine(
            database_url,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_timeout=config.pool_timeout,
            pool_recycle=config.pool_recycle,
            echo=False
        )
        
        # Create session factory
        session_factory = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        self.engines[name] = engine
        self.sessions[name] = session_factory
        
        # Test connection
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        print(f"PostgreSQL connection '{name}' initialized successfully")
    
    async def _init_redis_connection(self, name: str, config: DatabaseConfig) -> None:
        """Initialize Redis connection."""
        redis_url = f"redis://{config.host}:{config.port}/{config.database}"
        
        if config.password:
            redis_url = f"redis://:{config.password}@{config.host}:{config.port}/{config.database}"
        
        connection_pool = redis.ConnectionPool.from_url(
            redis_url,
            max_connections=config.pool_size,
            retry_on_timeout=True
        )
        
        self.connections[name] = redis.Redis(connection_pool=connection_pool)
        
        # Test connection
        await self.connections[name].ping()
        
        print(f"Redis connection '{name}' initialized successfully")
    
    async def execute_query(self, db_name: str, query: str, 
                          params: Dict[str, Any] = None) -> QueryResult:
        """Execute database query."""
        start_time = datetime.utcnow()
        
        try:
            config = self.configs.get(db_name)
            if not config:
                return QueryResult(
                    success=False,
                    error=f"Database '{db_name}' not configured"
                )
            
            if config.db_type == DatabaseType.POSTGRESQL:
                result = await self._execute_postgres_query(db_name, query, params)
            elif config.db_type == DatabaseType.REDIS:
                result = await self._execute_redis_query(db_name, query, params)
            else:
                return QueryResult(
                    success=False,
                    error=f"Unsupported database type: {config.db_type}"
                )
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            result.execution_time = execution_time
            
            return result
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    async def _execute_postgres_query(self, db_name: str, query: str, 
                                    params: Dict[str, Any] = None) -> QueryResult:
        """Execute PostgreSQL query."""
        session_factory = self.sessions.get(db_name)
        if not session_factory:
            return QueryResult(success=False, error="PostgreSQL session not available")
        
        async with session_factory() as session:
            try:
                result = await session.execute(text(query), params or {})
                
                if query.strip().upper().startswith(('SELECT', 'WITH')):
                    data = result.fetchall()
                    return QueryResult(success=True, data=data)
                else:
                    await session.commit()
                    return QueryResult(
                        success=True, 
                        affected_rows=result.rowcount
                    )
            except Exception as e:
                await session.rollback()
                raise e
    
    async def _execute_redis_query(self, db_name: str, query: str, 
                                 params: Dict[str, Any] = None) -> QueryResult:
        """Execute Redis query."""
        redis_client = self.connections.get(db_name)
        if not redis_client:
            return QueryResult(success=False, error="Redis connection not available")
        
        try:
            # Parse Redis command
            parts = query.strip().split()
            command = parts[0].upper()
            args = parts[1:] if len(parts) > 1 else []
            
            # Execute Redis command
            if command == "GET":
                result = await redis_client.get(args[0])
                return QueryResult(success=True, data=result.decode() if result else None)
            elif command == "SET":
                await redis_client.set(args[0], args[1])
                return QueryResult(success=True)
            elif command == "HGET":
                result = await redis_client.hget(args[0], args[1])
                return QueryResult(success=True, data=result.decode() if result else None)
            elif command == "HSET":
                result = await redis_client.hset(args[0], args[1], args[2])
                return QueryResult(success=True, affected_rows=result)
            elif command == "DEL":
                result = await redis_client.delete(args[0])
                return QueryResult(success=True, affected_rows=result)
            else:
                return QueryResult(
                    success=False, 
                    error=f"Unsupported Redis command: {command}"
                )
        except Exception as e:
            return QueryResult(success=False, error=str(e))
    
    async def get_connection_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all database connections."""
        status = {}
        
        for name, config in self.configs.items():
            try:
                if config.db_type == DatabaseType.POSTGRESQL:
                    engine = self.engines.get(name)
                    if engine:
                        async with engine.begin() as conn:
                            await conn.execute(text("SELECT 1"))
                        status[name] = {"status": "connected", "type": "postgresql"}
                    else:
                        status[name] = {"status": "disconnected", "type": "postgresql"}
                
                elif config.db_type == DatabaseType.REDIS:
                    redis_client = self.connections.get(name)
                    if redis_client:
                        await redis_client.ping()
                        status[name] = {"status": "connected", "type": "redis"}
                    else:
                        status[name] = {"status": "disconnected", "type": "redis"}
                
            except Exception as e:
                status[name] = {
                    "status": "error", 
                    "type": config.db_type.value,
                    "error": str(e)
                }
        
        return status
    
    async def close_connections(self) -> None:
        """Close all database connections."""
        # Close PostgreSQL engines
        for engine in self.engines.values():
            await engine.dispose()
        
        # Close Redis connections
        for redis_client in self.connections.values():
            await redis_client.close()
        
        self.engines.clear()
        self.connections.clear()
        self.sessions.clear()
    
    def get_config(self, db_name: str) -> Optional[DatabaseConfig]:
        """Get database configuration."""
        return self.configs.get(db_name)
    
    def add_config(self, name: str, config: DatabaseConfig) -> None:
        """Add new database configuration."""
        self.configs[name] = config



