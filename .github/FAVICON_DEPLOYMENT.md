# Favicon Deployment mit GitHub Actions

Diese Dokumentation erklärt, wie Sie die neuen Favicon-Dateien auf den Produktionsserver bereitstellen können, ohne direkten Zugriff auf den Server zu haben.

## Voraussetzungen

1. GitHub-Repository mit dem MKS-Projekt
2. Zugriff auf die Repository-Einstellungen, um Secrets hinzuzufügen
3. SSH-Zugriff auf den Produktionsserver (für die Einrichtung der Secrets)

## GitHub Secrets einrichten

Navigieren Sie zu Ihrem GitHub-Repository und gehen Sie zu "Settings" > "Secrets and variables" > "Actions