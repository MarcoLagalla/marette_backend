from datetime import datetime

from rest_framework import serializers

from ..models.models import GiornoApertura, OrarioApertura, FasciaOraria, Restaurant


class OpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrarioApertura
        fields = ('restaurant', )


class GiornoAperturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiornoApertura
        fields = ('restaurant', 'day', 'fasce', )

    def save(self, **kwargs):

        restaurant = self.validated_data.get('restaurant')

        try:
            orario = OrarioApertura.objects.all().get(restaurant=restaurant)
        except OrarioApertura.DoesNotExist:
            raise serializers.ValidationError({'error': 'Orario non trovato per questo ristorante.'})

        giorno = GiornoApertura.objects.create(orario=orario, **self.validated_data)
        giorno.save()

        return giorno


class FasciaOrariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FasciaOraria
        fields = ('restaurant', 'start', 'end', )

    def validate(self, attrs):
        start = datetime.strptime(attrs['start'], '%H:%M')
        stop = datetime.strptime(attrs['end'], '%H:%M')
        dt = stop - start
        if dt.days < 0:
            raise serializers.ValidationError({'error': "Orario di fine turno antecedente a quello di inizio."})

        return attrs

    def save(self, giorno, **kwargs):

        restaurant = self.validated_data.get('restaurant')

        try:
            orario = OrarioApertura.objects.all().get(restaurant=restaurant)
        except OrarioApertura.DoesNotExist:
            raise serializers.ValidationError({'error': 'Orario non trovato per questo ristorante.'})

        fascia = FasciaOraria.objects.create(giorno=giorno, **self.validated_data)
        fascia.save()

        giorno.fasce.add(fascia)
        giorno.save()

        return fascia
