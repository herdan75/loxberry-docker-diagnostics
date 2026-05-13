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

LoxBerry::Web::lbheader(
    "Übersicht Docker Container",
    undef,
    undef
);

# =========================================================
# PORTAINER
# =========================================================
my $portainer_url = "http://$host:9000";

print "<div class='card'>";

print "<h1>Docker / Portainer</h1>";

print qq{
<p>Verwaltung deiner Docker-Container über Portainer.</p>

<a class="btn"
   href="$portainer_url"
   target="_blank">
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

<p>
Systemdiagnose zur Validierung der Docker-Installation
(Version, Pakete, Konflikte und Systemzustand).
</p>

<a href="diagnose.cgi"
   class="btn btn-warning">
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
<tr>
    <th>Name</th>
    <th>Status</th>
    <th>Service URL</th>
    <th>Service URL zuordnen</th>
</tr>
};

# =========================================================
# STATUS CHIP
# =========================================================
sub status_chip {

    my ($status) = @_;

    return ($status =~ /Up/)
        ? "<span class='status-running'>Running</span>"
        : "<span class='status-stopped'>Stopped</span>";
}

# =========================================================
# ROWS
# =========================================================
foreach my $line (@containers) {

    my ($name, $status) = split(/\|/, $line);

    my $safe_name   = escapeHTML($name);
    my $safe_status = escapeHTML($status);

    my $saved_url = $saved->{$name} || "";

    my $link_html = $saved_url
        ? qq{<a href="$saved_url" target="_blank">$saved_url</a>}
        : "<span style='color:#999;'>n/a</span>";

    print "<tr>";

    print qq{
<td>$safe_name</td>
<td>} . status_chip($status) . qq{</td>
<td>$link_html</td>
<td>

<form method="GET" action="">
    <input type="hidden" name="save" value="1">
    <input type="hidden" name="container" value="$safe_name">

    <input type="text"
           name="url"
           value=""
           placeholder="http(s)://IP:PORT oder https://domain.tld"
           class="input-url">

    <button type="submit" class="btn">Speichern</button>
</form>

</td>
};

    print "</tr>";
}

print "</table>";
print "</div>";

# =========================================================
# FOOTER
# =========================================================
LoxBerry::Web::lbfooter();
