#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use LoxBerry::System;
use LoxBerry::Web;

# ---------------------------------------------------------
# Plugin-Version
# ---------------------------------------------------------
my $version = LoxBerry::System::pluginversion();

# ---------------------------------------------------------
# Saubere IP-Ermittlung (robust für ARM / Multi-NIC)
# ---------------------------------------------------------
my $ip = LoxBerry::System::get_localip();
$ip ||= `hostname -I 2>/dev/null | awk '{print $1}'`;
chomp($ip);
$ip ||= "localhost";

# ---------------------------------------------------------
# HTML Header
# ---------------------------------------------------------
our $htmlhead = "<link rel='stylesheet' href='docker.css'>";
LoxBerry::Web::lbheader("Docker", "https://www.docker.com", undef);

# =========================================================
# PORTAINER STATUS (robust via docker inspect)
# =========================================================
my $portainer_running = `docker inspect -f '{{.State.Running}}' portainer 2>/dev/null`;
chomp($portainer_running);

my $is_running = ($portainer_running && $portainer_running eq "true") ? 1 : 0;

my $status_text  = $is_running ? "Läuft" : "Gestoppt";
my $status_color = $is_running ? "#28a745" : "#dc3545";

# =========================================================
# DOCKER CONTAINER LIST (mit Timeout Schutz)
# =========================================================
my @containers;

eval {
    local $SIG{ALRM} = sub { die "timeout\n" };
    alarm(2);

    @containers = `docker ps --format "{{.Names}}|{{.Status}}" 2>/dev/null`;

    alarm(0);
};
alarm(0);

# =========================================================
# Portainer URL sicher bauen
# =========================================================
my $portainer_url = ($ip && $ip ne "localhost")
    ? "http://$ip:9000"
    : "#";

# =========================================================
# HTML OUTPUT
# =========================================================
print <<HTML;

<div class="card">
    <h1>Docker / Portainer</h1>

    <p>Verwaltung deiner Docker-Container über Portainer.</p>

    <a class="btn" href="$portainer_url" target="_blank">
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
        Portainer-Adresse: $portainer_url
    </p>
</div>

<!-- ---------------------------------------------------------
     Diagnose
---------------------------------------------------------- -->

<div class="card">

    <h2>Docker Systemdiagnose</h2>

    <p>
        Analysiert Docker-Version, Paketquellen, Update-Status und mögliche Konflikte.
    </p>

    <form action="diagnose.cgi" method="get" style="margin-top:10px;">
        <button type="submit" class="btn" style="background:#ffc107; color:#000;">
            Docker Systemdiagnose anzeigen
        </button>
    </form>

</div>

<!-- ---------------------------------------------------------
     Container Tabelle
---------------------------------------------------------- -->

<div class="card">

    <h2>Docker Container</h2>

    <table style="margin:0 auto; border-collapse:collapse; width:80%;">

        <tr style="background:#0078d4; color:white;">
            <th style="padding:10px;">Name</th>
            <th style="padding:10px;">Status</th>
        </tr>

HTML

# =========================================================
# TABLE OUTPUT SAFE
# =========================================================
foreach my $line (@containers) {

    chomp($line);

    my ($name, $status) = split(/\|/, $line);

    $name   = escapeHTML($name // "");
    $status = escapeHTML($status // "");

    print <<ROW;
        <tr>
            <td style="padding:10px; border-bottom:1px solid #ccc;">
                $name
            </td>
            <td style="padding:10px; border-bottom:1px solid #ccc;">
                $status
            </td>
        </tr>
ROW
}

print <<HTML;

    </table>

</div>

HTML

# Footer
LoxBerry::Web::lbfooter();
