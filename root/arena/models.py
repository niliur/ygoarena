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



class CardDataManager(models.Manager):

	
	def getMainDeckMonsters(self):
		cards = self.get_queryset()

		for card in cards:
			if (CFHelper.filterCardByHex(card.type, 0x1, True) 
					and CFHelper.filterCardByHex(card.type, 0x40, False) 
					and CFHelper.filterCardByHex(card.type, 0x80, False) 
					and CFHelper.filterCardByHex(card.type, 0x2000, False)
					and CFHelper.filterCardByHex(card.type, 0x800000, False)
					and CFHelper.filterCardByHex(card.type, 0x4000, False) ):
				yield card

	def getST(self):
		cards = self.get_queryset()

		for card in cards:

			if((CFHelper.filterCardByHex(card.type, 0x2, True)
					and CFHelper.filterCardByHex(card.type, 0x80, False))
					or CFHelper.filterCardByHex(card.type, 0x4, True)):
				yield card

	def getT(self):
		cards = self.get_queryset()

		for card in cards:

			if(CFHelper.filterCardByHex(card.type, 0x4, True)):
				yield card

	def getExtraDeckMonsters(self):
		cards = self.get_queryset()

		for card in cards:
			if(CFHelper.filterCardByHex(card.type, 0x800000, True)
					# Dunno if I should get fusions
					#and CFHelper.filterCardByHex(card.type, 0x40, True)
					or CFHelper.filterCardByHex(card.type, 0x2000, True)):
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
	def createDeck(self, bonusid = 99, deckSizeid = 99):
		ba = bytearray(struct.pack("f", time.time()))

		hashField = random_string(10)
		while(Deck.objects.filter(hashField = hashField).count() > 0):
			hashField = random_string(10)

		bonus = BonusGetter.BonusFactory(bonusid)
		mStarter = bonus.getMainStarterCards()
		eStarter = bonus.getExtraStarterCards()
		
		dsid = bonus.getDeckSizeid()
		if dsid is not None:
			deckSizeid = dsid

		deck = Deck.objects.create(hashField = hashField, bonusid = bonusid, deckSizeid = deckSizeid)
		for cardid in mStarter:
			deck.addStarters(cardid, True)

		print("cunt")
		for cardid in eStarter:
			deck.addStarters(cardid, False)

		print("cuck")
		return deck

	def retrieveDeck(self, hashfield):
		deck = Deck.objects.filter(hashField = hashfield)
		if not deck:
			return None
		return deck[0]



class Deck(models.Model):
	id = models.AutoField(primary_key = True)
	date = models.DateTimeField(default = timezone.now)
	finished = models.BooleanField(default=False)
	hashField = models.TextField(max_length = 10)
	mainDeck = models.IntegerField(default = 0)
	extraDeck = models.IntegerField(default = 0)
	size = models.IntegerField(default = 0)
	deckSizeid = models.IntegerField(default = 0)
	bonusid = models.IntegerField(default = 0)

	objects = DeckManager()

	def randomFromList(self, querylist, num):
		rcard = list(querylist)

		count = len(rcard)

		randc = [randint(0, count-1) for x in range(num)]

		randomCard = []
		for x in randc:
			randomCard.append(rcard[x])
			#[rcard[x] for x in randc]
		return randomCard

	def getMDM(self, count):
		#rcard = Datas.objects.exclude(type=16401)
		rcard = Datas.objects.getMainDeckMonsters()
		return self.randomFromList(rcard, count)
		

	def getSandT(self, count):
	#rcard = Datas.objects.exclude(type=16401)
		rcard = Datas.objects.getST()

		return self.randomFromList(rcard, count)

	def getEDM(self, count):
		rcard = Datas.objects.getExtraDeckMonsters()
		return self.randomFromList(rcard, count)

	


	def generateDraftList(self):

		mainDeck, randomCard = BonusGetter.BonusFactory(self.bonusid).modifyDraft(self.mainDeck, self.extraDeck)

		for i in randomCard:
			pk = i.pk;
			Draft.objects.create(deck = self,text = Texts.objects.get(pk = pk), card = Datas.objects.get(pk = pk), draftnum = self.size+1, mainDeck = mainDeck)
		draftList = self.draft_set.filter(draftnum = self.size + 1)
		return draftList

	def serveDraft(self):
		if self.finished == True:
			return None
		curDrafts = self.draft_set.filter(draftnum = self.size + 1)
		if curDrafts.first() == None:
			return self.generateDraftList()
		else:
			return curDrafts

	def addStarters(self, pk, mainDeck):
		print(pk)
		Draft.objects.create(deck = self,text = Texts.objects.get(pk = pk), card = Datas.objects.get(pk = pk), draftnum = self.size+1, mainDeck = mainDeck)
		self.chooseDraft(pk)

	def chooseDraft(self, draftid):
		if self.finished == True:
			return None

		drafts = self.draft_set.filter(draftnum = self.size + 1)
		for draft in drafts:
			if draft.draftnum == (self.size + 1):
				if draft.card.id == draftid:
					draft.picked = True
					self.size = self.size+1
					if draft.mainDeck:
						self.mainDeck = self.mainDeck+1
						if (self.mainDeck >= DeckSize.Factory(self.deckSizeid)):
							self.finished = True
					else:
						self.extraDeck = self.extraDeck+1
					draft.save()
					self.save()
					return draft
		return None

	def finishDraft(self):
		self.finished = True
		self.save()

	def getDrafted(self):
		return self.draft_set.select_related('card').select_related('text').filter(picked = True)

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


class Draft(models.Model):
	id = models.AutoField(primary_key = True)
	deck = models.ForeignKey('Deck', on_delete = models.CASCADE, db_index = True)
	card = models.ForeignKey('Datas', on_delete = models.CASCADE, db_index = False)
	text = models.ForeignKey('Texts', on_delete = models.CASCADE, db_index = False)
	date = models.DateTimeField(auto_now = True)
	draftnum = models.IntegerField()
	picked = models.BooleanField(default=False)
	mainDeck = models.BooleanField()

	def getCard(self):
		return self.card


	def __str__(self):
		return str(self.card.id)

#### DECK SIZE OPTIONS ####

class DeckSize:
	@staticmethod
	def Factory(deckSizeid):
		if deckSizeid == 0:
			return 40
		elif deckSizeid == 1:
			return 48
		elif deckSizeid == 2:
			return 60
		elif deckSizeid == 3:
			return 70
		else:
			return 40




#### BONUS RELATED STUFFS, fuck code readability #####


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
	bonusID = 0

	@staticmethod
	def getMainStarterCards():
		#Exodia pieces, Battle Fader, Factory of Mass production
		return []

	@staticmethod
	def getExtraStarterCards():
		return []

	@staticmethod	
	def modifyDraft(mdsize, edsize):


		if (edsize * 4 <= mdsize):
			rcard = Datas.objects.getExtraDeckMonsters()
			#rcard = self.get_queryset()
			randomCard = DraftHelper.randomFromList(rcard, 8)
			#randomCard = self.getEDM(6)
			mainDeck = False

		else:
			randomCard = DraftHelper.randomFromList(Datas.objects.getMainDeckMonsters(), 4) + DraftHelper.randomFromList(Datas.objects.getST(), 4)
			mainDeck = True	

		return mainDeck, randomCard

	@staticmethod
	def getDeckSizeid():
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
		#5 and over club: 1 x Tribute burial, 1 x Stormforth, 1 x Dark Squire, Double summon
		return [80230510, 79844764,59463312, 43422537]

class TrapBonus(DefaultBonus):

	@staticmethod
	def getMainStarterCards():
		#Powerful rebirth, quaking mirror force
		return [84298614, 40838625]


	@staticmethod	
	def modifyDraft(mdsize, edsize):


		if (edsize * 4 <= mdsize):
			rcard = Datas.objects.getExtraDeckMonsters()
			#rcard = self.get_queryset()
			randomCard = DraftHelper.randomFromList(rcard, 8)
			#randomCard = self.getEDM(6)
			mainDeck = False

		else:
			randomCard = DraftHelper.randomFromList(Datas.objects.getMainDeckMonsters(), 4) + DraftHelper.randomFromList(Datas.objects.getT(), 4)
			print("fuck you")
			mainDeck = True	

		return mainDeck, randomCard

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
	@staticmethod
	def getMainStarterCards():
		#3x lawnmowing, imp sabres, plaguespreader, electroturtle, shadoll beast
		return [11110587, 11110587, 11110587, 30068120, 33420078,34710660,3717252]

	@staticmethod
	def getDeckSizeid():
		return 3