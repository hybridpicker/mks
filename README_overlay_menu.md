# Overlay Menu für MKS

Ein modernes, vollständig responsives Overlay-Menü für die MKS Django-Anwendung.

## Features

- **Vollbildschirm-Overlay** mit sanften Animationen
- **Strukturierte Navigation** in logische Kategorien unterteilt
- **Live-Statistiken** mit animierten Zahlen
- **Benutzerprofile-Verwaltung** direkt im Menü
- **Schnellaktionen** für häufige Aufgaben
- **Barrierefreiheit** mit vollständigem Fokus-Management
- **Responsive Design** für alle Bildschirmgrößen
- **Django-Integration** mit Template-Tags

## Installation

### 1. Dateien kopieren

Die folgenden Dateien sind bereits erstellt:

```
templates/navigation/
├── overlay_menu.html
└── demo.html

static/css/navigation/
└── overlay_menu.css

static/js/navigation/
└── overlay_menu.js
```

### 2. CSS einbinden

Füge das CSS in deine Base-Template ein:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/navigation/overlay_menu.css' %}">
```

### 3. HTML einbinden

Füge das Overlay-Menü in deine Navigation ein:

```html
<nav class="navbar">
    <div class="navbar-brand">MKS</div>
    <div class="navbar-right">
        {% include 'navigation/overlay_menu.html' %}
    </div>
</nav>
```

### 4. JavaScript einbinden

Vor dem schließenden `</body>` Tag:

```html
<script src="{% static 'js/navigation/overlay_menu.js' %}"></script>
```

## Anpassung

### 1. CSRF Token aktualisieren

Ersetze den statischen CSRF Token in der HTML-Datei:

```html
<!-- Ersetze diese Zeile: -->
<input type="hidden" name="csrfmiddlewaretoken" value="wWtSQrY0LXq6Z5h98HkI0iRhH3IjK0ayAltCfbCdSPWW21kGcbwzZVGJ4GTihwSY">

<!-- Mit: -->
{% csrf_token %}
```

### 2. Benutzerinformationen dynamisch laden

Ersetze die statischen Benutzerinformationen mit Django-Variablen:

```html
<!-- Statisch (ersetzen): -->
<h3>Schoensgibl</h3>
<p>l@l.at</p>
<span class="mks-overlay-user-badge">Administrator</span>

<!-- Dynamisch: -->
<h3>{{ user.get_full_name|default:user.username }}</h3>
<p>{{ user.email }}</p>
<span class="mks-overlay-user-badge">
    {% if user.is_superuser %}Administrator{% else %}{{ user.groups.first.name|default:"Benutzer" }}{% endif %}
</span>
```

### 3. Statistiken mit echten Daten

Erstelle einen Context Processor oder übergebe die Daten in deiner View:

```python
# views.py
def overlay_menu_context(request):
    return {
        'stats': {
            'new_registrations': User.objects.filter(date_joined__gte=timezone.now() - timedelta(days=7)).count(),
            'page_views': get_page_views_last_30_days(),  # Deine Implementierung
            'recent_blogs': BlogPost.objects.filter(created_at__gte=timezone.now() - timedelta(days=30)).count(),
            'gallery_images': GalleryImage.objects.count(),
        }
    }
```

Dann in der HTML:

```html
<span class="mks-overlay-stat-number">{{ stats.new_registrations }}</span>
<span class="mks-overlay-stat-label">Neue Anmeldungen (7T)</span>
```

### 4. Berechtigungen prüfen

Füge Django-Template-Bedingungen hinzu:

```html
{% if user.is_staff %}
<div class="mks-overlay-nav-section">
    <h3>Benutzer & Anmeldungen</h3>
    <!-- Navigation items -->
</div>
{% endif %}
```

## Erweiterte Features

### 1. Echte Statistik-Updates

Um die Statistiken in Echtzeit zu aktualisieren, erstelle eine API-Endpoint:

```python
# urls.py
path('api/stats/', views.overlay_stats_api, name='overlay_stats_api'),

# views.py
from django.http import JsonResponse

def overlay_stats_api(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    return JsonResponse({
        'new_registrations': User.objects.filter(date_joined__gte=timezone.now() - timedelta(days=7)).count(),
        'page_views': get_page_views_last_30_days(),
        'recent_blogs': BlogPost.objects.filter(created_at__gte=timezone.now() - timedelta(days=30)).count(),
        'gallery_images': GalleryImage.objects.count(),
    })
```

Dann passe das JavaScript an:

```javascript
// In overlay_menu.js, updateStats() method:
async updateStats() {
    try {
        const response = await fetch('/api/stats/');
        const data = await response.json();
        
        // Update the numbers with real data
        if (this.statsCards.registrations) {
            this.statsCards.registrations.querySelector('.mks-overlay-stat-number').textContent = data.new_registrations;
        }
        // ... weitere Updates
        
        this.animateNumbers();
    } catch (error) {
        console.error('Failed to update stats:', error);
    }
}
```

### 2. Benachrichtigungen

Füge Benachrichtigungsbadges hinzu:

```css
.mks-overlay-nav-item::after {
    content: attr(data-notification-count);
    position: absolute;
    top: -0.5rem;
    right: -0.5rem;
    background: #dc2626;
    color: white;
    border-radius: 50%;
    width: 1.25rem;
    height: 1.25rem;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
```

## Browser-Unterstützung

- Chrome (neueste 2 Versionen)
- Firefox (neueste 2 Versionen)
- Safari (neueste 2 Versionen)
- Edge (neueste 2 Versionen)

## Performance

Das Menü ist optimiert für Performance:

- CSS Grid für effizientes Layout
- Event Delegation für bessere Performance
- Lazy Loading für Statistiken
- Minimaler DOM-Impact wenn geschlossen

## Barrierefreiheit

- Vollständige Tastaturnavigation
- Screen Reader Unterstützung
- Fokus-Management
- ARIA-Labels und -Attribute
- Farbkontrast nach WCAG 2.1

## Demo

Eine Demo-Seite ist verfügbar unter `templates/navigation/demo.html`.

Starte deinen Django-Server und navigiere zu der entsprechenden URL um das Menü zu testen.
