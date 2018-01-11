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
import string
import inspect
from django.db.models import Max
import math
from random import * 
import random

def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))


class CFHelper(object):
	@staticmethod
	def filterCardByHex(code, hval, boolean = True):
		# for card in cards:
		# 	if (card.type & hval == bool):
		# 		yield card
		if((code & hval) == hval):
			return boolean
		return not boolean


	@staticmethod
	def filterCardByHexList(code, hvalList):

		ret = True
		for hval in hvalList:
			target = getattr(code, hval[2])
			if((target & hval[0]) == hval[0]):
				if(not hval[1]):
					return False
			else:
				if(hval[1]):
					return False;

		return True
	



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
    	return 'type' + str(self.type) + 'setcode' + str(self.setcode)

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

			dETuple = DraftEffect.getDraftEffects()[DraftController.generateDraftEffect(self.bonusid, self.characterid)]
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

	@staticmethod
	def generateDraftEffect(bonusid, characterid):

		bonus = BonusGetter.BonusFactory(bonusid)
		character = CharacterGetter.CharacterFactory(characterid)
		code = None
		if(bonus.chooseDraftOptionsPriority > 0):
			code = bonus.getDraftEffect()
		if(character.chooseDraftOptionsPriority > 0):
			code = character.getDraftEffect(code)

		if code is None:
			if(random.random() < 0.1):
				code = randint(1, 9)
			else:
				code = 0


		if(bonus.alterDraftOptionsPriority > character.alterDraftOptionsPriority):
			code = bonus.alterDraftOption(code)
			code = character.alterDraftOption(code)
		else:
			code = character.alterDraftOption(code)
			code = bonus.alterDraftOption(code)

		return code






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


from .bonus import *


### Character perks #####


from .character import *

from .drafteffect import *
from .tokenpurchase import *