from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    work_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

