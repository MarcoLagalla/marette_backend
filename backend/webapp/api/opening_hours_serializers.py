from rest_framework import serializers

from ..models.models import GiornoApertura, OrarioApertura, FasciaOraria


class OpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrarioApertura
        fields = ('restaurant', )


class GiornoAperturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiornoApertura
        fields = ('restaurant', 'day', 'fasce', )


class FasciaOrariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FasciaOraria
        fields = ('restaurant', 'start', 'end', )
