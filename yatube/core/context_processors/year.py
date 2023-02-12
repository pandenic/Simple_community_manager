"""Module is used to create year variable for footer."""
from datetime import datetime


def year(request):
    """Add year variable."""
    return {
        "year": datetime.now().year,
    }
