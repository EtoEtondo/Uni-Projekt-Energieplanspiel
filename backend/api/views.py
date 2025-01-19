# import time
# from datetime import datetime
# from django.http import HttpResponse, JsonResponse
# from django.core.exceptions import PermissionDenied
# from django.core import serializers
# from django.contrib.auth import authenticate, login, logout

# from .models import *

# Create your views here.
# def adminview(request):
#     if request.user is not None:
#         if request.user.is_superuser:
#             return HttpResponse()
#     raise PermissionDenied()


# def instructorview(request):
#     if request.user is not None:
#         if request.user.is_staff or request.user.is_superuser:
#             return HttpResponse()
#     raise PermissionDenied()


# def groupview(request):
#     if request.user is not None:
#         return HttpResponse()
#     raise PermissionDenied()


# def test(request, id=0):
#     path = request.path
#     scheme = request.scheme
#     method = request.method
#     address = request.META["REMOTE_ADDR"]
#     user_agent = request.META["HTTP_USER_AGENT"]

#     inst = Institution(name="BHT-Berlin")
#     if not Institution.objects.filter(name="BHT-Berlin").exists():
#         inst.save()
#     else:
#         inst = Institution.objects.filter(name="BHT-Berlin")[0]
#     if not User.objects.filter(username="admin1").exists():
#         a = User(username="admin1", display_name="admin", is_superuser=True)
#         a.set_password("admin")
#         a.save()
#     if not User.objects.filter(username="hg98").exists():
#         instr = User(username="hg98", display_name="Hamit Güler", is_staff=True, institution=inst)
#         # pw werden gehasht
#         instr.set_password("hg98")
#         sched = Schedule(timeslot=datetime.utcfromtimestamp(time.time()), instructor=instr)
#         g = User(username="Tempelhof123", display_name="Tempelhof", date=sched)
#         # pw unterscheiden sich auch untereinander durch salt auch wenn raw pw gleich ist
#         g.set_password("hg98")
#         instr.save()
#         sched.save()
#         g.save()

#         # das prüfen sollte True returnen für beide user
#         print(instr.check_password("hg98"))
#         print(g.check_password("hg98"))
#         # der instructor der oben erstellt wurde würde zurückgegeben werden
#         print(serializers.serialize("json", [authenticate(username="hg98", password="hg98")]))

#     print(
#         {
#             u["id"]: {"username": u["username"], "display_name": u["display_name"]}
#             for u in User.objects.filter().values()
#         }
#     )
#     # das löschen aller Institutionen würde führt zum löschen aller daten bis auf admin user
#     # insts = Institution.objects.all()
#     # [inst.delete() for inst in insts]

#     request.user.has_submitted = False
#     request.user.save()

#     data = serializers.serialize("json", User.objects.all())

#     msg = f"\
# <html>\
# id: {id}<br>\
# Path: {path}<br>\
# Scheme: {scheme}<br>\
# Method: {method}<br>\
# Address: {address}<br>\
# User agent: {user_agent}<br>\
# Users: {data}<br>\
# User: {request.user}<br>\
# request: {request.body}<br>\
# request post: {type(request.POST)}<br>\
# request get: {request.GET}<br>\
# </html>\
# "
#     return HttpResponse(msg, content_type="text/html", charset="utf-8")
