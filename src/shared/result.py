"""
Result Type - Railway Oriented Programming
==========================================

Provides a Result type for functional error handling.
Inspired by Railway Oriented Programming (ROP) pattern.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar, Union, Callable, Any
from functools import wraps

T = TypeVar('T')
E = TypeVar('E')


@dataclass(frozen=True)
class Success(Generic[T]):
    """Represents a successful operation with a value."""
    value: T

    def is_success(self) -> bool:
        return True

    def is_failure(self) -> bool:
        return False

    def map(self, func: Callable[[T], Any]) -> 'Result[Any, E]':
        try:
            return Success(func(self.value))
        except Exception as e:
            return Failure(e)

    def bind(self, func: Callable[[T], 'Result[Any, E]']) -> 'Result[Any, E]':
        try:
            return func(self.value)
        except Exception as e:
            return Failure(e)

    def get_or_else(self, default: T) -> T:
        return self.value

    def or_else(self, func: Callable[[E], T]) -> T:
        return self.value


@dataclass(frozen=True)
class Failure(Generic[E]):
    """Represents a failed operation with an error."""
    error: E

    def is_success(self) -> bool:
        return False

    def is_failure(self) -> bool:
        return True

    def map(self, func: Callable[[T], Any]) -> 'Result[T, E]':
        return self  # Failure propagates unchanged

    def bind(self, func: Callable[[T], 'Result[Any, E]']) -> 'Result[T, E]':
        return self  # Failure propagates unchanged

    def get_or_else(self, default: T) -> T:
        return default

    def or_else(self, func: Callable[[E], T]) -> T:
        return func(self.error)


Result = Union[Success[T], Failure[E]]


def success(value: T) -> Success[T]:
    """Create a successful result."""
    return Success(value)


def failure(error: E) -> Failure[E]:
    """Create a failed result."""
    return Failure(error)


def try_catch(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    """
    Decorator to convert exceptions to Result types.

    Usage:
        @try_catch
        def risky_operation():
            # ... code that might raise exceptions
            return result
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Result[T, Exception]:
        try:
            return Success(func(*args, **kwargs))
        except Exception as e:
            return Failure(e)

    return wrapper
