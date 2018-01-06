# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import hashlib, time, datetime
import struct
import random
from random import randint
from abc import ABCMeta, abstractmethod
import string
import inspect
from django.db.models import Max
import math

def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))


class CFHelper(object):
	@staticmethod
	def filterCardByHex(code, hval, boolean = True):
		# for card in cards:
		# 	if (card.type & hval == bool):
		# 		yield card
		if((code & hval)):
			return boolean
		return not boolean


	@staticmethod
	def filterCardByHexList(code, hvalList):

		ret = True
		for hval in hvalList:
			target = getattr(code, hval[2])
			if((target & hval[0])):
				ret = ret and hval[1]
			else:
				ret = ret and (not hval[1])

		return ret
	



class CardDataManager(models.Manager):

	def getCardsFromList(self, list):
		cards = self.get_queryset()
		for card in cards:
			for cardid in list:
				if card.id == cardid:
					yield card
	

	def getMDMCustomFilter(self, listadd):
		cards = self.get_queryset()


		hvalList = [(0x1, True, 'type'), (0x40, False, 'type'), (0x80, False, 'type'), (0x2000, False, 'type'), (0x4000, False, 'type'), (0x800000, False, 'type')]
		hvalList = hvalList + listadd

		for card in cards:
			if(CFHelper.filterCardByHexList(card, hvalList)):
				yield card

	def getEDMCustomFilter(self, listadd):
		cards = self.get_queryset()

		hvalList = [(0x800000, True, 'type')]
		hvalList2 = [(0x2000, True, 'type')]
		hvalList = hvalList + listadd
		hvalList2 = hvalList2 + listadd

		for card in cards:
			if((CFHelper.filterCardByHexList(card, hvalList)
					or CFHelper.filterCardByHexList(card, hvalList2))):
				yield card
	def getMainDeckMonsters(self):
		cards = self.get_queryset()


		hvalList = [(0x1, True, 'type'), (0x40, False, 'type'), (0x80, False, 'type'), (0x2000, False, 'type'), (0x4000, False, 'type'), (0x800000, False, 'type')]

		for card in cards:
			if (CFHelper.filterCardByHexList(card,hvalList)):
				yield card

	def getST(self):
		cards = self.get_queryset()

		hvalList = [(0x2, True, 'type'), (0x80, False, 'type')]
		hvalList2 = [(0x4, True, 'type')]

		for card in cards:
			if(CFHelper.filterCardByHexList(card, hvalList) or CFHelper.filterCardByHexList(card, hvalList2)):
				yield card

	def getT(self):
		cards = self.get_queryset()

		for card in cards:

			if(CFHelper.filterCardByHex(card.type, 0x4, True)):
				yield card

	def getExtraDeckMonsters(self):
		cards = self.get_queryset()

		hvalList = [(0x800000, True, 'type')]
		hvalList2 = [(0x2000, True, 'type')]

		for card in cards:
			if(CFHelper.filterCardByHexList(card, hvalList)
					# Dunno if I should get fusions
					#and CFHelper.filterCardByHex(card.type, 0x40, True)
					or CFHelper.filterCardByHexList(card, hvalList2)):
				yield card


# This class represents a card, is called datas because I'm too lazy to rename a table
class Datas(models.Model):
    id = models.IntegerField(primary_key = True)
    ot = models.IntegerField(blank=True, null=True)
    alias = models.IntegerField(blank=True, null=True)
    setcode = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    atk = models.IntegerField(blank=True, null=True)
    def_field = models.IntegerField(db_column='def', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    level = models.IntegerField(blank=True, null=True)
    race = models.IntegerField(blank=True, null=True)
    attribute = models.IntegerField(blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    objects = CardDataManager()

    class Meta:
        managed = False
        db_table = 'datas'

    def __str__(self):
    	return str(self.type)

    def get_card_id(self):
    	return self.id


# This class represents a card's text, is called texts because 
class Texts(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    str1 = models.TextField(blank=True, null=True)
    str2 = models.TextField(blank=True, null=True)
    str3 = models.TextField(blank=True, null=True)
    str4 = models.TextField(blank=True, null=True)
    str5 = models.TextField(blank=True, null=True)
    str6 = models.TextField(blank=True, null=True)
    str7 = models.TextField(blank=True, null=True)
    str8 = models.TextField(blank=True, null=True)
    str9 = models.TextField(blank=True, null=True)
    str10 = models.TextField(blank=True, null=True)
    str11 = models.TextField(blank=True, null=True)
    str12 = models.TextField(blank=True, null=True)
    str13 = models.TextField(blank=True, null=True)
    str14 = models.TextField(blank=True, null=True)
    str15 = models.TextField(blank=True, null=True)
    str16 = models.TextField(blank=True, null=True)

    def __str__(self):
    	return self.name

    class Meta:
        managed = False
        db_table = 'texts'



class DeckManager(models.Manager):
	def createDeck(self, bonusid = 99,characterid = 99, deckSizeId = 99):
		ba = bytearray(struct.pack("f", time.time()))

		hashField = random_string(10)
		while(Deck.objects.filter(hashField = hashField).count() > 0):
			hashField = random_string(10)

		bonus = BonusGetter.BonusFactory(bonusid)
		character = CharacterGetter.CharacterFactory(characterid)
		mStarter = bonus.getMainStarterCards() + character.getMainStarterCards()
		eStarter = bonus.getExtraStarterCards() + character.getExtraStarterCards()
		
		mStarter = DraftController.getMainStarterCards(bonusid, characterid)
		eStarter = DraftController.getExtraStarterCards(bonusid, characterid)


		mainDeckLimit = DraftController.getMainDeckSize(bonusid, characterid, deckSizeId)
		extraDeckLimit = DraftController.getExtraDeckSize(bonusid, characterid, deckSizeId)

		deck = Deck.objects.create(hashField = hashField, bonusid = bonusid, characterid = characterid, mainDeckLimit = mainDeckLimit, extraDeckLimit = extraDeckLimit, curDraftNum = 0)
		for cardid in mStarter:
			deck.addStarters(cardid, True)

		for cardid in eStarter:
			deck.addStarters(cardid, False)

		return deck

	def retrieveDeck(self, hashfield):
		deck = Deck.objects.filter(hashField = hashfield)
		if not deck:
			return None
		return deck[0]



class Deck(models.Model):
	id = models.AutoField(primary_key = True)
	date = models.DateTimeField(default = timezone.now)
	hashField = models.TextField(max_length = 10)
	mainDeck = models.IntegerField(default = 0)
	extraDeck = models.IntegerField(default = 0)
	mainDeckLimit = models.IntegerField(default = 0)
	extraDeckLimit = models.IntegerField(default = 0)
	size = models.IntegerField(default = 0)
	bonusid = models.IntegerField(default = 99)
	characterid = models.IntegerField(default = 99)

	curDraftNum = models.IntegerField(default = 0)
	finished = models.BooleanField(default=False)
	draftFinished = models.BooleanField(default=False)
	tokens = models.IntegerField(default = 3)

	objects = DeckManager()



	def generateDraftList(self):

		lastEffect = self.pickdrafteffect_set.filter(draftnum = self.curDraftNum - 1)
		if (len(lastEffect) > 0) :
			effect = lastEffect[0].effect
		else:
			effect = 0
		mainDeck, randomCard = DraftController.generateDraftList(self.bonusid, self.characterid, self.mainDeck, self.extraDeck, self.mainDeckLimit, self.extraDeckLimit, effect)

		for i in randomCard:
			if isinstance(i, int):
				pk = i
			else:
				pk = i.pk;

			dETuple = (0, "")
			if(random.random() < 0.1):
					dETuple = DraftEffect.getDraftEffects()[DraftEffect.getRandom()]
			Draft.objects.create(deck = self,text = Texts.objects.get(pk = pk), card = Datas.objects.get(pk = pk), draftnum = self.curDraftNum, mainDeck = mainDeck, extraDeck = not mainDeck, effect = dETuple[0], effectString = dETuple[1])
		draftList = self.draft_set.filter(draftnum = self.curDraftNum)
		return draftList

	def generateTokenPurchaseList(self):
		#Since they are sharing the draft object might as well use num 1000

		pList = TokenPurchases.getBuyables()
		for p in pList:
			pk = p[0]
			cost = p[1]
			md = p[2]
			ed = p[3]
			Draft.objects.create(deck = self, text = Texts.objects.get(pk = pk), card = Datas.objects.get(pk = pk), draftnum = 1000, mainDeck = md, extraDeck = ed, tokenCost = cost)

		draftList = self.draft_set.filter(draftnum = 1000)
		return draftList



	def serveDraft(self):
		if self.finished == True:
			return None
		elif self.draftFinished == True:
			#set the shop picks to draft num 1000
			curDrafts = self.draft_set.filter(draftnum = 1000)
			if curDrafts.first() == None:
				return self.generateTokenPurchaseList()
			else:
				return curDrafts
		else:
			curDrafts = self.draft_set.filter(draftnum = self.curDraftNum)
			if curDrafts.first() == None:
				return self.generateDraftList()
			else:
				return curDrafts


	def addStarters(self, pk, mainDeck):
		self.addPick(pk, mainDeck, not mainDeck, False, 0)


	def addPick(self, pk, md, ed, other, gen):
		picks = self.pick_set.all().aggregate(Max('picknum'))


		if picks['picknum__max'] == None:
			newMax = 0

		else:
			newMax = picks['picknum__max'] + 1

		Pick.objects.create(deck = self, card = Datas.objects.get(pk = pk), text = Texts.objects.get(pk = pk), mainDeck = md, extraDeck = ed, other = other, picknum = newMax,generator = gen)
		self.size = self.size + 1
		if md:
			self.mainDeck = self.mainDeck + 1
		elif ed:
			self.extraDeck = self.extraDeck + 1

		self.save()




	def chooseDraft(self, draftid):
		if self.finished == True:
			return None


		#Token purchase section
		if self.draftFinished == True:
			if(draftid == 0):
				self.finished = True
				self.save()
			else:
				drafts = self.draft_set.filter(draftnum = 1000)
				for draft in drafts:
					if draft.card.id == draftid:
						if (self.tokens >= draft.tokenCost):
							self.addPick(draftid, draft.mainDeck, not draft.mainDeck, False, 2)
							self.tokens -= draft.tokenCost
							if (self.tokens <= 0):
								self.finished = True
							self.save()
							return draft
			
			return None


		# #Draft section

		# effArray = []
		# effArray.append((0, "No Effect"))
		# effArray.append((1, "If you pick this card, get 2 copies of it"))
		# effArray.append((2, "If you pick this card, draft 1 more main deck card"))
		# effArray.append((3, "If you pick this card, draft 3 more main deck cards"))
		# effArray.append((4, "If you pick this card, draft 2 less main deck cards"))
		# effArray.append((5, "If you pick this card, draft 1 more extra deck card"))
		# effArray.append((6, "If you pick this card, get 1 token"))
		# effArray.append((7, "If you pick this card, your next card draft has only 4 options"))
		# effArray.append((8, "If you pick this card, get 2 tokens"))
		# effArray.append((9, "If you pick this card, lose 1 token"))


		drafts = self.draft_set.filter(draftnum = self.curDraftNum)
		for draft in drafts:
			if draft.card.id == draftid:
				self.addPick(draftid, draft.mainDeck, not draft.mainDeck, False, 1)
				if (draft.effect == 1):
					self.addPick(draftid, draft.mainDeck, not draft.mainDeck, False, 1)
				elif(draft.effect == 2):
					self.mainDeckLimit += 1
				elif(draft.effect == 3):
					self.mainDeckLimit += 3
				elif(draft.effect == 4):
					self.mainDeckLimit -= 2
				elif(draft.effect == 5):
					self.extraDeckLimit += 1
				elif(draft.effect == 6):
					self.tokens += 1
				elif(draft.effect == 7):
					pass
				elif(draft.effect == 8):
					self.tokens += 2
				elif(draft.effect == 9):
					self.tokens -= 1

				PickDraftEffect.objects.create(deck = self, draftnum = self.curDraftNum, effect = draft.effect)

				self.curDraftNum = self.curDraftNum+1

				if ((self.mainDeck >= self.mainDeckLimit) and (self.extraDeck >= self.extraDeckLimit)):
					self.draftFinished = True

				self.save()
				return draft
		return None

	def finishDraft(self):
		#self.finished = True
		#self.save()

		#cannot voluntarily finish draft now
		pass

	def getDrafted(self):
		return self.draft_set.select_related('card').select_related('text').filter(picked = True)

	def getPicked(self):
		return self.pick_set.select_related('card').select_related('text').all()

	def getDraftedText(self, dlist = None):
		texts = []
		if dlist is not None:
			for d in dlist:
				texts.append(d.text)
		else:
			dlist = self.draft_set.filter(picked = True)
			for d in dlist:
				texts.append(d.text)

		return texts

	def getLatestDraft(self):
		return self.draft_set.select_related('card').select_related('text').get(picked = True, draftnum = self.size)

	def __str__(self):
		return self.hashField

class Pick(models.Model):

	id = models.AutoField(primary_key = True)
	deck = models.ForeignKey('Deck', on_delete = models.CASCADE, db_index = True)
	card = models.ForeignKey('Datas', on_delete = models.CASCADE, db_index = False)
	text = models.ForeignKey('Texts', on_delete = models.CASCADE, db_index = False)


	picknum = models.IntegerField()

	mainDeck = models.IntegerField()
	extraDeck = models.IntegerField()
	other = models.IntegerField()

	#0 is from draft, #1 is added automatically
	generator = models.IntegerField()


	def __str__(self):
		return str(self.draft.card.id)


class PickDraftEffect(models.Model):
	id = models.AutoField(primary_key = True)
	deck = models.ForeignKey('deck', on_delete = models.CASCADE, db_index = True)
	draftnum = models.IntegerField()
	effect = models.IntegerField(default = 0)




class Draft(models.Model):
	id = models.AutoField(primary_key = True)
	deck = models.ForeignKey('Deck', on_delete = models.CASCADE, db_index = True)
	card = models.ForeignKey('Datas', on_delete = models.CASCADE, db_index = False)
	text = models.ForeignKey('Texts', on_delete = models.CASCADE, db_index = False)
	draftnum = models.IntegerField()
	mainDeck = models.BooleanField()
	extraDeck = models.BooleanField()
	effect = models.IntegerField(default = 0)
	effectString = models.TextField(blank = True, null = False, default = "")
	tokenCost = models.IntegerField(default = 0)

	def getCard(self):
		return self.card


	def __str__(self):
		return str(self.card.id)

#### Draft Controller ####
'''
This thing manages the different draft effects and figures out which ones override which
'''

class DraftController:
	@staticmethod
	def getMainDeckSize(bonusid, characterid, deckSizeId):
		dp = BonusGetter.BonusFactory(bonusid).mainDeckSizePriority
		dp2 = CharacterGetter.CharacterFactory(characterid).mainDeckSizePriority
		md,ed = DeckSize.Factory(deckSizeId)
		if(dp == -1 and dp2 == -1):
			return md
		else:
			if(dp > dp2):
				return BonusGetter.BonusFactory(bonusid).getMainDeckSize(md)
			elif(dp < dp2):
				return CharacterGetter.CharacterFactory(characterid).getMainDeckSize(md)
			else:
				raise ValueError("DeckSize somehow has equal priority????")


	@staticmethod
	def getExtraDeckSize(bonusid, characterid, deckSizeId):
		dp = BonusGetter.BonusFactory(bonusid).extraDeckSizePriority
		dp2 = CharacterGetter.CharacterFactory(characterid).extraDeckSizePriority
		md,ed = DeckSize.Factory(deckSizeId)
		if(dp == -1 and dp2 == -1):
			return ed
		else:
			if(dp > dp2):
				return BonusGetter.BonusFactory(bonusid).getExtraDeckSize(ed)
			elif(dp < dp2):
				return CharacterGetter.CharacterFactory(characterid).getExtraDeckSize(ed)
			else:
				raise ValueError("DeckSize somehow has equal priority????")


	@staticmethod
	def getMainStarterCards(bonusid, characterid):
		return BonusGetter.BonusFactory(bonusid).getMainStarterCards() + CharacterGetter.CharacterFactory(characterid).getMainStarterCards()


	@staticmethod
	def getExtraStarterCards(bonusid, characterid):
		return BonusGetter.BonusFactory(bonusid).getExtraStarterCards() + CharacterGetter.CharacterFactory(characterid).getExtraStarterCards()

	@staticmethod
	def generateDraftList(bonusid, characterid, mainDeckSize, extraDeckSize, mainDeckLimit, extraDeckLimit, draftEffect):
		bonus = BonusGetter.BonusFactory(bonusid)
		character = CharacterGetter.CharacterFactory(characterid)



		if(bonus.chooseCardPriority > character.chooseCardPriority):
			mainDeck = bonus.modifyDraft(mainDeckSize, extraDeckSize, mainDeckLimit, extraDeckLimit)
		elif(bonus.chooseCardPriority < character.chooseCardPriority):
			mainDeck = character.modifyDraft(mainDeckSize, extraDeckSize, mainDeckLimit, extraDeckLimit)
		else:
			# Defaults to character
			mainDeck = character.modifyDraft(mainDeckSize, extraDeckSize, mainDeckLimit, extraDeckLimit)

		randomCard = []


		if (draftEffect == 7):
			numCards = 4
		else:
			numCards = 8

		if mainDeck:
			if(bonus.chooseMDMPriority > character.chooseMDMPriority):
				randomCard += bonus.modifyMDMCards(numCards/2, "code")
			elif(bonus.chooseMDMPriority < character.chooseMDMPriority):
				randomCard += character.modifyMDMCards(numCards/2, "code")
			else:
				# Defaults to character
				randomCard += character.modifyMDMCards(numCards/2, "code")

			if(bonus.chooseSTPriority > character.chooseSTPriority):
				randomCard += bonus.modifySTCards(numCards/2, "code")
			elif(bonus.chooseSTPriority < character.chooseSTPriority):
				randomCard += character.modifySTCards(numCards/2, "code")
			else:
				# Defaults to character
				randomCard += character.modifySTCards(numCards/2, "code")

			randomCard += character.addToMDMCards() + character.addToSTCards()

		else:
			if(bonus.chooseEDMPriority > character.chooseEDMPriority):
				randomCard += bonus.modifyEDMCards(numCards, "code")
			elif(bonus.chooseEDMPriority < character.chooseEDMPriority):
				randomCard += character.modifyEDMCards(numCards, "code")
			else:
				# Defaults to character
				randomCard += character.modifyEDMCards(numCards, "code")

			randomCard += character.addToEDMCards()


		return mainDeck, randomCard







#### DECK SIZE OPTIONS ####

class DeckSize:
	@staticmethod
	def Factory(deckSizeid):
		if deckSizeid == 0:
			return 32, 8
		elif deckSizeid == 1:
			return 40, 10
		elif deckSizeid == 2:
			return 48, 12




#### BONUS RELATED STUFFS, fuck code readability #####


class DraftHelper(object):

	@staticmethod
	def randomFromList(querylist, num, lmb=0):
		rcard = list(querylist)

		count = len(rcard)


		randomCard = []

		dolmb = inspect.isfunction(lmb)

		rands = []

		while len(randomCard) < num:

			rand = randint(0, count-1)
			while(rand in rands):
				rand = randint(0, count - 1)

			if dolmb:
				if(lmb(rcard[rand])):
					randomCard.append(rcard[rand])
					print(rcard[rand])
					rands.append(rand)
				else:
					pass
			else:
				randomCard.append(rcard[rand])
				rands.append(rand)


		return randomCard


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
	def modifySTCards():
		randomCard = DraftHelper.randomFromList(Datas.objects.getT(), 4)
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



### Character perks #####



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
	extraDeckSizePriority = 2

	@staticmethod
	def getExtraStarterCards():

		#starting #39 Utopia
		return [84013237]

	@staticmethod
	def getExtraDeckSize(eds):
		return eds*2



	# Double amount of extra deck monsters
	#1 to 4 ratio of extra to monster
	@staticmethod	
	def modifyDraft(mdsize, edsize, mdLimit, edLimit):
		missingMain = max(0,mdLimit - mdsize)
		missingExtra = max(0, edLimit - edsize)

		if ((missingMain == 0) and (missingExtra == 0)):
			ValueError("Should not generate")

		if (missingExtra * 2 <= missingMain):
			# return true for maindeck, false for extra deck
			return True

		else:
			return False

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


class TokenPurchases():


	@staticmethod
	def getBuyables():
		#Card id, token cost, maindeck, extradeck
		return ([(4923662, 1, True, False), #Chaos burst
			(56120475, 2, True, False),#Sakuretsu armor
			(81510157, 3, True, False), #Soul taker
			(51482758, 1, True, False), #remove trap
			(5318639, 2, True, False), #mst
			(43898403, 3, True, False), #twin twisters
			(71587526, 3, True, False), #karma cut
			(31222701, 1, True, False), #Wavering eyes
			(55144522, 3, True, False), #pot of greed
			(87979586, 3, True, False), #Angel trumpeter
			(70046172, 2, True, False), #rush recklessly
			 #Nothing at all, send 0 
			])

class DraftEffect():

	effects = 9

	@staticmethod
	def getDraftEffects():
		effArray = []
		effArray.append((0, "No Effect"))
		effArray.append((1, "If you pick this card, get 2 copies of it"))
		effArray.append((2, "If you pick this card, draft 1 more main deck card"))
		effArray.append((3, "If you pick this card, draft 3 more main deck cards"))
		effArray.append((4, "If you pick this card, draft 2 less main deck cards"))
		effArray.append((5, "If you pick this card, draft 1 more extra deck card"))
		effArray.append((6, "If you pick this card, get 1 token"))
		effArray.append((7, "If you pick this card, your next card draft has only 4 options"))
		effArray.append((8, "If you pick this card, get 2 tokens"))
		effArray.append((9, "If you pick this card, lose 1 token"))

		return effArray

	@staticmethod
	def getRandom():
		return randint(1, 9)