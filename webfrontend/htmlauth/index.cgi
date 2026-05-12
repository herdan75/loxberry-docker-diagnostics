#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use JSON;
use LoxBerry::System;
use LoxBerry::Web;

our $htmlhead = "<link rel='stylesheet' href='docker.css'>";

LoxBerry::Web::lbheader("Übersicht Docker Container", undef, undef);

# =========================================================
# REFRESH HANDLING (CACHE RESET)
# =========================================================
my $query = $ENV{QUERY_STRING} || "";

if ($query =~ /refresh=1/) {
    unlink "/tmp/docker_v6_cache.json";
}

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
# DIAGNOSE CARD + BUTTONS
# =========================================================
print "<div class='card'>";

print qq{
<h2>Docker Systemdiagnose</h2>

<p>Analysiert Docker Version, Ports und Container Status.</p>

<a href="diagnose.cgi" class="btn" style="background:#ffc107;color:#000;">
    Diagnose starten
</a>

<a href="?refresh=1" class="btn" style="background:#17a2b8;margin-left:10px;">
    Ports neu scannen
</a>
};

print "</div>";

# =========================================================
# CACHE
# =========================================================
my $cache_file = "/tmp/docker_v6_cache.json";
my $cache_time = 10;

my $raw;

if (-e $cache_file && (time - (stat($cache_file))[9] < $cache_time)) {

    open(my $fh, "<", $cache_file);
    local $/;
    $raw = <$fh>;
    close($fh);

} else {

    $raw = `docker ps --format '{{json .}}' 2>/dev/null`;

    open(my $fh, ">", $cache_file);
    print $fh $raw;
    close($fh);
}

# =========================================================
# PARSE JSON
# =========================================================
my @containers;

foreach my $line (split(/\n/, $raw)) {

    next unless $line;

    my $c;
    eval { $c = decode_json($line); };
    next unless $c;

    push @containers, $c;
}

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
# STATUS
# =========================================================
sub status_chip {
    my ($status) = @_;

    return ($status =~ /Up/)
        ? "<span style='background:#28a745;color:white;padding:4px 10px;border-radius:6px;'>Running</span>"
        : "<span style='background:#dc3545;color:white;padding:4px 10px;border-radius:6px;'>Stopped</span>";
}

# =========================================================
# LOOP
# =========================================================
foreach my $c (@containers) {

    my $name   = escapeHTML($c->{Names}  || "");
    my $status = escapeHTML($c->{Status} || "");

    my $inspect_raw = `docker inspect $name 2>/dev/null`;
    my $inspect;

    eval { $inspect = decode_json($inspect_raw); };

    my $url_html = "";

    # =====================================================
    # PORT DETECTION (REAL DOCKER API)
    # =====================================================
    if ($inspect && $inspect->[0]{NetworkSettings}{Ports}) {

        my $ports = $inspect->[0]{NetworkSettings}{Ports};

        foreach my $container_port (keys %$ports) {

            next unless $ports->{$container_port};

            foreach my $bind (@{$ports->{$container_port}}) {

                my $host_ip   = $bind->{HostIp}   || $host;
                my $host_port = $bind->{HostPort};

                my $proto = ($container_port =~ /443/) ? "https" : "http";

                my $url = "$proto://$host_ip:$host_port";

                $url_html .= qq{
<a href="$url" target="_blank">$url</a><br>
};
            }
        }
    }

    # =====================================================
    # FALLBACK
    # =====================================================
    if (!$url_html) {
        $url_html = "<span style='color:#888;font-style:italic;'>n/a</span>";
    }

    # =====================================================
    # OUTPUT ROW
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
