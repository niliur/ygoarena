from django.conf.urls import url

from . import views

urlpatterns = [ 
    url(r'^deck/create', views.deck_create, name='deck_create_api'),
    url(r'^deck/(?P<page_alias>.+?)/load', views.deck_load, name='deck_load_api'),
    url(r'^deck/(?P<page_alias>.+?)/drafts', views.get_drafts, name = 'drafts_load_api'),
    url(r'^deck/(?P<page_alias>.+?)/drafting', views.drafting, name = 'drafting_load_api'),
    url(r'^deck/(?P<page_alias>.+?)/cards', views.get_drafts_texts, name = 'texts_load_api'),
    url(r'^deck/(?P<page_alias>.+?)/current', views.drafting, name = 'drafting_api'),
    url(r'^deck/(?P<page_alias>.+?)/last', views.latest_draft, name = 'draft_latest_api'),
    url(r'^deck/(?P<page_alias>.+?)/generate', views.deck_generate, name='deck_get_api'),
    url(r'^deck/(?P<page_alias>.+?)/finish', views.deck_finish, name = 'deck_finish_api'),
    url(r'^deck/(?P<page_alias>.+?)/$', views.deck_load, name = 'deck_load_api'),
    #url(r'^deck/(?P<page_alias>.+?)/$', views.deckbuilder, name='deckbuilder')
]