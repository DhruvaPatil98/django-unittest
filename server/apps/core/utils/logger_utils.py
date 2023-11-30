import re

from apps.core.constants import CoreConstants
from contextvars import ContextVar

log_prefix_var = ContextVar('log_prefix')


def set_logger_prefix(account_id, user_id):
    return log_prefix_var.set(f"[Acc:{account_id}|User:{user_id}]")


def handle_none(value):
    return None if value == "None" else value


def fetch_logger_prefix():
    result = {}
    prefix = get_logger_prefix()
    match = re.search(CoreConstants.PATTERN, prefix)

    if match:
        acc_uuid = match.group("acc_id")
        user_uuid = match.group("user_id")

        result = {
            "account_id": handle_none(acc_uuid),
            "user_id": handle_none(user_uuid),
        }
    return result


def get_logger_prefix() -> str:
    return log_prefix_var.get()
