#!/usr/bin/env perl

use strict;
use warnings;

use LoxBerry::System;
use LoxBerry::Web;

our $htmlhead = "<link rel='stylesheet' href='docker.css'>";
LoxBerry::Web::lbheader("Docker Systemdiagnose (Pro)", undef, undef);

print "<div class='card'>";
print "<h1>Docker Systemdiagnose (Intelligent Pro)</h1>";

# ---------------------------------------------------------
# INFO
# ---------------------------------------------------------
print qq{
<div class="analysis-info-small">
    Docker Systemanalyse wird durchgeführt.<br>
    Bitte kurz warten...
</div>
};

# ---------------------------------------------------------
# SYSTEM INFO
# ---------------------------------------------------------
my $arch   = `uname -m 2>/dev/null`; chomp $arch;
my $kernel = `uname -r 2>/dev/null`; chomp $kernel;

# ---------------------------------------------------------
# DOCKER VERSION (robuster FIX)
# ---------------------------------------------------------
my $docker_version = `docker --version 2>/dev/null || true`;
chomp $docker_version;
$docker_version ||= "nicht installiert";

# ---------------------------------------------------------
# INSTALLATION DETECTION
# ---------------------------------------------------------
my $repo_file = `grep -l docker /etc/apt/sources.list.d/* 2>/dev/null`;
chomp $repo_file;

my $install_type = "Unbekannt";

if ($repo_file) {
    $install_type = "APT Repository (docker-ce)";
}
elsif ($docker_version =~ /build/) {
    $install_type = "get.docker.com Installation";
}
elsif ($docker_version ne "nicht installiert") {
    $install_type = "Docker vorhanden (Quelle unklar)";
}
else {
    $install_type = "Nicht installiert";
}

# ---------------------------------------------------------
# CONFLICT CHECK
# ---------------------------------------------------------
my $docker_io = `dpkg -l docker.io 2>/dev/null`;
my $docker_ce = `dpkg -l docker-ce 2>/dev/null`;

my $conflict_state = "OK";
my $conflict_text  = "Keine Konflikte erkannt";

if ($docker_io && $docker_ce) {
    $conflict_state = "CRITICAL";
    $conflict_text  = "KRITISCH: docker.io + docker-ce installiert";
}
elsif ($docker_io) {
    $conflict_state = "WARNING";
    $conflict_text  = "docker.io installiert (Debian Version)";
}
elsif ($docker_ce) {
    $conflict_state = "OK";
    $conflict_text  = "docker-ce installiert (empfohlen)";
}
else {
    $conflict_state = "UNKNOWN";
    $conflict_text  = "Docker Installation nicht eindeutig erkannt";
}

# ---------------------------------------------------------
# ARCH SUPPORT
# ---------------------------------------------------------
my $support_status = "Unbekannt";

if ($arch =~ /x86_64/) {
    $support_status = "x86_64 – vollständig unterstützt";
}
elsif ($arch =~ /aarch64|arm64|meson64/) {
    $support_status = "ARM64 / meson64 – get.docker.com empfohlen";
}
else {
    $support_status = "Spezielle Architektur";
}

# ---------------------------------------------------------
# ROOT CAUSE
# ---------------------------------------------------------
my $root_cause = "Keine Probleme erkannt";

if ($conflict_state eq "CRITICAL") {
    $root_cause = "Mischinstallation (docker.io + docker-ce)";
}
elsif ($arch =~ /aarch64|arm64|meson64/) {
    $root_cause = "ARM64 System – apt Installation kritisch";
}

# ---------------------------------------------------------
# ACTION ENGINE
# ---------------------------------------------------------
my $action = "OK";

if ($conflict_state eq "CRITICAL") {
    $action = "REINSTALL";
}
elsif ($docker_version eq "nicht installiert") {
    $action = "INSTALL";
}
elsif ($conflict_state eq "WARNING") {
    $action = "CHECK";
}

# ---------------------------------------------------------
# RECOMMENDATION
# ---------------------------------------------------------
my $recommendation = "";

if ($action eq "REINSTALL" || $action eq "INSTALL") {

    $recommendation = qq{
<b>Empfehlung</b><br><br>
Docker Installation über offizielles Script:<br><br>
<code>curl -fsSL https://get.docker.com | sh</code>
    };

}
elsif ($action eq "CHECK") {

    $recommendation = qq{
<b>Hinweis</b><br><br>
docker.io vorhanden – kein kritischer Fehler.
    };

}
else {

    $recommendation = qq{
<b>System OK</b><br><br>
Keine Aktion erforderlich.
    };
}

# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------
print "<h3>System</h3>";
print "<pre>Architektur: $arch\nKernel: $kernel</pre>";

print "<h3>Docker Version</h3>";
print "<pre>$docker_version</pre>";

print "<h3>Installationsart</h3>";
print "<pre>$install_type</pre>";

print "<h3>Konflikte</h3>";

if ($conflict_state eq "OK") {
    print "<pre style='color:green;'>$conflict_text</pre>";
}
elsif ($conflict_state eq "WARNING") {
    print "<pre style='color:orange;'>$conflict_text</pre>";
}
elsif ($conflict_state eq "CRITICAL") {
    print "<pre style='color:red;'>$conflict_text</pre>";
}
else {
    print "<pre>$conflict_text</pre>";
}

print "<h3>Support Status</h3>";
print "<pre>$support_status</pre>";

print "<h3>Root Cause</h3>";
print "<pre>$root_cause</pre>";

print "<h3>Bewertung</h3>";
print "<div class='diagnose-section'>$recommendation</div>";

# ---------------------------------------------------------
# BUTTONS
# ---------------------------------------------------------
print qq{
<div style="text-align:center; margin:25px;">

    <a href="/admin/plugins/docker/index.cgi"
       class="btn"
       style="background:#6c757d;">
       Schließen
    </a>

    <a href="diagnose.cgi"
       class="btn"
       style="background:#0078d4;">
       Neu laden
    </a>

</div>
};

print "</div>";

LoxBerry::Web::lbfooter();
