-- Erstelle die maintenance_maintenancemode Tabelle
CREATE TABLE IF NOT EXISTS maintenance_maintenancemode (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    title VARCHAR(200) NOT NULL DEFAULT 'Wartungsarbeiten',
    message TEXT NOT NULL DEFAULT 'Wir führen gerade ein Update durch und sind bald wieder für Sie da!',
    expected_downtime VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Füge die Migration zur django_migrations Tabelle hinzu
INSERT INTO django_migrations (app, name, applied) 
VALUES ('maintenance', '0001_initial', CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;