from __future__ import annotations


class GatewayError(Exception):
    """Base error for gateway platform."""


class AuthenticationError(GatewayError):
    """Authentication failed."""


class AuthorizationError(GatewayError):
    """Authorization failed."""


class NotFoundError(GatewayError):
    """Entity not found."""
