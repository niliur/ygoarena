from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from django.http import HttpResponse, FileResponse, HttpResponseRedirect, Http404

from django.utils.html import escape
from wsgiref.util import FileWrapper

from django.db import transaction

from .models import *
from .serializers import *

import io

@api_view(['GET'])
def deck_load(request, page_alias):
    #7d0b761
    #Get past that thick protection

    page_alias = escape(page_alias)
    #Creates a new deck on post, or get an existing deck
    if request.method == 'GET':
        dm = DeckManager()

        deck = dm.retrieveDeck(page_alias)
        if deck == None:
            raise Http404("Deck does not exist")
        serializer = deckSerializer(deck,context={'request': request} ,many=False)
        print(serializer.data)
        return Response(serializer.data)

    return Response("No HAXX PLZ", status = status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['POST'])
def deck_create(request):

    if request.method == 'POST':
        dm = DeckManager()
        d = dm.createDeck()
        serializer = deckSerializer(d, context={'request': request}, many = False)
        return Response(serializer.data)
    else:
        return Response("No HAXX PLZ", status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_drafts(request, page_alias):

    page_alias = escape(page_alias)
    if request.method == 'GET':
        try:
            deck = Deck.objects.get(hashField=page_alias)
        except Deck.DoesNotExist:
            raise Http404("Deck does not exist")

        drafted = deck.getDrafted()
        serializer = draftSerializer(drafted, context={'request': request}, many = True)
        return Response(serializer.data)
    raise HttpResponse('Wrong use of api')

@api_view(['GET'])
def get_drafts_texts(request, page_alias):

    page_alias = escape(page_alias)
    if request.method == 'GET':
        try:
            deck = Deck.objects.get(hashField=page_alias)
        except Deck.DoesNotExist:
            raise Http404("Deck does not exist")

        drafted = deck.getDraftedText()
        serializer = textsSerializer(drafted, context={'request': request}, many = True)
        return Response(serializer.data)
    raise HttpResponse('Wrong use of api')

@transaction.atomic
@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def drafting(request, page_alias):

    page_alias = escape(page_alias)
    try:
        deck = Deck.objects.get(hashField=page_alias)
    except Deck.DoesNotExist:
        raise Http404("Deck does not exist")
    drafting = deck.serveDraft()
    if drafting == None:
        return HttpResponse('Deck finished')

    if request.method == 'GET':
        serializer = draftSerializer(drafting, context={'request': request}, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        print(request.data["id"])
        res = deck.chooseDraft(request.data["id"])
        if res == None:
            return HttpResponse('Card not found')
        serializer = cardsSerializer(res.getCard(), context = {'request': request}, many = False)
        return Response(serializer.data)
    raise HttpResponse('Wrong use of api')

@api_view(['POST'])
def deck_finish(request, page_alias):

    page_alias = escape(page_alias)
    try:
        deck = Deck.objects.get(hashField=page_alias)
    except Deck.DoesNotExist:
        raise Http404("Deck does not exist")
    if request.method == 'POST':
        if request.data["finish"]:
            deck.finishDraft()
            serializer = deckSerializer(deck, context = {'request': request}, many = False)
            return Response(serializer.data)

        return HttpResponse('invalid request')
    
    return HttpResponse('Wrong use of api')


@api_view(['GET'])
def latest_draft(request, page_alias):

    page_alias = escape(page_alias)
    try:
        deck = Deck.objects.get(hashField = page_alias)
    except Deck.DoesNotExist:
        raise Http404("Deck does not exist")
    latest = deck.getLatestDraft()

    if request.method == 'GET':
        if latest == None:
            raise Http404('Deck has no drafts')

        serializer = draftSerializer(latest, context={'request': request}, many = False)
        return Response(serializer.data)

    raise HttpResponse('Wrong use of api')

@api_view(['GET'])
def deck_generate(request, page_alias):

    page_alias = escape(page_alias)
    try:
        deck = Deck.objects.get(hashField = page_alias)
    except Deck.DoesNotExist:
        raise Http404("Deck does not exist")

    if request.method == 'GET':

        if deck.finished:
            drafts = deck.getDrafted()
            buf = io.StringIO()


            buf.write(u'#main\n')
            for draft in drafts:
                #journey to utf-8
                buf.write(str(draft.card.id).encode().decode("utf-8"))
                buf.write(u'\n')


            response = HttpResponse( content_type='text/ydk')
            response['Content-Disposition'] = 'attachment; filename="' + page_alias + '".ydk"'
            response.write(buf.getvalue())

            return response

        else:
            return Http404("deck not finished")

    raise HttpResponse('Wrong use of api')

