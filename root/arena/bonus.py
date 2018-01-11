
from abc import ABCMeta, abstractmethod
from .models import DraftHelper, Datas
from random import * 
import random

class Bonus:
	__metaclass__ = ABCMeta
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
	def chooseCardPriority(self):
		pass


	@property
	@abstractmethod
	def chooseMDMPriority(self):
		pass


	@property
	@abstractmethod
	def chooseSTPriority(self):
		pass

	@property
	@abstractmethod
	def chooseEDMPriority(self):
		pass

	@property
	@abstractmethod
	def mainDeckSizePriority(self):
		pass


	@property
	@abstractmethod
	def extraDeckSizePriority(self):
		pass





	@staticmethod
	@abstractmethod
	def modifyMDMCards( card, code):
		pass

	@staticmethod
	@abstractmethod
	def modifySTCards( card, code):
		pass
		
	@staticmethod
	@abstractmethod
	def modifyEDMCards( card, code):
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



	@abstractmethod
	def chooseDraftOption(code):
		pass

	@abstractmethod
	def alterDraftOption(code):
		pass

class BonusGetter:


	@staticmethod
	def BonusFactory(bonusid):
		if bonusid == 0:
			return ExodiaBonus()
		if bonusid == 1:
			return TeslaBonus()
		if bonusid == 2:
			return UBWBonus()
		if bonusid == 3:
			return LightBonus()
		if bonusid == 4:
			return DegenerateBonus()
		if bonusid == 5:
			return TributeBonus()
		if bonusid == 6:
			return TrapBonus()
		if bonusid == 7:
			return SanganBonus()
		if bonusid == 8:
			return LawnmowBonus()
		else:
			return DefaultBonus()

class DefaultBonus(Bonus):
	nameString = "Obliterate!"
	descString = "You get 5 fucking pieces of exodia"
	chooseCardPriority = -1
	chooseEDMPriority = -1
	chooseMDMPriority = -1
	chooseSTPriority = -1
	mainDeckSizePriority = -1
	extraDeckSizePriority = -1
	chooseDraftOptionsPriority = -1
	alterDraftOptionsPriority = -1

	@staticmethod
	def getMainStarterCards():
		#Exodia pieces, Battle Fader, Factory of Mass production
		return []

	@staticmethod
	def getExtraStarterCards():
		return []


	#1 to 4 ratio of extra to monster
	@staticmethod	
	def modifyDraft(mdsize, edsize, mdLimit, edLimit):
		missingMain = max(0,mdLimit - mdsize)
		missingExtra = max(0, edLimit - edsize)

		if ((missingMain == 0) and (missingExtra == 0)):
			ValueError("Should not generate")

		if (missingExtra * 4 <= missingMain):
			# return true for maindeck, false for extra deck
			return True

		else:
			return False

	@staticmethod
	def modifyEDMCards(numCards, code):
		rcard = Datas.objects.getExtraDeckMonsters()
		#rcard = self.get_queryset()
		randomCard = DraftHelper.randomFromList(rcard, numCards)
		#randomCard = self.getEDM(6)
		
		return randomCard

	@staticmethod
	def modifyMDMCards(numCards, code):
		randomCard = DraftHelper.randomFromList(Datas.objects.getMainDeckMonsters(), numCards)
		return randomCard

	@staticmethod
	def modifySTCards(numCards, code):
		randomCard = DraftHelper.randomFromList(Datas.objects.getST(), numCards)
		return randomCard



	@staticmethod
	def getMainDeckSize():
		return None

	@staticmethod
	def getExtraDeckSize():
		return None
	@staticmethod
	def convertDraftOption(code):
		return code

	@staticmethod
	def chooseDraftOption(code):
		return code

	@staticmethod
	def alterDraftOption(code):
		return code

class ExodiaBonus(DefaultBonus):

	@staticmethod
	def getMainStarterCards():
		#Exodia pieces, Battle Fader, Factory of Mass production
		return [7902349,8124921,33396948,44519536,70903634, 90928333, 19665973]

class TeslaBonus(DefaultBonus):

	@staticmethod
	def getMainStarterCards():
		#raigeki, Cydra, limiter removal, twinbarrel
		return [12580477, 70095155,23171610, 70050374]

	@staticmethod
	def getExtraStarterCards():
		#Fortress dragon
		return [79229522]

class UBWBonus(DefaultBonus):

	@staticmethod
	def getMainStarterCards():
		#Axe of fools, butterfly elma, cursed armaments, iron blacksmith
		return [19578592, 69243953, 98867329, 73431236]

	@staticmethod
	def getExtraStarterCards():
		#Powertool dragon
		return [2403771]

class LightBonus(DefaultBonus):
	@staticmethod
	def getMainStarterCards():
		#honest, raiden, ryko, light, white dragon wyvernbuster
		return [37742478, 77558536,21502796, 99234526]


class DegenerateBonus(DefaultBonus):
	@staticmethod
	def getMainStarterCards():
		# wavemotion, nightmare wheel, pot of greed, trap hole
		return [38992735, 54704216,55144522, 4206964]



class TributeBonus(DefaultBonus):
	@staticmethod
	def getMainStarterCards():
		#5 and over club: 1 x Tribute burial, 1 x Dark Squire, Double summon
		return [80230510, 79844764, 43422537]

class TrapBonus(DefaultBonus):

	chooseSTPriority = 1

	@staticmethod
	def getMainStarterCards():
		#Powerful rebirth
		return [84298614]

	@staticmethod
	def modifySTCards(numCards, code):
		randomCard = DraftHelper.randomFromList(Datas.objects.getT(), numCards)
		return randomCard

class SanganBonus(DefaultBonus):
	@staticmethod
	def getMainStarterCards():
		#3x Sangan, tour guide
		return [26202165, 26202165, 26202165, 10802915]

	@staticmethod
	def getExtraStarterCards():
		#Alucard, wind up zenmaines
		return [75367227, 78156759]

class LawnmowBonus(DefaultBonus):

	mainDeckSizePriority = 1
	@staticmethod
	def getMainStarterCards():
		#3x lawnmowing, imp sabres, plaguespreader, electroturtle, shadoll beast
		return [11110587, 11110587, 11110587, 30068120, 33420078,34710660,3717252]

	@staticmethod
	def getMainDeckSize(mds):
		return 60

	@staticmethod
	def getExtraDeckSize(eds):
		return 15
