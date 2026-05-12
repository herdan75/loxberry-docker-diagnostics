#!/bin/bash

# postinstall.sh – ausgeführt nach Installation/Update
# Läuft als root

COMMAND=$0
PTEMPDIR=$1
PSHNAME=$2
PDIR=$3
PVERSION=$4
PTEMPPATH=$6

PCGI=$LBPCGI/$PDIR
PHTML=$LBPHTML/$PDIR
PTEMPL=$LBPTEMPL/$PDIR
PDATA=$LBPDATA/$PDIR
PLOG=$LBPLOG/$PDIR
PCONFIG=$LBPCONFIG/$PDIR
PSBIN=$LBPSBIN/$PDIR
PBIN=$LBPBIN/$PDIR

echo "<INFO> Plugin installiert: $PDIR Version $PVERSION"
echo "<INFO> Pluginpfade:"
echo "<INFO> CGI: $PCGI"
echo "<INFO> HTML: $PHTML"
echo "<INFO> Template: $PTEMPL"
echo "<INFO> Data: $PDATA"
echo "<INFO> Log: $PLOG"
echo "<INFO> Config: $PCONFIG"

# Docker installieren, falls nicht vorhanden
if ! command -v docker >/dev/null 2>&1; then
    echo "<INFO> Docker nicht gefunden – Installation wird gestartet"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker loxberry
else
    echo "<OK> Docker ist bereits installiert"
fi

# Portainer prüfen
container=$(docker ps --filter ancestor=portainer/portainer-ce:latest --filter name=portainer -q)

if [ -z "$container" ]; then
    echo "<INFO> Portainer läuft nicht – wird gestartet"

    # alten Container entfernen
    if docker ps -a --format '{{.Names}}' | grep -q '^portainer$'; then
        echo "<INFO> Entferne alten Portainer-Container"
        docker rm --force portainer
    fi

    echo "<INFO> Lade Portainer-Image"
    docker pull portainer/portainer-ce:latest

    echo "<INFO> Starte Portainer"
    docker run \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --volume=/opt/portainer:/data \
        -p=9000:9000 \
        --name="portainer" \
        --restart="unless-stopped" \
        --detach=true \
        portainer/portainer-ce:latest
else
    echo "<OK> Portainer läuft bereits"
fi

exit 0
