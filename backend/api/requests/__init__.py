from .csrf import backend_csrf
from .login import backend_login
from .logout import backend_logout
from .csrf import backend_csrf
from .group import crud_group, change_result_access_by_schedule
from .instructor import crud_instructor
from .schedule import crud_schedule
from .institution import crud_institution
from .input import handle_input
from .calculate import calculate_for_schedule, get_calculate_progress_for_schedule
from .results import get_results_for_schedule

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def get_own_info(request):
    user = request.user
    return JsonResponse(
        status=200,
        data={
            user.id: {
                "username": user.username,
                "display_name": user.display_name,
                "enabled": user.enabled,
                "has_submitted": user.has_submitted,
                "result_access": user.result_access,
            },
        },
    )
