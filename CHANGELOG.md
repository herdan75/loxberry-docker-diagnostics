# Changelog

Alle relevanten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.
## Unreleased (develop)

### Neu
- Docker-Diagnose um Daemon-Status, Portainer-Status, Portfreigaben, Docker Compose, APT-Updates und Speicherplatz erweitert
- GitHub Actions Validierung für Shell-, Perl-CGI- und Plugin-Metadaten ergänzt

### Geändert
- Portainer-Installation nutzt einen stabileren Image-Kanal und erkennt den Container exakt
- Service-URL-Verwaltung speichert per POST und zeigt vorhandene Zuordnungen im Formular an
- README um Sicherheits- und Betriebshinweise erweitert

### Behoben
- Verwechslung von portainer mit ähnlich benannten Containern verhindert
- Service-URLs werden auf http:// und https:// begrenzt
- JSON-Speicherung der Service-URLs gegen parallele Schreibzugriffe gehärtet

---


---

## v2.4.0-beta.1

### Neu
- GitHub Actions für automatische ZIP-Erstellung integriert
- Stable- und PreRelease-System eingeführt
- Automatische Release-Erstellung bei Git-Tags vorbereitet
- README modernisiert
- Release- und PreRelease-Links ergänzt

### Geändert
- Projektstruktur für zukünftige Releases verbessert
- Download-Bereitstellung über GitHub Releases vorbereitet
- Trennung zwischen Stable-Version und Beta-Version eingeführt

---

## v2.3.0

### Neu
- Docker-Systemdiagnose integriert
- Analyse der installierten Docker-Version
- Analyse der Installationsart
- Erkennung von docker.io / docker-ce / Script-Installationen
- Architektur- und Kernelanalyse
- Paketquellen-Analyse
- Erkennung von Mischinstallationen
- Mixed-Package-Detection für containerd / containerd.io
- Update-Status und Handlungsempfehlungen

### Geändert
- Plugin-Struktur verbessert
- UI modernisiert
- Docker-Containerübersicht verbessert
- Portainer-Statusanzeige verbessert
- Vorbereitung für GitHub Releases

---

## v2.2.1

### Geändert
- Oberfläche für LoxBerry 3.x modernisiert
- Alte Template-Engine entfernt
- Wiki-Hilfe entfernt
- Stabilere Installation
- Automatische IP-Erkennung verbessert
- Modernes CSS-basiertes UI eingeführt

---

## v2.1.0

### Neu
- AutoUpdate-Support ergänzt

---

## v2.0.2

### Geändert
- Wechsel zu `portainer/portainer-ce:latest`

---

## v2.0.1

### Geändert
- Support für LoxBerry 2.0.0.4
- Portainer auf Version 1.23.0 angepasst

---

## v1.1.0

### Geändert
- Größeres iFrame
- Portainer 1.19.1

---

## v1.0.0

### Neu
- Initial Release
