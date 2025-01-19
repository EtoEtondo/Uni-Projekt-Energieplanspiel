from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import *
from django.db.models import *


class Institution(Model):
    name = TextField()


class Schedule(Model):
    timeslot = DateTimeField()
    instructor = ForeignKey("User", on_delete=CASCADE)


class User(AbstractUser):
    display_name = TextField()
    # schon vorhanden, muss kein primary_key sein weil eh schon unqiue=True ist
    ## username = TextField(primary_key=True, unique=True)
    # können wir über is_superuser=False/True, is_staff=False/True regeln
    ## role = TextField(choices=ROLES)
    # können wir über is_active machen
    enabled = BooleanField(default=True)
    has_submitted = BooleanField(default=False)
    result_access = BooleanField(default=False)
    # date wichtig für user
    # musste ich umbenennen, sonst meckert der wegen  namens gebung
    date = ForeignKey("Schedule", blank=True, on_delete=CASCADE, null=True)
    # institution wichtig für instructor
    institution = ForeignKey("Institution", blank=True, on_delete=CASCADE, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
