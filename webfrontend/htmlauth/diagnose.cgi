#!/usr/bin/env perl

use strict;
use warnings;

use CGI qw(escapeHTML);
use LoxBerry::System;
use LoxBerry::Web;

# =========================================================
# HELPERS
# =========================================================
sub cmd_output {
    my ($cmd) = @_;
    my $out = qx{$cmd 2>/dev/null};
    chomp $out;
    return $out || "";
}

sub cmd_ok {
    my ($cmd) = @_;
    system("sh", "-c", "$cmd >/dev/null 2>&1");
    return ($? == 0) ? 1 : 0;
}

sub pkg_installed {
    my ($pkg) = @_;
    my $out = qx{dpkg -s $pkg 2>/dev/null};
    return ($out =~ /Status:\s+install ok installed/) ? 1 : 0;
}

sub plain_html {
    my ($content) = @_;
    $content = defined $content && $content ne "" ? $content : "n/a";
    $content = escapeHTML($content);
    $content =~ s/\n/<br>/g;
    return $content;
}

sub section {
    my ($title, $content, $color) = @_;
    $color ||= "#1f2937";

    my $safe_title = escapeHTML($title);
    my $safe_body  = plain_html($content);
    my $safe_color = ($color =~ /\A#[0-9a-fA-F]{6}\z/) ? $color : "#1f2937";

    print qq{
    <div class="section-box">

        <div class="section-title">
            $safe_title
        </div>

        <div class="section-content" style="color:$safe_color;">
$safe_body
        </div>

    </div>
    };
}

sub html_section {
    my ($title, $content) = @_;
    my $safe_title = escapeHTML($title);

    print qq{
    <div class="section-box">

        <div class="section-title">
            $safe_title
        </div>

        <div class="section-content">
$content
        </div>

    </div>
    };
}

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

print qq{
<div class="notice notice-info">
    Docker Systemanalyse wird durchgeführt.<br>
    Prüfung von Version, Paketquellen, Portainer, Ports, Updates und Speicherplatz.
</div>
};

# =========================================================
# SYSTEM INFO
# =========================================================
my $arch   = cmd_output("uname -m");
my $kernel = cmd_output("uname -r");
my $os     = cmd_output(q{. /etc/os-release && echo "$PRETTY_NAME"});

# =========================================================
# DOCKER STATUS
# =========================================================
my $docker_version = cmd_output("docker --version");
$docker_version ||= "nicht installiert";

my $docker_daemon = cmd_ok("docker info") ? "erreichbar" : "nicht erreichbar";

my $compose_version = cmd_output("docker compose version");
$compose_version ||= cmd_output("docker-compose --version");
$compose_version ||= "nicht gefunden";

# =========================================================
# PACKAGE CHECK
# =========================================================
my $docker_io   = pkg_installed("docker.io");
my $docker_ce   = pkg_installed("docker-ce");
my $docker_cli  = pkg_installed("docker-ce-cli");
my $containerd  = pkg_installed("containerd.io");
my $containerd_debian = pkg_installed("containerd");

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
elsif ($containerd && $containerd_debian) {
    $conflict_state = "CRITICAL";
    $conflict_text  = "Mischinstallation erkannt (containerd + containerd.io)";
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
elsif ($docker_daemon ne "erreichbar") {
    $conflict_state = "WARNING";
    $conflict_text  = "Docker ist installiert, aber der Daemon ist nicht erreichbar";
}

# =========================================================
# PORTAINER / PORTS / UPDATES
# =========================================================
my $portainer_status = cmd_output("docker inspect -f '{{.State.Status}} / {{.Config.Image}}' portainer");
$portainer_status ||= "Container 'portainer' nicht gefunden";

my $portainer_ports = cmd_output("docker port portainer");
$portainer_ports ||= "keine Portainer-Portfreigaben gefunden";

my $port_9000 = cmd_ok("ss -ltn | grep -q ':9000 '") ? "Port 9000 lauscht" : "Port 9000 lauscht nicht";
my $port_9443 = cmd_ok("ss -ltn | grep -q ':9443 '") ? "Port 9443 lauscht" : "Port 9443 lauscht nicht";

my $updates = cmd_output("apt list --upgradable | grep -E '^(docker-ce|docker-ce-cli|docker.io|containerd|containerd.io)/'");
$updates ||= "Keine Docker-relevanten APT-Updates gefunden";

my $disk = cmd_output("df -h /var/lib/docker /opt/portainer | tail -n +2");
$disk ||= cmd_output("df -h /");
$disk ||= "Speicherplatz konnte nicht ermittelt werden";

# =========================================================
# ROOT CAUSE
# =========================================================
my $root_cause = "Keine Probleme erkannt";

if ($conflict_state eq "CRITICAL") {
    $root_cause = $conflict_text;
}
elsif ($conflict_state eq "WARNING") {
    $root_cause = $conflict_text;
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
Mischinstallation erkannt. Vor Änderungen bitte Portainer-Daten sichern und Paketquellen bereinigen.<br><br>

<div class="codebox">apt remove docker.io containerd</div>

Anschließend Docker CE kontrolliert installieren oder das Plugin erneut ausführen.
    };

}
elsif ($conflict_state eq "WARNING") {

    $recommendation = qq{
<b>Hinweis</b><br><br>
Docker läuft nicht im empfohlenen Zielzustand. Prüfe Paketquelle, Docker-Daemon und Portainer-Containerstatus.
    };

}
elsif ($conflict_state eq "UNKNOWN") {

    $recommendation = qq{
<b>Docker nicht installiert</b><br><br>
Installation empfohlen. Das Plugin nutzt standardmäßig das offizielle Docker-Installationsscript.

<div class="codebox">curl -fsSL https://get.docker.com | sh</div>
    };

}
else {

    $recommendation = qq{
<b>System OK</b><br><br>
Docker ist sauber installiert. Prüfe bei Problemen zusätzlich Portainer-Status, Ports und Speicherplatz.
    };
}

# =========================================================
# OUTPUT SECTIONS
# =========================================================
section("System", "Betriebssystem: $os\nArchitektur: $arch\nKernel: $kernel");
section("Docker Version", $docker_version);
section("Docker Daemon", $docker_daemon, $docker_daemon eq "erreichbar" ? "#15803d" : "#b91c1c");
section("Docker Compose", $compose_version);
section("Installationsart", $install_type);

my $conflict_color = "#1f2937";
$conflict_color = "#15803d" if $conflict_state eq "OK";
$conflict_color = "#c2410c" if $conflict_state eq "WARNING";
$conflict_color = "#b91c1c" if $conflict_state eq "CRITICAL";

section("Konflikte", $conflict_text, $conflict_color);
section("Portainer", "$portainer_status\n$portainer_ports");
section("Ports", "$port_9000\n$port_9443");
section("Docker APT Updates", $updates);
section("Speicherplatz", $disk);
section("Root Cause", $root_cause);
html_section("Bewertung", $recommendation);

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
