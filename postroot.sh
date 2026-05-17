#!/bin/bash

# =========================================================
# LoxBerry Docker + Portainer Plugin
# =========================================================

set -e

COMMAND=$0
PTEMPDIR=$1
PSHNAME=$2
PDIR=$3
PVERSION=$4
PTEMPPATH=$6
PORTAINER_IMAGE=${PORTAINER_IMAGE:-portainer/portainer-ce:lts}
PORTAINER_DATA=${PORTAINER_DATA:-/opt/portainer}

echo "<INFO> Plugin installiert: $PDIR Version $PVERSION"
echo "<INFO> Portainer Image: $PORTAINER_IMAGE"

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

    echo "<INFO> Docker nicht gefunden -> Installation startet"

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

if ! docker info >/dev/null 2>&1; then
    echo "<ERROR> Docker ist installiert, aber der Docker-Daemon ist nicht erreichbar"
    exit 1
fi

# =========================================================
# PORTAINER STATE MACHINE
# =========================================================
container_running() {
    docker ps --format '{{.Names}}' | grep -Fxq "$1"
}

container_exists() {
    docker ps -a --format '{{.Names}}' | grep -Fxq "$1"
}

run_portainer() {
    docker pull "$PORTAINER_IMAGE"

    docker run -d \
        --name portainer \
        --restart unless-stopped \
        -p 9000:9000 \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v "$PORTAINER_DATA":/data \
        "$PORTAINER_IMAGE"
}

# ---------------------------------------------------------
# CASE 1: laeuft korrekt
# ---------------------------------------------------------
if container_running portainer; then

    echo "<OK> Portainer laeuft korrekt"

# ---------------------------------------------------------
# CASE 2: existiert aber gestoppt -> nur starten
# ---------------------------------------------------------
elif container_exists portainer; then

    echo "<INFO> Portainer existiert -> Start"

    docker start portainer >/dev/null 2>&1 || {

        echo "<WARN> Start fehlgeschlagen -> kontrollierter Restart"

        docker rm -f portainer >/dev/null 2>&1 || true
        run_portainer
    }

# ---------------------------------------------------------
# CASE 3: nicht vorhanden -> neu installieren
# ---------------------------------------------------------
else

    echo "<INFO> Portainer nicht vorhanden -> Installation"
    run_portainer

fi

# =========================================================
# SAFE CLEANUP (KEINE DATENVERLUSTE)
# =========================================================
echo "<INFO> Docker Cleanup (dangling images only)"
docker image prune -f >/dev/null 2>&1 || true

echo "<OK> Postinstall abgeschlossen sauber"
exit 0
