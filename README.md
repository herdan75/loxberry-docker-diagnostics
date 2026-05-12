### **LoxBerry Plugin: Docker \& Portainer (Modernisierte Version)**

Dieses Plugin basiert auf dem ursprünglichen LoxBerry Docker Plugin von Michael Miklis (michaelmiklis)

und wurde umfangreich modernisiert, aktualisiert und für LoxBerry 3.x angepasst.



Das Plugin installiert die Docker‑Engine auf dem LoxBerry und richtet automatisch

Portainer CE für die grafische Verwaltung von Containern ein.



Es integriert Docker sauber in die LoxBerry‑Weboberfläche und bietet ein modernes Dashboard mit:

* Portainer‑Statusanzeige
* Docker‑Containerliste
* automatische IP‑Erkennung 
* modernes UI
* stabiler, templatefreier CGI‑Implementierung
* neuer Docker‑Systemdiagnose‑Funktion (ab Version 2.2.0)





### ✨ Features



##### 🔥 Neu in Version 2.2.0

* Docker-Systemdiagnose integriert
* Erkennung der installierten Docker-Version
* Analyse der Paketquellen (Debian vs Docker CE)
* Architektur- und Systemanalyse (x86\_64 / ARM64)
* Erkennung problematischer Paketkonstellationen
* Analyse der Docker-Installationsart
* Erkennung potenzieller Mischinstallationen
* Intelligente Systembewertung mit Handlungsempfehlung
* Erkennung von Update-Konflikten
* Mixed-Package-Detection (containerd / containerd.io)
* Empfehlung zur sauberen Neuinstallation
* Neue Datei diagnose.cgi
* Erweiterte docker.css für Diagnose-UI
* Erweiterte index.cgi mit Diagnose-Button
* Verbesserte Struktur für zukünftige Erweiterungen
* Vorbereitung für AutoUpdate-Release 2.2.0



##### 🔥 Neu in der modernisierten Version (2.1.x → 2.2.x)

* Vollständig kompatibel mit LoxBerry 3.x
* Entfernung der Template‑Engine (keine HTML::Template‑Fehler mehr)
* Entfernung der Wiki‑Hilfe (keine Hilfe‑Crashes mehr)
* Automatische Erkennung der LoxBerry‑IP
* Portainer‑Statusanzeige (läuft / läuft nicht)
* Docker‑Containerliste (laufende Container)
* Modernes UI (CSS‑basiert)
* Stabilere Installation \& Startlogik
* Bereinigte plugin.cfg \& release.cfg
* ZIP‑Erstellungsskript für Entwickler



##### Standard‑Features (vom Original übernommen)

* Automatische Installation der Docker‑Engine
* Automatische Installation \& Start von Portainer CE
* Integration in die LoxBerry‑Weboberfläche
* Verwaltung von Containern über Portainer



##### 📦 Installation

1\. ZIP herunterladen **oder Installation über den LoxBerry Plugin Manager (empfohlen)**

2\. LoxBerry Webinterface öffnen

3\. System → Pluginverwaltung

4\. Plugin installieren

5\. Plugin öffnen → Portainer starten

Nach erfolgreicher Installation ist Portainer erreichbar unter:

Portainer is available at:
http://<LoxBerry IP>:9000



##### 🧩 Voraussetzungen

* LoxBerry 3.x
* Internetzugang für Docker‑Installation



##### 🛠 Troubleshooting \& Hinweise

Dieses Plugin installiert Docker und Portainer, bietet aber keinen Support für Docker‑Container selbst.

Docker ist ein komplexes System — für Container‑Konfigurationen gibt es zahlreiche Tutorials, Videos und Dokumentationen.

Für Plugin‑Feedback oder Fehlerberichte kann weiterhin der ursprüngliche LoxForum‑Thread genutzt werden:



LoxForum Thread: https://www.loxforum.com/forum/projektforen/loxberry/plugins/165754-plugin-docker-und-portainer-io



Auf einigen ARM64-basierten Distributionen oder Spezialsystemen (z. B. bestimmte Armbian-/meson64-Systeme)

kann die Installation über klassische Docker-APT-Repositories eingeschränkt sein.



In solchen Fällen wird die Verwendung des offiziellen Docker-Installationsscripts empfohlen:



https://get.docker.com (official Docker install script)


##### 🔧 Technische Hinweise



Die Docker-Systemdiagnose dient ausschließlich der Analyse und Bewertung der lokalen Docker-Installation.

Es werden keine automatischen Änderungen am System durchgeführt.

Empfehlungen und Hinweise basieren auf der erkannten Systemumgebung und Paketkonfiguration.





### 🆕 Change‑Log



##### 2026‑05‑12 – Release 2.2.0

* Neue Docker‑Systemdiagnose integriert
* diagnose.cgi hinzugefügt
* index.cgi erweitert (Diagnose‑Button)
* docker.css erweitert (Diagnose‑Styles)
* Verbesserte Plugin‑Struktur
* Vorbereitung für AutoUpdate‑Release



##### 2026‑05‑12 – Release 2.1.1 (Modernisierte Version)

* LB3‑kompatible Oberfläche
* Entfernung der Template‑Engine
* Entfernung der Wiki‑Hilfe (Crash‑Fix)
* Automatische IP‑Erkennung
* Modernes UI
* Portainer‑Statusanzeige
* Docker‑Containerliste
* Stabilere Installation
* Bereinigung der plugin.cfg \& release.cfg
* ZIP‑Erstellungsskript hinzugefügt



##### 2022‑12‑22 – Release 2.1.0

* Auto‑Update‑Support



##### 2022‑12‑13 – Release 2.0.2

* Wechsel zu portainer/portainer-ce:latest



##### 2019‑12‑31 – Release 2.0.1

* Support für LoxBerry 2.0.0.4
* Portainer 1.23.0



##### 2018‑11‑16 – Release 1.1.0

* Größeres iFrame
* Portainer 1.19.1



##### 2018‑08‑27 – Release 1.0.0

* Initial Release



### ⚠️ Known Issues

Aktuell keine reproduzierbaren Probleme bekannt.



### 📝 Lizenz



Dieses Projekt basiert auf dem ursprünglichen

„loxberry-plugin-docker“ von Michael Miklis.



Originalprojekt:

https://github.com/michaelmiklis/loxberry-plugin-docker



Dieses Projekt enthält modifizierte und erweiterte Bestandteile

des Originalprojekts und wird weiterhin unter der

Apache License 2.0 veröffentlicht.



Eigene Erweiterungen, Modernisierungen und Diagnosefunktionen:

Copyright © 2026 Daniel Hermann



### 🙏 Credits



Originalprojekt:

Michael Miklis



Modernisierung \& Weiterentwicklung:

Daniel Hermann

