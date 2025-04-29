-- Diese SQL-Datei aktualisiert die Kategorien für Kurse
-- Hinweis: Die Kategorien werden hauptsächlich durch Code bestimmt,
-- diese SQL-Befehle sind eine zusätzliche Absicherung

-- Für MySQL oder PostgreSQL

-- Aktualisiere Beschreibungen, die 'Klassisches Ballett' enthalten könnten
-- Dies ist optional, da die Kategorien in der Anwendung durch Code bestimmt werden
UPDATE dance_course 
SET description = REPLACE(description, 'Klassisches Ballett', 'Klassischer Tanz')
WHERE description LIKE '%Klassisches Ballett%';

-- Aktualisiere Kursnamen, falls erwünscht
-- Dies ist nur nötig, wenn tatsächlich der Name eines Kurses 'Klassisches Ballett' enthält
UPDATE dance_course 
SET name = REPLACE(name, 'Klassisches Ballett', 'Klassischer Tanz')
WHERE name LIKE '%Klassisches Ballett%';

-- Hinweis: Der Kurs "Zeitgenössischer Tanz - Fokus Improvisation & Tanztheater"
-- wird durch die Anpassung der Kategorie-Zuweisungslogik bereits als "Moderner Tanz" kategorisiert
-- Daher ist hier keine zusätzliche SQL-Operation erforderlich
