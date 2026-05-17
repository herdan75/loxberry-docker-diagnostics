#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use Fcntl qw(:flock);
use File::Temp qw(tempfile);
use JSON qw(decode_json encode_json);
use LoxBerry::System;
use LoxBerry::Web;

# =========================================================
# STORAGE
# =========================================================
my $store_file_old = "/opt/loxberry/data/docker_services.json";
my $store_file     = "$lbpdatadir/docker_services.json";
my $lock_file      = "$store_file.lock";

# Einmalige Migration alter Daten
if (!-e $store_file && -e $store_file_old) {
    system("cp", $store_file_old, $store_file);
}

sub read_saved_unlocked {
    return {} if !-e $store_file;

    open(my $fh, "<", $store_file) or return {};
    local $/;

    my $json = <$fh>;
    close($fh);

    my $data = {};
    eval { $data = decode_json($json || "{}"); };

    return (ref $data eq "HASH") ? $data : {};
}

sub load_saved {
    open(my $lock, ">>", $lock_file) or return read_saved_unlocked();
    flock($lock, LOCK_SH);

    my $data = read_saved_unlocked();

    close($lock);
    return $data;
}

sub valid_container_name {
    my ($name) = @_;
    return ($name && $name =~ /\A[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\z/) ? 1 : 0;
}

sub normalize_url {
    my ($url) = @_;
    $url ||= "";
    $url =~ s/\A\s+|\s+\z//g;
    return $url;
}

sub valid_service_url {
    my ($url) = @_;
    return ($url =~ m{\Ahttps?://[^\s<>"]+\z}i) ? 1 : 0;
}

# =========================================================
# SAVE ACTION
# =========================================================
my $cgi = CGI->new;

if (($ENV{REQUEST_METHOD} || "") eq "POST" && ($cgi->param('save') || "") eq "1") {

    my $container = $cgi->param('container') || "";
    my $url       = normalize_url($cgi->param('url') || "");

    my $redirect = "index.cgi";

    if (!valid_container_name($container)) {
        $redirect .= "?err=container";
    }
    elsif ($url ne "" && !valid_service_url($url)) {
        $redirect .= "?err=url";
    }
    else {
        open(my $lock, ">>", $lock_file);
        if ($lock && flock($lock, LOCK_EX)) {
            my $data = read_saved_unlocked();

            if ($url eq "") {
                delete $data->{$container};
            }
            else {
                $data->{$container} = $url;
            }

            my ($fh, $tmpfile) = tempfile("docker_services.XXXXXX", DIR => $lbpdatadir, UNLINK => 0);
            print $fh encode_json($data);
            close($fh);

            if (rename($tmpfile, $store_file)) {
                $redirect .= "?msg=saved";
            }
            else {
                unlink $tmpfile;
                $redirect .= "?err=save";
            }

            close($lock);
        }
        else {
            $redirect .= "?err=lock";
        }
    }

    print $cgi->redirect(-uri => $redirect, -status => "303 See Other");
    exit;
}

# =========================================================
# LOAD DATA
# =========================================================
my $saved = load_saved();

# =========================================================
# HOST
# =========================================================
my $host = LoxBerry::System::get_localip();
$host ||= "localhost";

# =========================================================
# CONTAINERS
# =========================================================
my @containers = qx{docker ps --format "{{.Names}}|{{.Status}}" 2>/dev/null};
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

my $err = $cgi->param('err') || "";
my $msg = $cgi->param('msg') || "";

if ($msg eq "saved") {
    print qq{<div class="notice notice-ok">Service URL gespeichert.</div>};
}
elsif ($err eq "url") {
    print qq{<div class="notice notice-error">Nur http:// und https:// URLs sind erlaubt.</div>};
}
elsif ($err) {
    print qq{<div class="notice notice-error">Service URL konnte nicht gespeichert werden.</div>};
}

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
   target="_blank"
   rel="noopener noreferrer">
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

    my ($name, $status) = split(/\|/, $line, 2);
    next if !defined $name || !defined $status;

    my $safe_name = escapeHTML($name);
    my $saved_url = normalize_url($saved->{$name} || "");
    my $safe_url  = escapeHTML($saved_url);

    my $link_html = ($saved_url && valid_service_url($saved_url))
        ? qq{<a href="$safe_url"
                target="_blank"
                rel="noopener noreferrer">$safe_url</a>}
        : "<span style='color:#999;'>n/a</span>";

    print "<tr>";

    print qq{
<td>$safe_name</td>
<td>} . status_chip($status) . qq{</td>
<td>$link_html</td>
<td>

<form method="POST" action="index.cgi">
    <input type="hidden" name="save" value="1">
    <input type="hidden" name="container" value="$safe_name">

    <input type="text"
           name="url"
           value="$safe_url"
           placeholder="http(s)://IP:PORT oder https://domain.tld"
           class="input-url">

    <button type="submit" class="btn">Speichern</button>
</form>

</td>
};

    print "</tr>";
}

print "</table>";
print "<p class='hint'>Leeres URL-Feld speichern, um eine Zuordnung zu löschen.</p>";
print "</div>";

# =========================================================
# FOOTER
# =========================================================
LoxBerry::Web::lbfooter();
