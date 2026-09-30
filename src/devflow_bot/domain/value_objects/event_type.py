"""GitHub event types value object."""

from enum import StrEnum


class EventType(StrEnum):
    """GitHub webhook event types."""

    PUSH = "push"
    PULL_REQUEST = "pull_request"
    ISSUES = "issues"
    ISSUE_COMMENT = "issue_comment"
    RELEASE = "release"
    WORKFLOW_RUN = "workflow_run"
    PING = "ping"
