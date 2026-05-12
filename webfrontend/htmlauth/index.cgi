#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use JSON;
use LoxBerry::System;
use LoxBerry::Web;

# =========================================================
# STORAGE
# =========================================================
my $store_file = "/opt/loxberry/data/docker_services.json";

# =========================================================
# SAVE ACTION
# =========================================================
my $query = $ENV{QUERY_STRING} || "";

if ($query =~ /save=1/) {

    my $cgi = CGI->new;

    my $container = $cgi->param('container') || "";
    my $url       = $cgi->param('url') || "";

    my $data = {};

    if (-e $store_file) {
        open(my $fh, "<", $store_file);
        local $/;
        my $json = <$fh>;
        close($fh);

        eval { $data = decode_json($json); };
    }

    # speichern
    $data->{$container} = $url;

    open(my $fh, ">", $store_file);
    print $fh encode_json($data);
    close($fh);
}

# =========================================================
# LOAD DATA
# =========================================================
my $saved = {};

if (-e $store_file) {
    open(my $fh, "<", $store_file);
    local $/;
    my $json = <$fh>;
    close($fh);

    eval { $saved = decode_json($json); };
}

# =========================================================
# HOST
# =========================================================
my $host = LoxBerry::System::get_localip();
$host ||= "localhost";

# =========================================================
# CONTAINERS
# =========================================================
my @containers = `docker ps --format "{{.Names}}|{{.Status}}" 2>/dev/null`;
chomp @containers;

# =========================================================
# HEADER
# =========================================================
our $htmlhead = "<link rel='stylesheet' href='docker.css'>";
LoxBerry::Web::lbheader("Übersicht Docker Container", undef, undef);

# =========================================================
# PORTAINER
# =========================================================
my $portainer_url = "http://$host:9000";

print "<div class='card'>";
print "<h1>Docker / Portainer</h1>";

print qq{
<p>Verwaltung deiner Docker-Container über Portainer.</p>

<a class="btn" href="$portainer_url" target="_blank">
    Portainer öffnen
</a>

<p style="margin-top:10px;color:#666;">
Portainer: $portainer_url
</p>
};

print "</div>";

# =========================================================
# DIAGNOSE
# =========================================================
print "<div class='card'>";

print qq{
<h2>Docker Systemdiagnose</h2>

<p>Analyse bleibt verfügbar (Version / Status / System).</p>

<a href="diagnose.cgi" class="btn" style="background:#ffc107;color:#000;">
    Diagnose starten
</a>
};

print "</div>";

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
<th>Service URL</th>
<th>Aktion</th>
</tr>
};

# =========================================================
# STATUS CHIP
# =========================================================
sub status_chip {
    my ($status) = @_;

    return ($status =~ /Up/)
        ? "<span style='background:#28a745;color:white;padding:4px 10px;border-radius:6px;'>Running</span>"
        : "<span style='background:#dc3545;color:white;padding:4px 10px;border-radius:6px;'>Stopped</span>";
}

# =========================================================
# ROWS
# =========================================================
foreach my $line (@containers) {

    my ($name, $status) = split(/\|/, $line);

    my $safe_name = escapeHTML($name);
    my $safe_status = escapeHTML($status);

    my $saved_url = $saved->{$name} || "";

    # Anzeige-Link
    my $link_html = $saved_url
        ? qq{<a href="$saved_url" target="_blank">$saved_url</a>}
        : "<span style='color:#999;'>n/a</span>";

    print "<tr>";

    # NAME
    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>$safe_name</td>";

    # STATUS
    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>";
    print status_chip($status);
    print "</td>";

    # URL
    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>$link_html</td>";

    # INPUT + SAVE
    print "<td style='padding:10px;border-bottom:1px solid #ddd;'>";

    print qq{
        <form method="GET" action="">
            <input type="hidden" name="save" value="1">
            <input type="hidden" name="container" value="$safe_name">

            <input type="text"
                   name="url"
                   value=""
                   placeholder="http(s)://IP:PORT oder https://domain.tld"
                   style="
                       width: 320px;
                       padding: 10px 12px;
                       font-size: 14px;
                       line-height: 20px;
                       letter-spacing: 0.2px;
                       box-sizing: border-box;
                       border-radius: 6px;
                   ">

            <button type="submit" class="btn" style="padding:6px 10px;">
                Speichern
            </button>
        </form>
    };

    print "</td>";

    print "</tr>";
}

print "</table>";
print "</div>";

# =========================================================
# FOOTER
# =========================================================
LoxBerry::Web::lbfooter();
