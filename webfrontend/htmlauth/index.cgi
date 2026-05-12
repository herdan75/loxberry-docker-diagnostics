#!/usr/bin/env perl

use strict;
use warnings;

use CGI;
use LoxBerry::System;
use LoxBerry::Web;

# Plugin-Version auslesen
my $version = LoxBerry::System::pluginversion();

# LoxBerry-IP automatisch ermitteln
my $ip = LoxBerry::System::lbhostname();

# HTML-Header laden
our $htmlhead = "<link rel='stylesheet' href='docker.css'>";
LoxBerry::Web::lbheader("Docker", "https://www.docker.com", undef);

# ---------------------------------------------------------
# Portainer-Status prüfen
# ---------------------------------------------------------
my $portainer_running = `docker ps --filter "name=portainer" --format "{{.Status}}"`;
chomp($portainer_running);

my $status_text  = $portainer_running ? "Läuft" : "Gestoppt";
my $status_color = $portainer_running ? "#28a745" : "#dc3545";

# ---------------------------------------------------------
# Docker-Containerliste abrufen
# ---------------------------------------------------------
my @containers = `docker ps --format "{{.Names}}|{{.Status}}"`;

# ---------------------------------------------------------
# HTML-Ausgabe
# ---------------------------------------------------------
print <<END_HTML;

<div class="card">
    <h1>Docker / Portainer</h1>

    <p>
        Verwaltung deiner Docker-Container über Portainer.
    </p>

    <a class="btn" href="http://$ip:9000" target="_blank">
        Portainer öffnen
    </a>

    <div style="margin-top:20px;">
        <span style="
            padding:8px 15px;
            background:$status_color;
            color:white;
            border-radius:6px;
        ">
            Portainer Status: $status_text
        </span>
    </div>

    <p style="margin-top:20px; color:#666;">
        Plugin-Version: $version<br>
        Portainer-Adresse: http://$ip:9000
    </p>
</div>

<!-- ---------------------------------------------------------
     Diagnose-Button
---------------------------------------------------------- -->

<div class="card">

    <h2>Docker Systemdiagnose</h2>

    <p>
        Analysiert Docker-Version,
        Paketquellen,
        Update-Status
        und mögliche Konflikte.
    </p>

    <form action="diagnose.cgi" method="get" style="margin-top:10px;">

        <button
            type="submit"
            class="btn"
            style="background:#ffc107; color:#000;"
        >
            Docker Systemdiagnose anzeigen
        </button>

    </form>

</div>

<!-- ---------------------------------------------------------
     Docker Container Tabelle
---------------------------------------------------------- -->

<div class="card">

    <h2>Docker Container</h2>

    <table style="
        margin:0 auto;
        border-collapse:collapse;
        width:80%;
    ">

        <tr style="background:#0078d4; color:white;">
            <th style="padding:10px;">Name</th>
            <th style="padding:10px;">Status</th>
        </tr>

END_HTML

# Tabellenzeilen erzeugen
foreach my $line (@containers) {

    chomp($line);

    my ($name, $status) = split(/\|/, $line);

    print <<END_ROW;

        <tr>
            <td style="
                padding:10px;
                border-bottom:1px solid #ccc;
            ">
                $name
            </td>

            <td style="
                padding:10px;
                border-bottom:1px solid #ccc;
            ">
                $status
            </td>
        </tr>

END_ROW

}

# Tabelle schließen
print <<END_HTML;

    </table>

</div>

END_HTML

# Footer
LoxBerry::Web::lbfooter();