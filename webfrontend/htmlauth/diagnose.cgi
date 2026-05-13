#!/usr/bin/env perl

use strict;
use warnings;

use LoxBerry::System;
use LoxBerry::Web;

# =========================================================
# HEADER
# =========================================================
our $htmlhead = "<link rel='stylesheet' href='docker.css'>";

LoxBerry::Web::lbheader(
    "Docker Systemdiagnose",
    undef,
    undef
);

print "<div class='card'>";
print "<h1>Docker Systemdiagnose</h1>";

# =========================================================
# INFO BOX (schlicht)
# =========================================================
print qq{
<div style="
    background:#eef5fb;
    border:1px solid #c8dff2;
    color:#1f2937;
    border-radius:6px;
    padding:12px;
    margin-top:20px;
">
    Docker Systemanalyse wird durchgeführt.<br>
    Prüfung von Version, Paketquellen und möglichen Konflikten.
</div>
};

# =========================================================
# SYSTEM INFO
# =========================================================
my $arch   = `uname -m 2>/dev/null`; chomp $arch;
my $kernel = `uname -r 2>/dev/null`; chomp $kernel;

# =========================================================
# DOCKER VERSION
# =========================================================
my $docker_version = `docker --version 2>/dev/null`;
chomp $docker_version;
$docker_version ||= "nicht installiert";

# =========================================================
# PACKAGE CHECK
# =========================================================
sub pkg_installed {
    my ($pkg) = @_;
    my $out = `dpkg -s $pkg 2>/dev/null`;
    return ($out =~ /Status:\s+install ok installed/) ? 1 : 0;
}

my $docker_io   = pkg_installed("docker.io");
my $docker_ce   = pkg_installed("docker-ce");
my $docker_cli  = pkg_installed("docker-ce-cli");
my $containerd  = pkg_installed("containerd.io");

# =========================================================
# INSTALLATION TYPE
# =========================================================
my $install_type = "Nicht installiert";

if ($docker_ce && $docker_cli && $containerd) {
    $install_type = "Docker CE (saubere Installation)";
}
elsif ($docker_io) {
    $install_type = "Docker IO (Debian Paket)";
}
elsif ($docker_version ne "nicht installiert") {
    $install_type = "Docker vorhanden (unklare Quelle)";
}

# =========================================================
# CONFLICT CHECK
# =========================================================
my $conflict_state = "OK";
my $conflict_text  = "Keine Konflikte erkannt";

if ($docker_io && ($docker_ce || $docker_cli)) {
    $conflict_state = "CRITICAL";
    $conflict_text  = "Mischinstallation erkannt (docker.io + docker-ce)";
}
elsif ($docker_io) {
    $conflict_state = "WARNING";
    $conflict_text  = "docker.io installiert (nicht empfohlen)";
}
elsif ($docker_ce && $docker_cli && $containerd) {
    $conflict_state = "OK";
    $conflict_text  = "Docker CE Installation sauber";
}
elsif ($docker_version eq "nicht installiert") {
    $conflict_state = "UNKNOWN";
    $conflict_text  = "Docker ist nicht installiert";
}

# =========================================================
# ROOT CAUSE
# =========================================================
my $root_cause = "Keine Probleme erkannt";

if ($conflict_state eq "CRITICAL") {
    $root_cause = "Mischinstallation docker.io + docker-ce";
}
elsif ($conflict_state eq "WARNING") {
    $root_cause = "Debian docker.io aktiv";
}
elsif ($conflict_state eq "UNKNOWN") {
    $root_cause = "Docker fehlt";
}

# =========================================================
# RECOMMENDATION
# =========================================================
my $recommendation = "";

if ($conflict_state eq "CRITICAL") {

    $recommendation = qq{
<b>Empfehlung</b><br><br>
Mischinstallation erkannt – Bereinigung empfohlen:<br><br>

<div class="codebox">apt remove docker.io</div>

Anschließend optional:

<div class="codebox">curl -fsSL https://get.docker.com | sh</div>
    };

}
elsif ($conflict_state eq "WARNING") {

    $recommendation = qq{
<b>Hinweis</b><br><br>
docker.io ist installiert.<br>
Kein kritischer Fehler, aber Docker CE wird empfohlen.
    };

}
elsif ($conflict_state eq "UNKNOWN") {

    $recommendation = qq{
<b>Docker nicht installiert</b><br><br>

Installation empfohlen:

<div class="codebox">curl -fsSL https://get.docker.com | sh</div>
    };

}
else {

    $recommendation = qq{
<b>System OK</b><br><br>
Docker ist sauber installiert.
    };
}

# =========================================================
# SECTION HELPER (schlicht, LoxBerry‑Standard)
# =========================================================
sub section {

    my ($title, $content, $color) = @_;
    $color ||= "#1f2937";

    print qq{
    <div class="section-box">

        <div class="section-title">
            $title
        </div>

        <div class="section-content" style="color:$color;">
$content
        </div>

    </div>
    };
}

# =========================================================
# OUTPUT SECTIONS
# =========================================================
section("System", "Architektur: $arch\nKernel: $kernel");
section("Docker Version", $docker_version);
section("Installationsart", $install_type);

my $conflict_color = "#1f2937";
$conflict_color = "#15803d" if $conflict_state eq "OK";
$conflict_color = "#c2410c" if $conflict_state eq "WARNING";
$conflict_color = "#b91c1c" if $conflict_state eq "CRITICAL";

section("Konflikte", $conflict_text, $conflict_color);
section("Root Cause", $root_cause);

# =========================================================
# BEWERTUNG
# =========================================================
print qq{
<div class="section-box">

    <div class="section-title">
        Bewertung
    </div>

    <div class="section-content">
        $recommendation
    </div>

</div>
};

# =========================================================
# BUTTONS
# =========================================================
print qq{
<div style="text-align:center; margin-top:30px;">

    <a href="/admin/plugins/docker/index.cgi"
       class="btn">
       Zur Übersicht
    </a>

    <a href="diagnose.cgi"
       class="btn"
       style="margin-left:10px;">
       Neu laden
    </a>

</div>
};

print "</div>";

LoxBerry::Web::lbfooter();

