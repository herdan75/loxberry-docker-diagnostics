#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use LoxBerry::System;
use LoxBerry::Web;

our $htmlhead = "<link rel='stylesheet' href='docker.css'>";

LoxBerry::Web::lbheader("Übersicht Docker Container", undef, undef);

# =========================================================
# HOST / IP
# =========================================================
my $host = LoxBerry::System::get_localip();
$host ||= `hostname -I 2>/dev/null | awk '{print \$1}'`;
chomp($host);
$host ||= "localhost";

# =========================================================
# PORTAINER STATUS
# =========================================================
my $portainer_running = `docker inspect -f '{{.State.Running}}' portainer 2>/dev/null`;
chomp($portainer_running);

my $is_running = ($portainer_running eq "true") ? 1 : 0;

my $status_text  = $is_running ? "Läuft" : "Gestoppt";
my $status_color = $is_running ? "#28a745" : "#dc3545";

my $portainer_url = "http://$host:9000";

# =========================================================
# PORTAINER CARD
# =========================================================
print "<div class='card'>";
print "<h1>Docker / Portainer</h1>";

print qq{
<p>Verwaltung deiner Docker-Container über Portainer.</p>

<a class="btn" href="$portainer_url" target="_blank">
    Portainer öffnen
</a>

<div style="margin-top:15px;">
    <span style="padding:8px 15px;background:$status_color;color:white;border-radius:6px;">
        Portainer Status: $status_text
    </span>
</div>

<p style="margin-top:15px;color:#666;">
    Portainer: $portainer_url
</p>
};

print "</div>";

# =========================================================
# DIAGNOSE / ANALYSE
# =========================================================
print "<div class='card'>";

print qq{
<h2>Docker Systemdiagnose</h2>

<p>Analysiert Docker-Version, Paketquellen und Konfiguration.</p>

<a href="diagnose.cgi" class="btn" style="background:#ffc107;color:#000;">
    Diagnose starten
</a>

<a href="/admin/plugins/docker/index.cgi"
   class="btn"
   style="background:#6c757d;margin-left:10px;">
    Docker Plugin
</a>
};

print "</div>";

# =========================================================
# CONTAINER LIST
# =========================================================
my @containers = `docker ps --format "{{.Names}}|{{.Status}}|{{.Ports}}" 2>/dev/null`;
chomp @containers;

# =========================================================
# TABLE
# =========================================================
print "<div class='card'>";
print "<h2>Übersicht Docker Container</h2>";

print qq{
<table class="docker-table">
<tr style="background:#0078d4;color:white;">
<th>Name</th>
<th>Status</th>
<th>Ports / URL</th>
</tr>
};

# =========================================================
# STATUS CHIP
# =========================================================
sub status_chip {
    my ($status) = @_;

    if ($status =~ /Up/) {
        return "<span style='background:#28a745;color:white;padding:4px 10px;border-radius:6px;'>Running</span>";
    }

    return "<span style='background:#dc3545;color:white;padding:4px 10px;border-radius:6px;'>Stopped</span>";
}

# =========================================================
# ROWS
# =========================================================
foreach my $line (@containers) {

    my ($name, $status, $ports) = split(/\|/, $line);

    $name   = escapeHTML($name   || "");
    $status = escapeHTML($status || "");
    $ports  = $ports || "";

    my $url_html = "";

    # PORT DETECTION
    if ($ports =~ /0\.0\.0\.0:(\d+)->/) {

        my $port = $1;
        my $proto = ($port == 443) ? "https" : "http";
        my $url   = "$proto://$host:$port";

        $url_html = qq{<a href="$url" target="_blank">$url</a>};
    }
    elsif ($ports =~ /:(\d+)->/) {

        my $port = $1;
        my $proto = ($port == 443) ? "https" : "http";
        my $url   = "$proto://$host:$port";

        $url_html = qq{<a href="$url" target="_blank">$url</a>};
    }

    if (!$url_html) {
        $url_html = "<span style='color:#888;font-style:italic;'>n/a</span>";
    }

    print "<tr>";

    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>$name</td>";

    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>";
    print status_chip($status);
    print "</td>";

    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>$url_html</td>";

    print "</tr>";
}

print "</table>";
print "</div>";

# =========================================================
# FOOTER
# =========================================================
LoxBerry::Web::lbfooter();
