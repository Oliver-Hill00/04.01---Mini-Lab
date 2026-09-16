from django.shortcuts import render

from .canvas_api import CanvasAPIError, get_active_courses


def dashboard(request):
    """Skeleton view: call Canvas, handle errors, pass results to the template.

    TODO:
    - Read whatever input you added in forms.py from `request.GET`.
    - Call get_active_courses() and your second endpoint function.
    - Combine/filter/sort the results into whatever shape your template needs.
    """
    context = {"error": None, "courses": None}

    try:
        context["courses"] = get_active_courses()
        # TODO: call your second endpoint here and merge its data into context.
    except CanvasAPIError as exc:
        # Errors from canvas_api.py (missing token, network failure, bad
        # status code) land here as plain strings — safe to show directly.
        context["error"] = str(exc)

    return render(request, "dashboard/dashboard.html", context)
