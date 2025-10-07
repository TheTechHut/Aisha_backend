# Aisha_backend


## This setup:

Uses environment variables for sensitive data
Includes connection pooling for better performance
Adds automatic reconnection handling
Keeps database credentials secure
Uses the PostgreSQL-specific driver
N.ever commit the .env file to version control. Instead, provide a template file (.env.example) with dummy values for other developers.


from typing import Generic, Literal, TypeVar, Any
from pydantic import BaseModel
from abc import ABC, abstractmethod

# Define a generic type variable
T = TypeVar("T")

# The Resource protocol defines the required structure.
# We use an abstract class to ensure subclasses implement the 'status' and 'data' properties.
# Literal is used for type-checking to enforce specific string values for the status.
class ResourceProtocol(ABC, Generic[T]):
    @property
    @abstractmethod
    def status(self) -> Literal["success", "failure", "loading"]:
        ...

    @property
    @abstractmethod
    def data(self) -> T | None:
        ...

class Loading(BaseModel, ResourceProtocol[Any]):
    status: Literal["loading"] = "loading"
    data: None = None

class Success(BaseModel, ResourceProtocol[T]):
    status: Literal["success"] = "success"
    data: T

class Failure(BaseModel, ResourceProtocol[Any]):
    status: Literal["failure"] = "failure"
    data: None = None
    error: str
