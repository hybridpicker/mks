"""
Diese Datei enthält die aktualisierte Kategorie-Zuweisungslogik für die Dance-App.
Sie wird von views.py importiert und überschreibt die ursprüngliche Funktion.
"""

def get_course_category(description):
    """Infers course category based on description."""
    if not description:
        return "Kindertanz"
        
    description_lower = description.lower()
    
    # Traditioneller Tanz
    if any(keyword in description_lower for keyword in [
        'klassischen balletts', 'vaganova-methode', 'klassischen tanzes', 
        'traditionellen methoden', 'historischer charaktertanz', 
        'volkstümlichen charaktertänzen', 'ballett', 'klassisch', 'traditionell'
    ]):
        return 'Klassischer Tanz'
    
    # Modernen Tanz
    elif any(keyword in description_lower for keyword in [
        'modern', 'zeitgenössischer tanz', 'contemporary', 'zeitgenössisch',
        'hiphop', 'funky moves', 'ausdruckstanz', 'jazz', 'urban', 'improvisation', 'tanztheater'
    ]):
        return 'Moderner Tanz'
    
    # Musical Dance
    elif any(keyword in description_lower for keyword in [
        'musical-tanz', 'musicals', 'musical', 'showdance', 'show'
    ]):
        return 'Musical Dance'
    
    # Kindertanz basierend auf Altersgruppe (wird in der view noch überprüft)
    elif any(keyword in description_lower for keyword in [
        'kinder', 'elementar', 'junge', 'spielerisch', 'kreativ', 'anfänger'
    ]):
        return 'Kindertanz'
    
    # Default Kategorie
    else:
        return 'Allgemeiner Tanz'
