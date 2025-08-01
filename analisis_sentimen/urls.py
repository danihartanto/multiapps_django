# sentiment_app/urls.py

from django.urls import path
from .views import analyze_text, list_data_lexicon, update_lexicon_entry, add_lexicon_entry, delete_lexicon_entry, sentiment_history, delete_sentiment, update_sentiment

urlpatterns = [
    path('', analyze_text, name='analisis_sentimen'),
    path('data_lexicon/', list_data_lexicon, name='data_lexicon'),
    path('lexicon/update/', update_lexicon_entry, name='update_lexicon_entry'),
    path('lexicon/add/', add_lexicon_entry, name='add_lexicon_entry'),
    path('lexicon/delete/', delete_lexicon_entry, name='delete_lexicon_entry'),
    path('sentiment_history/', sentiment_history, name='sentiment_history'),
    path('sentiment_history/delete/<int:id>/', delete_sentiment, name='delete_sentiment'),
    path('sentiment_history/update/<int:id>/', update_sentiment, name='update_sentiment'),

    

]
