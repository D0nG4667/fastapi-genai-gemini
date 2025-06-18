import time
from collections import defaultdict
from fastapi import HTTPException, status

# --- Constants ---
# Rate limit configuration for authenticated users
AUTHENTICATED_RATE_LIMIT = 9  # Maximum number of requests per user
# Time window in seconds for the rate limit
AUTHENTICATED_TIME_WINDOW_SECONDS = 60


# --- For unauthenticated users ---
GLOBAL_RATE_LIMIT = 3  # Maximum number of requests per user
GLOBAL_TIME_WINDOW_SECONDS = 60  # Time window in seconds for the rate limit

# --- In-memory storage for user requests ---
user_requests = defaultdict(list)  # Dictionary to track user requests


def apply_rate_limit(user_id: str):
    current_time = time.time()

    if user_id == "unauthenticated_user":
        # For unauthenticated users, apply global rate limit
        rate_limit = GLOBAL_RATE_LIMIT
        time_window = GLOBAL_TIME_WINDOW_SECONDS
    else:
        # For authenticated users, apply user-specific rate limit
        rate_limit = AUTHENTICATED_RATE_LIMIT
        time_window = AUTHENTICATED_TIME_WINDOW_SECONDS

    # Filter out requests older than the time window
    user_requests[user_id] = [
        timestamp for timestamp in user_requests.get(user_id, [])
        if timestamp > current_time - time_window
    ]

    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    else:
        # For debugging purposes, print current usage
        current_usage = len(user_requests[user_id])
        print(f"User {user_id}: {current_usage + 1}/{rate_limit} requests used.")

    # Record the current request
    user_requests[user_id].append(current_time)
    return True
