from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from . import views
import teaching.get_students
from teaching.get_students import get_all_students, get_student
from teaching.show_teacher_view import show_teacher_view

app_name = 'teaching'

urlpatterns = [
    path('ueber-uns', teaching.show_teacher_view.show_teacher_view, name="all_teachers"),
    path('bildungsangebot-musikschule', teaching.views.teaching_music_view, name="teaching_music"),
    path('bildungsangebot-musikschule/blasinstrumente', teaching.views.teaching_brass_view, name="teaching_brass"),
    path('bildungsangebot-musikschule/elementare-musikerziehung', teaching.views.teaching_eme_view, name="teaching_eme"),
    path('bildungsangebot-musikschule/musikkunde', teaching.views.teaching_theory_view, name="teaching_theory"),
    path('bildungsangebot-musikschule/schlaginstrumente', teaching.views.teaching_drums_view, name="teaching_drums"),
    path('bildungsangebot-musikschule/stimmbildung', teaching.views.teaching_vocal_view, name="teaching_vocal"),
    path('bildungsangebot-musikschule/streichinstrumente', teaching.views.teaching_strings_view, name="teaching_strings"),
    path('bildungsangebot-musikschule/tasteninstrumente', teaching.views.teaching_keys_view, name="teaching_keys"),
    path('bildungsangebot-musikschule/zupfinstrumente', teaching.views.teaching_picked_view, name="teaching_picked"),
    path('bildungsangebot-kunstschule', teaching.views.teaching_art_view, name="teaching_art"),
    path('beitraege-ermaessigungen', teaching.views.teaching_prices_view, name="teaching_prices"),
]
