#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use LoxBerry::System;
use LoxBerry::Web;

our $htmlhead = "<link rel='stylesheet' href='docker.css'>";

LoxBerry::Web::lbheader("Übersicht Docker Container", undef, undef);

# =========================================================
# HOST IP (robust)
# =========================================================
my $host = LoxBerry::System::get_localip();
$host ||= `hostname -I 2>/dev/null | awk '{print \$1}'`;
chomp($host);
$host ||= "localhost";

# =========================================================
# REFRESH HANDLING (optional lightweight cache reset)
# =========================================================
my $refresh = $ENV{QUERY_STRING} && $ENV{QUERY_STRING} =~ /refresh=1/ ? 1 : 0;

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
# HEADER CARD
# =========================================================
print "<div class='card'>";
print "<h1>Docker / Portainer</h1>";

print qq{
<p>Appliance Dashboard für Docker Container Verwaltung</p>

<a class="btn" href="$portainer_url" target="_blank">
    Portainer öffnen
</a>

<div style="margin-top:15px;">
    <span style="padding:8px 15px;background:$status_color;color:white;border-radius:6px;">
        Portainer Status: $status_text
    </span>
</div>

<p style="margin-top:10px;color:#666;">
    $portainer_url
</p>
};

print "</div>";

# =========================================================
# ACTIONS (ANALYSE + REFRESH)
# =========================================================
print "<div class='card'>";

print qq{
<h2>System Aktionen</h2>

<a href="diagnose.cgi" class="btn" style="background:#ffc107;color:#000;">
    Analyse starten
</a>

<a href="index.cgi?refresh=1" class="btn" style="background:#0078d4;margin-left:10px;">
    Ports neu scannen
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
<th>Host / Port</th>
</tr>
};

# =========================================================
# STATUS CHIP
# =========================================================
sub status_chip {
    my ($status) = @_;

    return $status =~ /Up/
        ? "<span style='background:#28a745;color:white;padding:4px 10px;border-radius:6px;'>Running</span>"
        : "<span style='background:#dc3545;color:white;padding:4px 10px;border-radius:6px;'>Stopped</span>";
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

    # =====================================================
    # MULTI PORT DETECTION (robust)
    # =====================================================
    while ($ports =~ /0\.0\.0\.0:(\d+)->/g) {

        my $port = $1;
        my $proto = ($port == 443) ? "https" : "http";
        my $url   = "$proto://$host:$port";

        $url_html .= qq{<a href="$url" target="_blank">$url</a><br>};
    }

    # fallback generic pattern
    if (!$url_html && $ports =~ /:(\d+)->/) {

        my $port = $1;
        my $proto = ($port == 443) ? "https" : "http";
        my $url   = "$proto://$host:$port";

        $url_html = qq{<a href="$url" target="_blank">$url</a>};
    }

    # =====================================================
    # CLEAN FALLBACK
    # =====================================================
    if (!$url_html) {
        $url_html = "<span style='color:#999;font-style:italic;'>n/a</span>";
    }

    # =====================================================
    # OUTPUT
    # =====================================================
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
