'''
Views for teaching
'''
import datetime
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import render, redirect
from students.models import Student
from teaching.models import Teacher
from django.contrib.auth.forms import AuthenticationForm
from blog.models import BlogPost
from teaching.show_teacher_view import get_teachers_from_category
from school.school_year import get_current_school_year
from teaching.subject import Subject, SubjectCategory

def get_calendar(student):
    '''
    Helper function to get calendar
    '''
    student = Student.objects.get(pk=student)  # pylint: disable=no-member
    calendar = student.teacher.calendar
    return calendar

def get_date_time(date, time):
    start_time = str(date + ' ' + time)
    start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    return start

def get_end_time(start, student_id):
    '''
    Calculate end time
    '''
    date_and_time = start
    student = Student.objects.get(pk=student_id)
    lesson_form_minutes = student.lesson_form.minutes
    end_delta = timedelta(minutes=lesson_form_minutes)
    end_time = date_and_time + end_delta
    return end_time

def increment_counter(student_id):
    student = Student.objects.get(pk=student_id)
    student.lesson_count = F('lesson_count') + 1
    student.save()
    return student_id

def get_title(student, new_count):
    student = str(student)
    counter = str(new_count)
    title = student + ' ' + '(' + counter + ')'
    return title

def teaching_music_view (request):
    # Lade alle Fachgruppen-Kategorien
    categories = {}
    
    # Blasinstrumente (kombiniere Holz- und Blechblasinstrumente)
    brass_subjects = []
    try:
        brass_cat = SubjectCategory.objects.get(name="Blechblasinstrumente")
        brass_subjects.extend(list(Subject.objects.filter(
            category=brass_cat, 
            hidden_subject=False,
            complementary_subject=False
        )))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        wood_cat = SubjectCategory.objects.get(name="Holzblasinstrumente")
        brass_subjects.extend(list(Subject.objects.filter(
            category=wood_cat, 
            hidden_subject=False,
            complementary_subject=False
        )))
    except SubjectCategory.DoesNotExist:
        pass
    
    if brass_subjects:
        categories['blasinstrumente'] = brass_subjects
    
    # Elementare Musikerziehung
    try:
        eme_cat = SubjectCategory.objects.get(name="Elementare Musikerziehung")
        eme_subjects = list(Subject.objects.filter(
            category=eme_cat, 
            hidden_subject=False,
            complementary_subject=False
        ))
        if eme_subjects:
            categories['elementare_musikerziehung'] = eme_subjects
    except SubjectCategory.DoesNotExist:
        pass
    
    # Musikkunde
    try:
        theory_cat = SubjectCategory.objects.get(name="Musikkunde")
        theory_subjects = list(Subject.objects.filter(
            category=theory_cat, 
            hidden_subject=False,
            complementary_subject=False
        ))
        if theory_subjects:
            categories['musikkunde'] = theory_subjects
    except SubjectCategory.DoesNotExist:
        pass
    
    # Schlaginstrumente
    schlag_subjects = []
    try:
        schlag_cat = SubjectCategory.objects.get(name="Schlaginstrumente")
        schlag_subjects.extend(list(Subject.objects.filter(
            category=schlag_cat, 
            hidden_subject=False,
            complementary_subject=False
        )))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        schlagwerk_cat = SubjectCategory.objects.get(name="Schlagwerk")
        schlag_subjects.extend(list(Subject.objects.filter(
            category=schlagwerk_cat, 
            hidden_subject=False,
            complementary_subject=False
        )))
    except SubjectCategory.DoesNotExist:
        pass
    
    if schlag_subjects:
        categories['schlaginstrumente'] = schlag_subjects
    
    # Stimmbildung
    stimm_subjects = []
    try:
        stimm_cat = SubjectCategory.objects.get(name="Stimmbildung")
        stimm_subjects.extend(list(Subject.objects.filter(
            category=stimm_cat, 
            hidden_subject=False,
            complementary_subject=False
        )))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        gesang_cat = SubjectCategory.objects.get(name="Gesang")
        stimm_subjects.extend(list(Subject.objects.filter(
            category=gesang_cat, 
            hidden_subject=False,
            complementary_subject=False
        )))
    except SubjectCategory.DoesNotExist:
        pass
    
    if stimm_subjects:
        categories['stimmbildung'] = stimm_subjects
    
    # Streichinstrumente
    try:
        string_cat = SubjectCategory.objects.get(name="Streichinstrumente")
        string_subjects = list(Subject.objects.filter(
            category=string_cat, 
            hidden_subject=False,
            complementary_subject=False
        ))
        if string_subjects:
            categories['streichinstrumente'] = string_subjects
    except SubjectCategory.DoesNotExist:
        pass
    
    # Tanz und Bewegung
    try:
        dance_cat = SubjectCategory.objects.get(name="Tanz und Bewegung")
        dance_subjects = list(Subject.objects.filter(
            category=dance_cat, 
            hidden_subject=False,
            complementary_subject=False
        ))
        if dance_subjects:
            categories['tanz_und_bewegung'] = dance_subjects
    except SubjectCategory.DoesNotExist:
        pass
    
    # Tasteninstrumente
    try:
        keys_cat = SubjectCategory.objects.get(name="Tasteninstrumente")
        keys_subjects = list(Subject.objects.filter(
            category=keys_cat, 
            hidden_subject=False,
            complementary_subject=False
        ))
        if keys_subjects:
            categories['tasteninstrumente'] = keys_subjects
    except SubjectCategory.DoesNotExist:
        pass
    
    # Zupfinstrumente
    try:
        picked_cat = SubjectCategory.objects.get(name="Zupfinstrumente")
        picked_subjects = list(Subject.objects.filter(
            category=picked_cat, 
            hidden_subject=False,
            complementary_subject=False
        ))
        if picked_subjects:
            categories['zupfinstrumente'] = picked_subjects
    except SubjectCategory.DoesNotExist:
        pass
    
    return render(request, 'teaching/teaching_music.html', {'categories': categories})

def get_fachgruppe_context(category_name):
    """
    Generische Funktion um den Context für eine Fachgruppe zu erstellen
    Nutzt die gleiche Logik wie die ueber-uns Seite
    """
    try:
        category = SubjectCategory.objects.get(name=category_name)
    except SubjectCategory.DoesNotExist:
        return {'category_name': category_name, 'subjects': [], 'teachers': []}
    
    # Hole alle Fächer dieser Kategorie - filtere hidden und complementary subjects heraus
    subjects = Subject.objects.filter(
        category=category, 
        hidden_subject=False,
        complementary_subject=False
    )
    
    # Hole alle Lehrer dieser Kategorie mit der gleichen Funktion wie bei ueber-uns
    teachers = get_teachers_from_category(category_name)
    
    context = {
        'category': category,
        'category_name': category_name,
        'subjects': subjects,
        'teachers': teachers if teachers is not None else [],
    }
    
    return context

def teaching_brass_view (request):
    # Blasinstrumente umfasst sowohl Holz- als auch Blechblasinstrumente
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_brass = get_teachers_from_category("Blechblasinstrumente")
    teachers_wood = get_teachers_from_category("Holzblasinstrumente")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_brass | teachers_wood
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        brass_cat = SubjectCategory.objects.get(name="Blechblasinstrumente")
        brass_subjects = Subject.objects.filter(
            category=brass_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(brass_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        wood_cat = SubjectCategory.objects.get(name="Holzblasinstrumente")
        wood_subjects = Subject.objects.filter(
            category=wood_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(wood_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Blasinstrumente'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Fachgruppe der Blasinstrumente umfasst ein breites Spektrum, von Holzblasinstrumenten wie Querflöte, Klarinette und Saxophon bis hin zu Blechblasinstrumenten wie Trompete, Posaune und Horn. Der Unterricht, konzipiert nach dem in Österreich gültigen KOMU-Lehrplan (Konferenz der österreichischen Musikschulwerke) gemäß unseres vom Ministerium für Bildung genehmigten Organisationsstatuts, vermittelt den Studierenden eine solide technische Basis, einschließlich korrekter Atemführung, Tonbildung und musikalischer Gestaltung. Das Repertoire erstreckt sich von klassischen Werken über Jazzstandards bis hin zu zeitgenössischer Musik. Ziel ist die Entwicklung sowohl solistischer Fähigkeiten als auch der Kompetenz im Ensemblespiel, um eine aktive Teilnahme am vielfältigen Musikleben zu ermöglichen.'
    context['youtube_videos'] = ['aOCC8U4ldBI', 'HeTdrvqdkzg', 'AkXkj-1mOgg', 'GP04_HEJwvM', 'mYLesCKiU8E']
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_eme_view (request):
    # Elementare Musikerziehung und Musikalische Früherziehung
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_eme = get_teachers_from_category("Elementare Musikerziehung")
    teachers_mfe = get_teachers_from_category("Musikalische Früherziehung")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_eme | teachers_mfe
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        eme_cat = SubjectCategory.objects.get(name="Elementare Musikerziehung")
        eme_subjects = Subject.objects.filter(
            category=eme_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(eme_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        mfe_cat = SubjectCategory.objects.get(name="Musikalische Früherziehung")
        mfe_subjects = Subject.objects.filter(
            category=mfe_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(mfe_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Elementare Musikerziehung'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Elementare Musikerziehung (EMP) bildet die Basis für eine nachhaltige musikalische Entwicklung im Kindesalter, entsprechend den pädagogischen Richtlinien des in Österreich gültigen KOMU-Lehrplans (Konferenz der österreichischen Musikschulwerke) gemäß unseres vom Ministerium für Bildung genehmigten Organisationsstatuts. Im Zentrum steht die spielerische Annäherung an Musik durch Singen, rhythmische Bewegung, Tanz und den Umgang mit dem Orff-Instrumentarium. Dieses Fach fördert grundlegende musikalische Fertigkeiten, stimuliert die Kreativität und unterstützt die Entwicklung sozialer Kompetenzen. Die EMP verfolgt einen ganzheitlichen Ansatz, der die natürliche Musikalität der Kinder fördert und eine optimale Vorbereitung auf den weiterführenden Instrumental- oder Vokalunterricht darstellt.'
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_theory_view (request):
    # Musikkunde und Theorie
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_musikkunde = get_teachers_from_category("Musikkunde")
    teachers_theorie = get_teachers_from_category("Theorie")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_musikkunde | teachers_theorie
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        musikkunde_cat = SubjectCategory.objects.get(name="Musikkunde")
        musikkunde_subjects = Subject.objects.filter(
            category=musikkunde_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(musikkunde_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        theorie_cat = SubjectCategory.objects.get(name="Theorie")
        theorie_subjects = Subject.objects.filter(
            category=theorie_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(theorie_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Musikkunde'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Das Fach Musikkunde bietet eine umfassende Einführung in die Grundlagen der Musiktheorie und Gehörbildung, orientiert am in Österreich gültigen KOMU-Lehrplan (Konferenz der österreichischen Musikschulwerke) gemäß unseres vom Ministerium für Bildung genehmigten Organisationsstatuts. Die Lerninhalte umfassen Notationskunde, Rhythmusschulung, Harmonielehre sowie die Analyse musikalischer Formen und Strukturen. Darüber hinaus werden Einblicke in die Musikgeschichte und verschiedene Stilrichtungen vermittelt. Ziel des Musikkundeunterrichts ist es, das praktische Musizieren durch theoretisches Wissen zu ergänzen, das Hörvermögen zu schulen und ein tiefergehendes Verständnis für musikalische Zusammenhänge zu entwickeln, was für eine umfassende musikalische Bildung unerlässlich ist.'
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_drums_view (request):
    # Schlaginstrumente und Schlagwerk
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_schlag = get_teachers_from_category("Schlaginstrumente")
    teachers_schlagwerk = get_teachers_from_category("Schlagwerk")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_schlag | teachers_schlagwerk
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        schlag_cat = SubjectCategory.objects.get(name="Schlaginstrumente")
        schlag_subjects = Subject.objects.filter(
            category=schlag_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(schlag_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        schlagwerk_cat = SubjectCategory.objects.get(name="Schlagwerk")
        schlagwerk_subjects = Subject.objects.filter(
            category=schlagwerk_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(schlagwerk_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Schlaginstrumente'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Ausbildung an Schlaginstrumenten, basierend auf dem in Österreich gültigen KOMU-Lehrplan (Konferenz der österreichischen Musikschulwerke) gemäß unseres vom Ministerium für Bildung genehmigten Organisationsstatuts, umfasst ein vielseitiges Instrumentarium, darunter das klassische Orchester-Schlagwerk (z.B. Pauken, kleine Trommel), Mallet-Instrumente (Xylophon, Marimbaphon, Vibraphon) und das Drumset für Popularmusik und Jazz. Der Unterricht fokussiert auf die Entwicklung rhythmischer Präzision, technischer Fertigkeiten, koordinativer Fähigkeiten und musikalischer Ausdruckskraft. Die Studierenden werden auf das solistische Spiel sowie auf das Mitwirken in diversen Ensembles und Orchestern vorbereitet, wobei ein breites stilistisches Spektrum abgedeckt wird.'
    context['youtube_videos'] = ['w8yg-ZHYYAA']
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_vocal_view (request):
    # Stimmbildung und Gesang
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_stimm = get_teachers_from_category("Stimmbildung")
    teachers_gesang = get_teachers_from_category("Gesang")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_stimm | teachers_gesang
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        stimm_cat = SubjectCategory.objects.get(name="Stimmbildung")
        stimm_subjects = Subject.objects.filter(
            category=stimm_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(stimm_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        gesang_cat = SubjectCategory.objects.get(name="Gesang")
        gesang_subjects = Subject.objects.filter(
            category=gesang_cat, 
            hidden_subject=False,
            complementary_subject=False
        )
        subjects.extend(list(gesang_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Gesang'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Das Fach Stimmbildung und Gesang zielt auf die Kultivierung der Stimme als persönliches Musikinstrument ab, im Einklang mit den gesangspädagogischen Prinzipien gemäß dem in Österreich gültigen KOMU-Lehrplan (Konferenz der österreichischen Musikschulwerke) und unserem vom Ministerium für Bildung genehmigten Organisationsstatut. Im Vordergrund stehen die Erarbeitung einer gesunden Gesangstechnik durch Schulung von Atmung, Körperhaltung, Stütze, Artikulation und Resonanz. Das Repertoire umfasst verschiedene Epochen und Stilrichtungen. Der Unterricht fördert die Erweiterung des stimmlichen Umfangs, die Verbesserung der Intonation und die Entwicklung der interpretatorischen Fähigkeiten, um sowohl solistischen als auch chorischen Anforderungen gerecht zu werden.'
    context['youtube_videos'] = ['ESVykNyE3tY', '64DIUyJyXeM']
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_strings_view (request):
    context = get_fachgruppe_context('Streichinstrumente')
    context['intro_text'] = 'Die Streichinstrumente – Violine, Viola, Violoncello und Kontrabass – bilden eine zentrale Säule der abendländischen Musiktradition. Der Unterricht, ausgerichtet an den Standards des in Österreich gültigen KOMU-Lehrplans (Konferenz der österreichischen Musikschulwerke) gemäß unserem vom Ministerium für Bildung genehmigten Organisationsstatut, legt Wert auf eine fundierte technische Ausbildung, die Aspekte wie Haltung, Bogenführung, Intonation und Klanggestaltung umfasst. Die Studierenden erarbeiten ein breit gefächertes Repertoire, das solistische Literatur ebenso wie Kammermusik und Orchesterpartien einschließt. Ziel ist die Heranbildung versierter Instrumentalisten, die zur aktiven Teilnahme am Musikleben befähigt sind.'
    context['youtube_videos'] = ['rVTWes-vLL4', 'cI4jhzFOBoQ']
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_keys_view (request):
    context = get_fachgruppe_context('Tasteninstrumente')
    context['intro_text'] = 'Die Fachgruppe der Tasteninstrumente, zu der Klavier, Orgel, Cembalo, Akkordeon und elektronische Tasteninstrumente zählen, eröffnet den Zugang zu einem umfangreichen musikalischen Repertoire. Gemäß dem in Österreich gültigen KOMU-Lehrplan (Konferenz der österreichischen Musikschulwerke) und unserem vom Ministerium für Bildung genehmigten Organisationsstatut werden im Unterricht fundierte spieltechnische Fertigkeiten, musiktheoretisches Wissen sowie Kenntnisse in verschiedenen Stilrichtungen von der Alten Musik bis zur Moderne vermittelt. Die Ausbildung zielt darauf ab, die Studierenden sowohl zu solistischen Leistungen als auch zur kompetenten Liedbegleitung und zum Ensemblespiel zu befähigen.'
    context['youtube_videos'] = ['fi8ZGiB-lSc', 'NaTwXuR4VwM', 'Wh-uAzNYsLU', 'XhqeetX6NFo']
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_picked_view (request):
    context = get_fachgruppe_context('Zupfinstrumente')
    context['intro_text'] = 'Die Fachgruppe der Zupfinstrumente umfasst Instrumente wie Gitarre, E-Gitarre, Harfe, Hackbrett und Zither, die sich durch eine charakteristische Tonerzeugung und klangliche Vielfalt auszeichnen. Der Unterricht, orientiert am in Österreich gültigen KOMU-Lehrplan (Konferenz der österreichischen Musikschulwerke) gemäß unserem vom Ministerium für Bildung genehmigten Organisationsstatut, vermittelt die instrumentenspezifischen Spieltechniken und führt in ein breites musikalisches Spektrum ein, das von Volksmusik über Klassik bis hin zu Jazz und Pop reicht. Die Ausbildung fördert die musikalische Ausdrucksfähigkeit, die interpretatorische Kompetenz und die Vorbereitung auf solistische Darbietungen sowie das Musizieren in verschiedenen Ensembleformen.'
    context['youtube_videos'] = ['v30Zs04SwTU', 'CO9peHPN-_Q', 'jQUk2C51T5c', '2kBBFfEORmw']
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_dance_view (request):
    # Automatische Weiterleitung zur Tanz-und-Bewegung Hauptseite
    return redirect('/tanz-und-bewegung/')

def teaching_art_view (request):
    blog = BlogPost.objects.filter(category__category__name="Kunstschule")[0:6]
    teacher_art = get_teachers_from_category("Kunstschule")
    context = { 'blog': blog, 
                'teacher_art': teacher_art,}
    return render (request, 'teaching/teaching_art.html', context)

def teaching_prices_view (request):
    current_school_year = get_current_school_year()
    context = { 'current_school_year': current_school_year,}
    return render (request, 'teaching/prices.html', context)
