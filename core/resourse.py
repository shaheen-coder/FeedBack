from import_export import resources
from core.models import CustomUser


class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('username','email','password')