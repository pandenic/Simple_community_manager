"""Contain page renders for core app.

pages
404
"""

from django.shortcuts import render


def page_not_found(request, exception):
    """Exchange basic 404 error page with custom template."""
    return render(request, "core/404.html", {"path": request.path}, status=404)


def csrf_failure(request, reason=""):
    """Exchange basic 404 csrf error page with custom template."""
    return render(request, "core/403csrf.html")
