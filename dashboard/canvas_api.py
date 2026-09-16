"""Small client for the Canvas LMS REST API.

Only what this app needs: listing active courses and listing assignments
for a course, both with Link-header pagination followed to completion.
"""
from django.conf import settings
import requests


class CanvasAPIError(Exception):
    """Raised for any problem talking to Canvas: missing token, network
    failure, or a non-2xx response. Callers show `str(error)` to the user.
    """


def _require_config():
    if not settings.CANVAS_API_TOKEN:
        raise CanvasAPIError(
            "No Canvas API token configured. Set CANVAS_API_TOKEN in your .env file."
        )
    if not settings.CANVAS_API_URL:
        raise CanvasAPIError(
            "No Canvas API URL configured. Set CANVAS_API_URL in your .env file."
        )


def _get_all_pages(path, params=None):
    """GET `path` and follow the Link header's "next" relation until
    Canvas stops returning one, collecting every page's JSON list into one.

    Canvas paginates list endpoints (courses, assignments, etc.) using a
    standard Link header rather than an offset/limit you pass yourself, so
    the only reliable way to get every item is to keep following "next".
    """
    _require_config()

    headers = {"Authorization": f"Bearer {settings.CANVAS_API_TOKEN}"}
    url = f"{settings.CANVAS_API_URL}{path}"
    results = []

    try:
        while url:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            # params only apply to the first request; the "next" link from
            # Canvas already has every query parameter baked in.
            params = None

            if response.status_code != 200:
                raise CanvasAPIError(
                    f"Canvas returned an error (status {response.status_code}) for {url}: "
                    f"{response.text[:200]}"
                )

            results.extend(response.json())
            url = response.links.get("next", {}).get("url")
    except requests.exceptions.RequestException as exc:
        raise CanvasAPIError(f"Could not reach Canvas: {exc}") from exc

    return results


def get_active_courses():
    """Return the current user's active courses.

    Example endpoint call using the _get_all_pages helper above — use this
    as the pattern for whatever second endpoint you pick below.
    """
    return _get_all_pages(
        "/api/v1/courses",
        params={"enrollment_state": "active", "per_page": 50},
    )


# TODO: add a second endpoint function here, following the pattern above.
# Ideas: assignments for a course (/api/v1/courses/:id/assignments),
# announcements (/api/v1/announcements?context_codes[]=course_XXX),
# a to-do list (/api/v1/users/self/todo), upcoming events, grades, etc.
# Whatever you pick, call it through _get_all_pages so pagination and auth
# are handled for you.
