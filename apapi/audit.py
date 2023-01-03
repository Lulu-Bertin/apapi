"""
apapi.audit

Child of Basic Connection class, responsible for Audit API capabilities
"""
import json

from requests import Response, Session

from .authentication import AuthType
from .basic_connection import BasicConnection
from .utils import (
    API_URL,
    AUDIT_URL,
    AUTH_URL,
    AuditEventType,
    MIMEType,
    get_generic_session,
)


class AuditConnection(BasicConnection):
    """Anaplan connection with Audit API functions."""

    def __init__(
        self,
        credentials: str,
        auth_type: AuthType = AuthType.BASIC,
        session: Session = get_generic_session(),
        auth_url: str = AUTH_URL,
        api_url: str = API_URL,
        _audit_url: str = AUDIT_URL,
    ):
        super().__init__(credentials, auth_type, session, auth_url, api_url)
        self._audit_url: str = f"{_audit_url}/audit/api/1"

    def get_events(
        self,
        event_type: AuditEventType = AuditEventType.ALL,
        accept: MIMEType = MIMEType.APP_JSON,
        date_from: int = None,
        date_to: int = None,
        interval: int = None,
    ) -> Response:
        """Retrieve Audit Events for tenant."""
        params = {
            "type": event_type.value,
            "limit": 2147483647,  # 2^31-1, max accepted, as default is 20
        }
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        if interval:
            params["intervalInHours"] = interval
        return self.request(
            "GET",
            f"{self._audit_url}/events",
            params=params,
            headers={"Accept": accept.value} if accept else None,
        )

    def search_events(
        self,
        event_type: AuditEventType = AuditEventType.ALL,
        accept: MIMEType = MIMEType.APP_JSON,
        date_from: int = None,
        date_to: int = None,
        interval: int = None,
    ) -> Response:
        """
        Retrieve Audit Events for tenant.

        This function is practically an alternative for AuditConnection.get_events().
        """
        params = {
            "type": event_type.value,
            "limit": 2147483647,  # 2^31-1, max accepted, as default is 20
        }
        data = {}
        if date_from:
            data["from"] = date_from
        if date_to:
            data["to"] = date_to
        if interval:
            data["interval"] = interval
        return self.request(
            "POST",
            f"{self._audit_url}/events/search",
            params=params,
            data=json.dumps(data),
            headers={"Accept": accept.value} if accept else None,
        )
