"""
Pydantic schemas for request/response validation.

This module defines all Pydantic models used for data validation
throughout the application. These schemas ensure type safety and
automatic validation of incoming requests and outgoing responses.

Following the Interface Segregation Principle, schemas are split
into specific models for different operations (Create, Update, Response).

Author: Equipo 46
Date: 2024
"""

from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Authentication Schemas
# ============================================================================

class UserLoginRequest(BaseModel):
    """
    Schema for user login requests.

    Attributes:
        login: Email or username of the user.
        password: User's password.
    """
    login: str = Field(
        ...,
        description="Email or username",
        min_length=1,
        json_schema_extra={"example": "user@example.com"}
    )
    password: str = Field(
        ...,
        description="User password",
        min_length=1,
        json_schema_extra={"example": "password123"}
    )


class UserLoginResponse(BaseModel):
    """
    Schema for user login responses.

    Attributes:
        user_token: Authentication token to be used in subsequent requests.
        objectId: Unique identifier of the user.
        email: User's email address.
    """
    user_token: str = Field(
        ...,
        alias="user-token",
        description="Authentication token for subsequent requests"
    )
    objectId: str = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")

    class Config:
        """Pydantic configuration."""
        populate_by_name = True


# ============================================================================
# Subject (Materia) Schemas
# ============================================================================

class SubjectCreate(BaseModel):
    """
    Schema for creating a new subject.

    Attributes:
        name: Name of the subject.
        code: Unique code identifier for the subject.
        kind: Type of subject (class, exam, task, project, other).
        weeklyLoadHours: Number of hours per week for this subject.
    """
    name: str = Field(
        ...,
        description="Name of the subject",
        min_length=1,
        json_schema_extra={"example": "Cálculo I"}
    )
    code: str = Field(
        ...,
        description="Unique code for the subject",
        min_length=1,
        json_schema_extra={"example": "CALC1"}
    )
    kind: Literal["class", "exam", "task", "project", "other"] = Field(
        default="class",
        description="Type of subject"
    )
    weeklyLoadHours: int = Field(
        default=4,
        ge=0,
        description="Weekly hours load",
        json_schema_extra={"example": 4}
    )

    @field_validator('name', 'code')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """
        Validates that string fields are not empty or whitespace only.

        Args:
            v: The string value to validate.

        Returns:
            str: The validated string.

        Raises:
            ValueError: If the string is empty or contains only whitespace.
        """
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip()


class SubjectUpdate(BaseModel):
    """
    Schema for updating an existing subject.

    All fields are optional to allow partial updates.

    Attributes:
        name: Name of the subject.
        code: Unique code identifier for the subject.
        kind: Type of subject.
        weeklyLoadHours: Number of hours per week for this subject.
    """
    name: Optional[str] = Field(
        None,
        description="Name of the subject",
        min_length=1
    )
    code: Optional[str] = Field(
        None,
        description="Unique code for the subject",
        min_length=1
    )
    kind: Optional[Literal["class", "exam", "task", "project", "other"]] = Field(
        None,
        description="Type of subject"
    )
    weeklyLoadHours: Optional[int] = Field(
        None,
        ge=0,
        description="Weekly hours load"
    )

    @field_validator('name', 'code')
    @classmethod
    def validate_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """
        Validates that string fields, if provided, are not empty.

        Args:
            v: The string value to validate.

        Returns:
            Optional[str]: The validated string or None.

        Raises:
            ValueError: If the string is empty or contains only whitespace.
        """
        if v is not None and (not v or not v.strip()):
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip() if v else None


class Subject(BaseModel):
    """
    Schema for subject responses.

    Represents a complete subject object as returned by the API.

    Attributes:
        objectId: Unique identifier assigned by Backendless.
        name: Name of the subject.
        code: Unique code identifier for the subject.
        kind: Type of subject.
        weeklyLoadHours: Number of hours per week for this subject.
        created: Timestamp when the subject was created.
        updated: Timestamp when the subject was last updated.
    """
    objectId: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the subject")
    code: str = Field(..., description="Unique code for the subject")
    kind: Literal["class", "exam", "task", "project", "other"] = Field(
        default="class",
        description="Type of subject"
    )
    weeklyLoadHours: int = Field(
        default=4,
        ge=0,
        description="Weekly hours load"
    )
    created: Optional[int] = Field(
        None,
        description="Creation timestamp (Unix milliseconds)"
    )
    updated: Optional[int] = Field(
        None,
        description="Last update timestamp (Unix milliseconds)"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "objectId": "ABCD1234",
                "name": "Cálculo I",
                "code": "CALC1",
                "kind": "class",
                "weeklyLoadHours": 4,
                "created": 1699564800000,
                "updated": 1699564800000
            }
        }


class PaginatedSubjects(BaseModel):
    """
    Schema for paginated subject list responses.

    Attributes:
        total: Total number of subjects available.
        count: Number of subjects in the current page.
        offset: Offset used for this page.
        results: List of subjects in the current page.
    """
    total: int = Field(..., description="Total number of items", ge=0)
    count: int = Field(..., description="Number of items in this page", ge=0)
    offset: int = Field(..., description="Offset used for pagination", ge=0)
    results: list[Subject] = Field(..., description="List of subjects")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "total": 124,
                "count": 10,
                "offset": 0,
                "results": [
                    {
                        "objectId": "ABCD1234",
                        "name": "Cálculo I",
                        "code": "CALC1",
                        "kind": "class",
                        "weeklyLoadHours": 4
                    }
                ]
            }
        }
