from abc import ABCMeta, abstractmethod

from django.db import models
from .models import *


class DraftHelper(object):

	@staticmethod
	def randomFromList(querylist, num):
		rcard = list(querylist)

		count = len(rcard)

		randc = [randint(0, count-1) for x in range(num)]

		randomCard = []
		for x in randc:
			randomCard.append(rcard[x])

		return randomCard



class Bonus(metaclass = ABCMeta):
	def __init__(self):


		pass

	@property
	@abstractmethod
	def nameString(self):
		pass

	@property
	@abstractmethod
	def descString(self):
		pass

	@property
	@abstractmethod
	def bonusID(self):
		pass

	@staticmethod
	@abstractmethod
	def getMainStarterCards():
		pass

	@staticmethod
	@abstractmethod
	def getExtraStarterCards():
		pass

	@abstractmethod
	def modifyDraft():
		pass

class BonusGetter:
	def BonusFactory(bonusid):
		if bonusid == 0:
			return DefaultBonus()
		else:
			return None

class DefaultBonus(models.Manager, Bonus ):
	nameString = "Obliterate!"
	descString = "You get 5 fucking pieces of exodia"
	bonusID = 0

	@staticmethod
	def getMainStarterCards():
		#Exodia pieces, Battle Fader, Factory of Mass production
		return [7902349,8124921,3396948,44519536,70903634, 90928333, 19665973]

	@staticmethod
	def getExtraStarterCards():
		return []

	def modifyDraft(self,count):
		#rcard = Datas.objects.getExtraDeckMonsters()
		rcard = self.get_queryset()
		return DraftHelper.randomFromList(rcard, count)


class ExodiaBonus(Bonus):
	nameString = "Obliterate!"
	descString = "You get 5 fucking pieces of exodia"
	bonusID = 0

	@staticmethod
	def getMainStarterCards():
		#Exodia pieces, Battle Fader, Factory of Mass production
		return [7902349,8124921,3396948,44519536,70903634, 90928333, 19665973]

	@staticmethod
	def getExtraStarterCards():
		return []

	@staticmethod
	def modifyDraft(count):
		rcard = Datas.objects.getExtraDeckMonsters()
		return DraftHelper.randomFromList(rcard, count)

