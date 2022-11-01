from rest_framework import serializers
from .models import Vendedor


class VendedorViewSet(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'
