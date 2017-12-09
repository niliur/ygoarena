from rest_framework import serializers
from .models import *

class deckSerializer(serializers.ModelSerializer):

	#url = serializers.HyperlinkedIdentityField(view_name="arena:deck")
	class Meta:
		model = Deck
		fields = '__all__'


class cardsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Datas
		fields = '__all__'

class textsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Texts
		fields = '__all__'


class draftSerializer(serializers.ModelSerializer):
	card = cardsSerializer(many = False, read_only = True)
	text = textsSerializer(many = False, read_only = True)
	class Meta:
		model = Draft
		fields = '__all__'