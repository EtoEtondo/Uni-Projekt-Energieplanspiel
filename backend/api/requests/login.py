import json
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from datetime import datetime
import pytz

from ..const import INPUT_VARIABLES
from ..models import *


def backend_login(request):
    if request.method == "POST":
        error_msg = ""
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            sessions = []
            for s in Session.objects.all():
                if datetime.now(tz=pytz.UTC) < s.expire_date:
                    sessions.append(s)
                else:
                    s.delete()
            if (
                (len(sessions) == 0
                or str(user.id) not in [s.get_decoded().get("_auth_user_id") for s in sessions])
                and user.enabled
            ):
                login(request, user)
                return redirect_by_role(user, request)
            else:
                error_msg = "Konto ist derzeit deaktiviert oder in Gebrauch!"
        else:
            error_msg = "Benutzername oder Passwort ist falsch!"

        return JsonResponse(status=404, data={"Error": error_msg})


def redirect_by_role(user, request):
    if user.is_superuser:
        # request.session["institutions"] = serializers.serialize("json", Institution.objects.all())
        return JsonResponse(status=200, data={"roles": f"admin"})
    elif user.is_staff:
        # request.session["schedules"] = serializers.serialize("json", Schedule.objects.filter(instructor_id=user.id))
        return JsonResponse(status=200, data={"roles": f"instructor"})
    else:
        # request.session["inputs"] = {"Variables": INPUT_VARIABLES}
        return JsonResponse(status=200, data={"roles": f"group"})
