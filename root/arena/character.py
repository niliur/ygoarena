
from abc import ABCMeta, abstractmethod
from .models import DraftHelper, Datas
from random import * 
import random
from .priorities import *





class Character:
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


class CharacterGetter:
	@staticmethod
	def CharacterFactory(characterid):
		if characterid == 0:
			return BCKaibaCharacter()

		elif characterid == 1:
			return OldKaibaCharacter()

		elif characterid == 2:
			return JoeyCharacter()

		elif characterid == 3:
			return YoungYugiCharacter()

		elif characterid == 4:
			return JadenCharacter()

		elif characterid == 5:
			return OldYugiCharacter()

		elif characterid == 6:
			return YumaCharacter()

		elif characterid == 7:
			return MakoCharacter()

		elif characterid == 8:
			return AkiCharacter()
		else:
			return DefaultCharacter()

class DefaultCharacter(Character):
	nameString = "Yugi"
	descString = "Yung thug"

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
		return []

	@staticmethod
	def getExtraStarterCards():
		return []


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
	def addToMDMCards():
		return []

	@staticmethod
	def addToSTCards():
		return []

	@staticmethod
	def addToEDMCards():
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
	def getMainDeckSize():
		return None

	@staticmethod
	def getExtraDeckSize():
		return None



	@staticmethod
	def chooseDraftOption(code):
		return code

	@staticmethod
	def alterDraftOption(code):
		return code

class BCKaibaCharacter(DefaultCharacter):

	#Nigga in battle city
	@staticmethod
	def getMainStarterCards():
		#Soul Exchange, obelisk the tormentor, enemy controller
		return [68005187, 10000000, 98045062]


class OldKaibaCharacter(DefaultCharacter):	

	@staticmethod
	def addToMDMCards():
		# Always able to draft blueeyes
		return [89631139]

class JoeyCharacter(DefaultCharacter):
	chooseMDMPriority = 1
	@staticmethod
	def getMainStarterCards():

		#REBD, heart of the underdog, Ancient rules
		return [74677422,35762283,10667321]

		#During the draft, all normal monsters have > 1500 attack or > 1500 def
	@staticmethod
	def modifyMDMCards(num,code):

		normal = lambda x: (x.type & 0x11 != 0x11) or (x.atk > 1500) or (x.def_field > 1500)


		randomCard = DraftHelper.randomFromList(Datas.objects.getMainDeckMonsters(), num, normal)
		return randomCard

class YoungYugiCharacter(DefaultCharacter):

	mainDeckSizePriority = 2
	extraDeckSizePriority = 1

	@staticmethod
	def getMainStarterCards():

		#Monster Reborn, Horn of heaven
		return [83764718,98069388]

	@staticmethod
	def getMainDeckSize(mds):
		return 24
	
	@staticmethod
	def getExtraDeckSize(eds):
		return 6

class JadenCharacter(DefaultCharacter):
	chooseEDMPriority = 0
	@staticmethod
	def getMainStarterCards():

		#starting a hero lives, bubbleman, clayman, shadow mist:
		return [8949584,79979666, 84327329, 50720316]

	@staticmethod
	def addToSTCards():
		#adds a fucking mask change
		return [21143940]

	@staticmethod
	def addToEDMCards():
		#adds a fucking mask change 2
		return[93600443]

	@staticmethod
	def modifyEDMCards(numCards, code):

		#Chance to draft masked heroes

		if(numCards <= 3):
			numCardsNormal = 0
			numCardsHeroes = numCards

		else:
			numCardsNormal = numCards - 3
			numCardsHeroes = 3

		normal = lambda x: (x.setcode & 0xA008 == 0xA008)


		randomCard1 = DraftHelper.randomFromList(Datas.objects.getExtraDeckMonsters(), numCardsNormal)
		randomCard2 = DraftHelper.randomFromList(Datas.objects.getCardsFromList([89870349,62624486, 59642500, 58481572, 58147549, 50608164, 29095552, 22093873, 10920352]), numCardsHeroes)
		randomCard = randomCard1 + randomCard2
		return randomCard

class OldYugiCharacter(DefaultCharacter):
	chooseMDMPriority = 0
	chooseEDMPriority = 0

	@staticmethod
	def getMainStarterCards():

		#starting eternal soul, dark magician, wonder wand
		return [48680970,46986420, 67775894]



	# 15% chance for a monster to be a spellcaster
	@staticmethod
	def modifyEDMCards(numCards, code):

		magicians = 0
		for i in range(numCards):
			if (randint(0, 99) < 15):
				magicians += 1

		randomCard1 = DraftHelper.randomFromList(Datas.objects.getExtraDeckMonsters(), numCards-magicians)
		randomCard2 = DraftHelper.randomFromList(Datas.objects.getEDMCustomFilter([(0x2, True, 'race')]), magicians)
		randomCard = randomCard1 + randomCard2
		return randomCard


	@staticmethod
	def modifyMDMCards(numCards, code):

		magicians = 0
		for i in range(numCards):
			if (randint(0, 99) < 15):
				magicians += 1

		randomCard1 = DraftHelper.randomFromList(Datas.objects.getMainDeckMonsters(), numCards-magicians)
		randomCard2 = DraftHelper.randomFromList(Datas.objects.getMDMCustomFilter([(0x2, True, 'race')]), magicians)
		randomCard = randomCard1 + randomCard2
		return randomCard

class YumaCharacter(DefaultCharacter):
	chooseCardPriority = 0
	chooseEDMPriority = YUMAEDMPRIORITY
	alterDraftOptionsPriority = YUMAADOPRIORITY

	@staticmethod
	def getExtraStarterCards():

		#starting #39 Utopia
		return [84013237]


	@staticmethod
	def modifyEDMCards(numCards, code):
		randomCard = DraftHelper.randomFromList(Datas.objects.getEDMCustomFilter([(0x48, True, u'setcode'),(0x1, False, u'setcode'),(0x2, False, u'setcode'),(0x4, False, u'setcode'),(0x10, False, u'setcode'),(0x20, False, u'setcode')]), numCards)
		return randomCard


	@staticmethod
	def alterDraftOption(code):
		if (code == 5):
			print("denied")
			code = 0 
		return code

class MakoCharacter(DefaultCharacter):
	chooseMDMPriority = 0
	chooseEDMPriority = 0



	@staticmethod
	def getMainStarterCards():

		#starting Umi, umiruka, a legendary ocean
		return [22702055,82999629, 295517]



	# 50% chance for a monster to be water type
	@staticmethod
	def modifyEDMCards(numCards, code):

		magicians = 0
		for i in range(numCards):
			if (randint(0, 99) < 50):
				magicians += 1

		randomCard1 = DraftHelper.randomFromList(Datas.objects.getExtraDeckMonsters(), numCards-magicians)
		randomCard2 = DraftHelper.randomFromList(Datas.objects.getEDMCustomFilter([(0x2, True, 'attribute')]), magicians)
		randomCard = randomCard1 + randomCard2
		return randomCard


	@staticmethod
	def modifyMDMCards(numCards, code):

		magicians = 0
		for i in range(numCards):
			if (randint(0, 99) < 50):
				magicians += 1

		randomCard1 = DraftHelper.randomFromList(Datas.objects.getMainDeckMonsters(), numCards-magicians)
		randomCard2 = DraftHelper.randomFromList(Datas.objects.getMDMCustomFilter([(0x2, True, 'attribute')]), magicians)
		randomCard = randomCard1 + randomCard2
		return randomCard

class AkiCharacter(DefaultCharacter):
	@staticmethod
	def getMainStarterCards():

		#starting lonefire blossom, glow up bulb, blue rose dragon, gigaplant
		return [48686504,67441435, 98884569, 53257892]

	@staticmethod
	def getExtraStarterCards():

		#starting black rose dragon
		return [73580471]

