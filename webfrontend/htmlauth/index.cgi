#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use LoxBerry::System;
use LoxBerry::Web;

our $htmlhead = "<link rel='stylesheet' href='docker.css'>";

LoxBerry::Web::lbheader("Docker / Container (Enterprise V3+)", undef, undef);

# =========================================================
# HOST / IP
# =========================================================
my $host = LoxBerry::System::get_localip();
$host ||= `hostname -I 2>/dev/null | awk '{print \$1}'`;
chomp($host);
$host ||= "localhost";

# =========================================================
# CONTAINER LIST (FAST MODE)
# =========================================================
my @containers = `docker ps --format "{{.Names}}|{{.Status}}|{{.Ports}}" 2>/dev/null`;
chomp @containers;

# =========================================================
# PAGE
# =========================================================
print "<div class='card'>";
print "<h1>Docker Container (Enterprise V3+)</h1>";

print qq{
<p style="color:#666;">
Fast Engine Mode (no inspect / low CPU)
</p>
};

print qq{
<table class="docker-table">
<tr style="background:#0078d4;color:white;">
<th>Name</th>
<th>Status</th>
<th>Ports / URL</th>
</tr>
};

# =========================================================
# HELPERS
# =========================================================
sub status_chip {
    my ($status) = @_;

    if ($status =~ /Up/) {
        return "<span style='background:#28a745;color:white;padding:4px 10px;border-radius:6px;'>Running</span>";
    }
    return "<span style='background:#dc3545;color:white;padding:4px 10px;border-radius:6px;'>Stopped</span>";
}

# =========================================================
# MAIN LOOP
# =========================================================
foreach my $line (@containers) {

    my ($name, $status, $ports) = split(/\|/, $line);

    $name   = escapeHTML($name   || "");
    $status = escapeHTML($status || "");
    $ports  = $ports || "";

    my $url_html = "";

    # =====================================================
    # PORT PARSING
    # =====================================================
    if ($ports =~ /0\.0\.0\.0:(\d+)->/) {

        my $port = $1;
        my $proto = ($port == 443) ? "https" : "http";
        my $url   = "$proto://$host:$port";

        $url_html .= qq{<a href="$url" target="_blank">$url</a>};
    }
    elsif ($ports =~ /:(\d+)->/) {

        my $port = $1;
        my $proto = ($port == 443) ? "https" : "http";
        my $url   = "$proto://$host:$port";

        $url_html .= qq{<a href="$url" target="_blank">$url</a>};
    }

    # =====================================================
    # UI FALLBACK
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
