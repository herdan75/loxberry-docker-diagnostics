# LoxBerry Plugin: Docker & Portainer (Modernisierte Version)

Dieses Plugin basiert auf dem ursprünglichen LoxBerry Docker Plugin von Michael Miklis und wurde für LoxBerry 3.x vollständig modernisiert und stabilisiert.

Es integriert Docker sauber in die LoxBerry-Weboberfläche und bietet ein leichtgewichtiges, CGI-basiertes Dashboard zur Verwaltung und Analyse von Docker-Systemen.


## 📸 Screenshots

### 🔧 Portainer starten
Über das Docker-Plugin kann Portainer direkt gestartet werden.  
Der Status zeigt an, ob der Portainer‑Container läuft.

<img src="https://github.com/user-attachments/assets/021ff549-751f-4049-b488-43409bcc561a"
     alt="Docker Übersicht"
     style="max-width: 350px; width: 40%; height: auto;" />

Anmeldeseite öffnet sich:

<img src="https://github.com/user-attachments/assets/4747a8ba-2799-4b46-ab41-4f84b055f431"
     alt="Portainer Login"
     style="max-width: 350px; width: 20%; height: auto;" />


### 🔧 Docker‑Systemdiagnose
Die neue Diagnose‑Funktion (ab Version 2.2.0) analysiert:

* Docker‑Version  
* Installationsart (docker.io / docker‑ce / Script)  
* Architektur & Kernel  
* Paketquellen  
* Konflikte (z. B. Mischinstallation)  
* Update‑Status  
* Handlungsempfehlungen

Viele LoxBerry‑Systeme laufen auf ARM‑basierten Plattformen wie **aarch64**, **arm64** oder **meson64**.  
Diese Systeme verwenden oft unterschiedliche Kernel, Paketquellen oder Hersteller‑Images, die nicht vollständig mit den offiziellen Docker‑Paketen kompatibel sind.

Dadurch entstehen typische Probleme:

* Mischinstallationen (docker.io + docker‑ce gleichzeitig)
* veraltete Debian‑Pakete (`docker.io`)
* fehlende oder inkompatible Abhängigkeiten (`containerd.io`)
* nicht unterstützte Kernel‑Versionen auf ARM‑Boards
* unklare Installationsquellen (APT, Script, Hersteller‑Image)

Diese Fehler sind für den Benutzer kaum sichtbar — Docker „funktioniert irgendwie“, aber instabil.

<img src="https://github.com/user-attachments/assets/953ae1ea-b706-474a-a122-4440a44385f7"
     alt="Docker Diagnose"
     style="max-width: 350px; width: 40%; height: auto;" />

Beispiel eines Analyse‑Resultats:

<img src="https://github.com/user-attachments/assets/5b8b5157-5e21-4dbd-a70d-903f3b2b5fc9"
     alt="Docker Container Übersicht"
     style="max-width: 600px; width: 40%; height: auto;" />

👉 **Das Analysetool erkennt genau diese versteckten Probleme**, bewertet die Installation und gibt klare Handlungsempfehlungen, bevor Docker‑Container fehlerhaft laufen oder Updates scheitern.


### 🔧 Übersicht der Docker‑Container
Übersicht der laufenden Container und Status:

<img src="https://github.com/user-attachments/assets/d2c59a72-ed39-48ad-a7ba-edbff54d335f"
     alt="Docker UI"
     style="max-width: 350px; width: 40%; height: auto;" />

👉 Den Docker Container können auch die URL's zugeordnet werden. Nach dem Speichern kann der jeweilige Container durch **Ancklicken der URL** geöffnet werden.


## ✨ Features

### 🔥 Neu in Version 2.2.0

#### Diagnose & Systemanalyse
* Neue Docker‑Systemdiagnose integriert
* Erkennung der installierten Docker‑Version
* Analyse der Paketquellen (Debian docker.io vs Docker CE)
* Architektur‑ und Kernel‑Analyse (x86_64 / ARM64)
* Erkennung problematischer Paketkonstellationen
* Analyse der Docker‑Installationsart (docker.io / docker‑ce / Script)
* Erkennung potenzieller Mischinstallationen
* Erkennung von Update‑Konflikten
* Mixed‑Package‑Detection (containerd / containerd.io)
* Bewertung des Systemzustands mit klaren Handlungsempfehlungen
* Empfehlung zur sauberen Neuinstallation

#### Modernisierung & UI‑Verbesserungen
* Vollständig kompatibel mit LoxBerry 3.x
* Entfernung der Template‑Engine (keine HTML::Template‑Fehler mehr)
* Entfernung der Wiki‑Hilfe (keine Hilfe‑Crashes mehr)
* Modernes, CSS‑basiertes UI
* Stabilere Installation & Startlogik
* Portainer‑Statusanzeige (läuft / läuft nicht)
* Docker‑Containerliste (laufende Container)

#### Dateien & Struktur
* Neue Datei diagnose.cgi
* Erweiterte docker.css (Diagnose‑UI)
* Erweiterte index.cgi (Diagnose‑Button)
* Bereinigte plugin.cfg & release.cfg
* Verbesserte Plugin‑Struktur für zukünftige Erweiterungen
* Vorbereitung für AutoUpdate‑Release 2.2.0

### Standard‑Features (vom Original übernommen)
* Automatische Installation der Docker‑Engine
* Automatische Installation & Start von Portainer CE
* Integration in die LoxBerry‑Weboberfläche
* Verwaltung von Containern über Portainer


## 📦 Installation

1. ZIP herunterladen **oder Installation über den LoxBerry Plugin Manager (empfohlen)**  
2. LoxBerry Webinterface öffnen  
3. System → Pluginverwaltung  
4. Plugin installieren  
5. Plugin öffnen → Portainer starten  

Portainer ist erreichbar unter:
http://your-loxberry.local:9000



## 🧩 Voraussetzungen
* LoxBerry 3.x  
* Internetzugang für Docker‑Installation  


## 🛠 Troubleshooting & Hinweise

Dieses Plugin installiert Docker und Portainer, bietet aber keinen Support für Docker‑Container selbst.

Für Feedback oder Fehlerberichte:

👉 https://www.loxforum.com/forum/projektforen/loxberry/plugins/165754-plugin-docker-und-portainer-io

Auf einigen ARM64‑basierten Distributionen oder Spezialsystemen (z. B. Armbian / meson64) kann die Installation über klassische Docker‑APT‑Repositories eingeschränkt sein.

Empfohlen:
https://get.docker.com



## 🔧 Technische Hinweise
Die Docker-Systemdiagnose dient ausschließlich der Analyse und Bewertung der lokalen Docker-Installation.  
Es werden **keine automatischen Änderungen** am System durchgeführt.  


## 🆕 Change‑Log

### 2026‑05‑12 – Release 2.2.0
* Neue Docker‑Systemdiagnose integriert
* diagnose.cgi hinzugefügt
* index.cgi erweitert (Diagnose‑Button)
* docker.css erweitert (Diagnose‑Styles)
* Verbesserte Plugin‑Struktur
* Vorbereitung für AutoUpdate‑Release

### 2026‑05‑12 – Release 2.1.1 (Modernisierte Version)
* LB3‑kompatible Oberfläche
* Entfernung der Template‑Engine
* Entfernung der Wiki‑Hilfe (Crash‑Fix)
* Automatische IP‑Erkennung
* Modernes UI
* Portainer‑Statusanzeige
* Docker‑Containerliste
* Stabilere Installation
* Bereinigung der plugin.cfg & release.cfg
* ZIP‑Erstellungsskript hinzugefügt

### 2022‑12‑22 – Release 2.1.0
* Auto‑Update‑Support

### 2022‑12‑13 – Release 2.0.2
* Wechsel zu portainer/portainer-ce:latest

### 2019‑12‑31 – Release 2.0.1
* Support für LoxBerry 2.0.0.4
* Portainer 1.23.0

### 2018‑11‑16 – Release 1.1.0
* Größeres iFrame
* Portainer 1.19.1

### 2018‑08‑27 – Release 1.0.0
* Initial Release


## ⚠️ Known Issues
Aktuell keine reproduzierbaren Probleme bekannt.


## 📝 Lizenz
Dieses Projekt basiert auf dem ursprünglichen  
„loxberry-plugin-docker“ von Michael Miklis.  
https://github.com/michaelmiklis/loxberry-plugin-docker  

Veröffentlicht unter **Apache License 2.0**.  

Eigene Erweiterungen, Modernisierungen und Diagnosefunktionen:  
© 2026 Daniel Hermann


## 🙏 Credits
* Originalprojekt: Michael Miklis  
* Modernisierung & Weiterentwicklung: Daniel Hermann


