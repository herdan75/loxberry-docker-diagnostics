# Docker & Portainer for LoxBerry

Modernisierte und erweiterte Docker- & Portainer-Integration für LoxBerry 3.x.

Dieses Projekt basiert auf dem ursprünglichen Docker-Plugin von Michael Miklis und wurde vollständig modernisiert, stabilisiert und erweitert.

Die neue Version integriert Docker sauber in die LoxBerry-Weboberfläche und bietet zusätzliche Diagnose- und Analysefunktionen für Docker-Systeme auf x86_64- und ARM-basierten Plattformen.

---

## 📥 Downloads

### Stable Release
Finale getestete Version:

https://github.com/herdan75/loxberry-docker-diagnostics/releases/latest

### Beta / Pre-Releases
Vorabversionen und Testversionen:

https://github.com/herdan75/loxberry-docker-diagnostics/releases

---

## 🚀 Release-Kanäle

### Stable
Getestete und freigegebene Versionen für produktive Systeme.

### Beta / Pre-Release
Vorabversionen mit neuen Funktionen und Änderungen.

Diese Versionen dienen Testzwecken und können Fehler enthalten.

---

## 📸 Screenshots

### 🔧 Portainer starten

Über das Docker-Plugin kann Portainer direkt gestartet werden.

Der Status zeigt an, ob der Portainer-Container läuft.

<img src="https://github.com/user-attachments/assets/021ff549-751f-4049-b488-43409bcc561a"
     alt="Docker Übersicht"
     style="max-width: 350px; width: 40%; height: auto;" />

Anmeldeseite öffnet sich:

<img src="https://github.com/user-attachments/assets/4747a8ba-2799-4b46-ab41-4f84b055f431"
     alt="Portainer Login"
     style="max-width: 350px; width: 20%; height: auto;" />

---

### 🔧 Docker-Systemdiagnose

Die integrierte Diagnose-Funktion analysiert:

* Docker-Version
* Installationsart (docker.io / docker-ce / Script)
* Architektur & Kernel
* Paketquellen
* Konflikte und Mischinstallationen
* Update-Status
* Handlungsempfehlungen

Viele LoxBerry-Systeme laufen auf ARM-basierten Plattformen wie:

* aarch64
* arm64
* meson64

Diese Systeme verwenden oft unterschiedliche Kernel, Paketquellen oder Hersteller-Images, die nicht vollständig mit den offiziellen Docker-Paketen kompatibel sind.

Dadurch entstehen typische Probleme:

* Mischinstallationen (docker.io + docker-ce gleichzeitig)
* veraltete Debian-Pakete (`docker.io`)
* fehlende oder inkompatible Abhängigkeiten (`containerd.io`)
* nicht unterstützte Kernel-Versionen auf ARM-Boards
* unklare Installationsquellen (APT, Script, Hersteller-Image)

Diese Fehler bleiben für Benutzer oft unsichtbar — Docker „funktioniert irgendwie“, aber instabil.

<img src="https://github.com/user-attachments/assets/953ae1ea-b706-474a-a122-4440a44385f7"
     alt="Docker Diagnose"
     style="max-width: 350px; width: 40%; height: auto;" />

Beispiel eines Analyse-Resultats:

<img src="https://github.com/user-attachments/assets/5b8b5157-5e21-4dbd-a70d-903f3b2b5fc9"
     alt="Docker Analyse"
     style="max-width: 600px; width: 40%; height: auto;" />

👉 Das Analysetool erkennt versteckte Probleme, bewertet die Installation und gibt klare Handlungsempfehlungen.

---

### 🔧 Übersicht der Docker-Container

Übersicht der laufenden Container und Status:

<img src="https://github.com/user-attachments/assets/d2c59a72-ed39-48ad-a7ba-edbff54d335f"
     alt="Docker UI"
     style="max-width: 350px; width: 40%; height: auto;" />

👉 Docker-Containern können individuelle URLs zugeordnet werden.

Nach dem Speichern kann der jeweilige Container direkt über die URL geöffnet werden.

---

## ✨ Features

### 🔍 Diagnose & Systemanalyse

* Docker-Systemdiagnose integriert
* Erkennung der installierten Docker-Version
* Analyse der Paketquellen (Debian docker.io vs Docker CE)
* Architektur- und Kernel-Analyse (x86_64 / ARM64)
* Erkennung problematischer Paketkonstellationen
* Analyse der Docker-Installationsart
* Erkennung potenzieller Mischinstallationen
* Erkennung von Update-Konflikten
* Mixed-Package-Detection (containerd / containerd.io)
* Bewertung des Systemzustands
* Handlungsempfehlungen zur Fehlerbehebung
* Empfehlung zur sauberen Neuinstallation

---

### 🎨 Modernisierung & UI-Verbesserungen

* Vollständig kompatibel mit LoxBerry 3.x
* Entfernung der alten Template-Engine
* Entfernung der Wiki-Hilfe
* Modernes CSS-basiertes UI
* Stabilere Installations- und Startlogik
* Portainer-Statusanzeige
* Docker-Containerliste
* Verbesserte Plugin-Struktur
* GitHub Actions für automatische ZIP-Erstellung
* Stable- und PreRelease-System integriert

---

### 🐳 Docker & Portainer

* Automatische Installation der Docker-Engine
* Automatische Installation & Start von Portainer CE
* Integration in die LoxBerry-Weboberfläche
* Verwaltung von Containern über Portainer

---

## 📦 Installation

### Installation über den LoxBerry Plugin Manager (empfohlen)

1. LoxBerry Webinterface öffnen
2. System → Pluginverwaltung
3. Plugin installieren
4. Plugin öffnen
5. Portainer starten

---

### Manuelle Installation

#### Stable Release

https://github.com/herdan75/loxberry-docker-diagnostics/releases/latest

#### Beta / Pre-Releases

https://github.com/herdan75/loxberry-docker-diagnostics/releases

---

## 🌐 Portainer Zugriff

Portainer ist standardmäßig erreichbar unter:

http://your-loxberry.local:9000

---

## 🧩 Voraussetzungen

* LoxBerry 3.x
* Internetzugang für Docker-Installation

---

## 🛠 Troubleshooting & Hinweise

Dieses Plugin installiert Docker und Portainer, bietet jedoch keinen Support für Docker-Container selbst.

Für Feedback oder Fehlerberichte:

https://www.loxforum.com/forum/projektforen/loxberry/plugins/165754-plugin-docker-und-portainer-io

---

### Hinweise zu ARM64-Systemen

Auf einigen ARM64-basierten Distributionen oder Spezialsystemen (z. B. Armbian / meson64) kann die Installation über klassische Docker-APT-Repositories eingeschränkt sein.

Empfohlen:

https://get.docker.com

---

## 🔧 Technische Hinweise

Die Docker-Systemdiagnose dient ausschließlich der Analyse und Bewertung der lokalen Docker-Installation.

Es werden keine automatischen Änderungen am System durchgeführt.

---

## 🆕 Changelog

Die vollständige Versionshistorie befindet sich in:

CHANGELOG.md

Zusätzlich sind alle Releases inklusive Release Notes hier verfügbar:

https://github.com/herdan75/loxberry-docker-diagnostics/releases

---

## ⚠️ Known Issues

Aktuell keine reproduzierbaren Probleme bekannt.

---

## 📝 Lizenz

Dieses Projekt basiert auf dem ursprünglichen Projekt:

„loxberry-plugin-docker“ von Michael Miklis

https://github.com/michaelmiklis/loxberry-plugin-docker

Veröffentlicht unter der Apache License 2.0.

Eigene Erweiterungen, Modernisierungen und Diagnosefunktionen:

© Daniel Hermann

---

## 🙏 Credits

* Originalprojekt: Michael Miklis
* Modernisierung & Weiterentwicklung: Daniel Hermann



---

## Sicherheit & Betrieb

Portainer wird mit Zugriff auf /var/run/docker.sock gestartet. Wer Zugriff auf Portainer erhält, kann damit faktisch Docker und damit große Teile des Hosts administrieren. Portainer sollte deshalb nur im vertrauenswürdigen lokalen Netz erreichbar sein und mit einem starken Passwort geschützt werden.

Das Plugin verwendet bei einer fehlenden Docker-Installation das offizielle Docker-Installationsscript von https://get.docker.com. Das ist bequem, aber bewusst ein Root-Installationspfad aus dem Internet. Für produktive Systeme empfiehlt sich vorher ein Backup und eine Prüfung der bestehenden Docker-/APT-Paketquellen.

Die Diagnose prüft zusätzlich Docker-Daemon, Portainer-Container, Portfreigaben, Docker-Compose, Docker-relevante APT-Updates und Speicherplatz. So lassen sich typische Fehler vor einem Update oder Release schneller erkennen.
