"""
Diese Datei enthält einen einfachen SQL-Befehl, der in der Produktionsumgebung ausgeführt werden kann,
um die location-Spalte hinzuzufügen und Standorte zuzuweisen.

Hinweis: Dies ist kein Migrations-Skript, sondern ein einfaches SQL-Skript, 
das direkt in der Datenbank ausgeführt werden kann.

Verwendung (MySQL):
---------------------
mysql -u [username] -p [database] < production_fix.sql

Verwendung (PostgreSQL):
---------------------
psql -U [username] -d [database] -f production_fix.sql
"""

# MySQL Version:
"""
-- Prüfen, ob die Spalte bereits existiert
SET @columnExists = 0;
SELECT COUNT(*) INTO @columnExists FROM information_schema.columns 
WHERE table_name = 'dance_timeslot' AND column_name = 'location' AND table_schema = DATABASE();

-- Spalte hinzufügen, falls sie nicht existiert
SET @query = IF(@columnExists = 0, 
                'ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100) NULL', 
                'SELECT "Spalte existiert bereits"');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Standorte zuweisen
UPDATE dance_timeslot
JOIN dance_course ON dance_timeslot.course_id = dance_course.id
JOIN dance_teacher ON dance_course.teacher_id = dance_teacher.id
SET dance_timeslot.location = 
    CASE 
        WHEN dance_teacher.name LIKE '%Zeisel%' OR dance_teacher.name LIKE '%Bauer%' THEN 'Campus'
        WHEN dance_teacher.name LIKE '%Usmanova%' THEN 'Kulturhaus Wagram'
        WHEN dance_teacher.name LIKE '%Grüssinger%' OR dance_teacher.name LIKE '%Holzweber%' THEN 'Kulturhaus Spratzern'
        ELSE 'Campus'
    END;
"""

# PostgreSQL Version:
"""
-- Prüfen, ob die Spalte bereits existiert und hinzufügen, falls nicht
DO $$
BEGIN
    IF NOT EXISTS(SELECT 1 FROM information_schema.columns 
                 WHERE table_name='dance_timeslot' AND column_name='location') THEN
        ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100) NULL;
    END IF;
END $$;

-- Standorte zuweisen
UPDATE dance_timeslot
SET location = 
    CASE 
        WHEN t.name LIKE '%Zeisel%' OR t.name LIKE '%Bauer%' THEN 'Campus'
        WHEN t.name LIKE '%Usmanova%' THEN 'Kulturhaus Wagram'
        WHEN t.name LIKE '%Grüssinger%' OR t.name LIKE '%Holzweber%' THEN 'Kulturhaus Spratzern'
        ELSE 'Campus'
    END
FROM dance_course c
JOIN dance_teacher t ON c.teacher_id = t.id
WHERE dance_timeslot.course_id = c.id;
"""

# SQLite Version (für lokale Entwicklung):
"""
-- SQLite unterstützt keine IF EXISTS für ALTER TABLE Befehle,
-- daher müssen wir es anders handhaben

-- Spalte hinzufügen
ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100);

-- Standorte zuweisen
-- In SQLite müssen mehrere UPDATE-Anweisungen verwendet werden

-- Zeisel und Bauer
UPDATE dance_timeslot
SET location = 'Campus'
WHERE course_id IN (
    SELECT c.id FROM dance_course c
    JOIN dance_teacher t ON c.teacher_id = t.id
    WHERE t.name LIKE '%Zeisel%' OR t.name LIKE '%Bauer%'
);

-- Usmanova
UPDATE dance_timeslot
SET location = 'Kulturhaus Wagram'
WHERE course_id IN (
    SELECT c.id FROM dance_course c
    JOIN dance_teacher t ON c.teacher_id = t.id
    WHERE t.name LIKE '%Usmanova%'
);

-- Grüssinger und Holzweber
UPDATE dance_timeslot
SET location = 'Kulturhaus Spratzern'
WHERE course_id IN (
    SELECT c.id FROM dance_course c
    JOIN dance_teacher t ON c.teacher_id = t.id
    WHERE t.name LIKE '%Grüssinger%' OR t.name LIKE '%Holzweber%'
);

-- Default für alle restlichen
UPDATE dance_timeslot
SET location = 'Campus'
WHERE location IS NULL;
"""
