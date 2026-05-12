#!/bin/bash

# =========================================================
# LoxBerry Docker + Portainer Plugin (FINAL SAFE VERSION)
# =========================================================

set -e

COMMAND=$0
PTEMPDIR=$1
PSHNAME=$2
PDIR=$3
PVERSION=$4
PTEMPPATH=$6

echo "<INFO> Plugin installiert: $PDIR Version $PVERSION"

# =========================================================
# LoxBerry Pfade (nur Info)
# =========================================================
echo "<INFO> Pluginpfade:"
echo "<INFO> CGI: $LBPCGI/$PDIR"
echo "<INFO> HTML: $LBPHTML/$PDIR"
echo "<INFO> Template: $LBPTEMPL/$PDIR"
echo "<INFO> Data: $LBPDATA/$PDIR"
echo "<INFO> Log: $LBPLOG/$PDIR"
echo "<INFO> Config: $LBPCONFIG/$PDIR"

# =========================================================
# DOCKER INSTALL (NUR FALLS FEHLT)
# =========================================================
if ! command -v docker >/dev/null 2>&1; then

    echo "<INFO> Docker nicht gefunden → Installation startet"

    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sh /tmp/get-docker.sh
    rm -f /tmp/get-docker.sh

    if id "loxberry" >/dev/null 2>&1; then
        usermod -aG docker loxberry || true
    fi

else
    echo "<OK> Docker bereits installiert"
fi

systemctl enable docker >/dev/null 2>&1 || true
systemctl start docker >/dev/null 2>&1 || true

# =========================================================
# PORTAINER STATE MACHINE (SAFE LOGIC)
# =========================================================

PORTAINER_RUNNING=$(docker ps --format '{{.Names}}' | grep -qw portainer && echo "yes" || echo "no")
PORTAINER_EXISTS=$(docker ps -a --format '{{.Names}}' | grep -qw portainer && echo "yes" || echo "no")

# ---------------------------------------------------------
# CASE 1: läuft korrekt
# ---------------------------------------------------------
if [ "$PORTAINER_RUNNING" = "yes" ]; then

    echo "<OK> Portainer läuft korrekt"

# ---------------------------------------------------------
# CASE 2: existiert aber gestoppt → nur starten
# ---------------------------------------------------------
elif [ "$PORTAINER_EXISTS" = "yes" ]; then

    echo "<INFO> Portainer existiert → Start"

    docker start portainer >/dev/null 2>&1 || {

        echo "<WARN> Start fehlgeschlagen → kontrollierter Restart"

        docker rm -f portainer >/dev/null 2>&1 || true

        docker pull portainer/portainer-ce:latest

        docker run -d \
            --name portainer \
            --restart unless-stopped \
            -p 9000:9000 \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v /opt/portainer:/data \
            portainer/portainer-ce:latest
    }

# ---------------------------------------------------------
# CASE 3: nicht vorhanden → neu installieren
# ---------------------------------------------------------
else

    echo "<INFO> Portainer nicht vorhanden → Installation"

    docker pull portainer/portainer-ce:latest

    docker run -d \
        --name portainer \
        --restart unless-stopped \
        -p 9000:9000 \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /opt/portainer:/data \
        portainer/portainer-ce:latest

fi

# =========================================================
# SAFE CLEANUP (KEINE DATENVERLUSTE)
# =========================================================
echo "<INFO> Docker Cleanup (dangling images only)"
docker image prune -f >/dev/null 2>&1 || true

echo "<OK> Postinstall abgeschlossen sauber"
exit 0
