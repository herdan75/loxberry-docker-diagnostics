#!/usr/bin/env perl

use strict;
use warnings;

use LoxBerry::System;
use LoxBerry::Web;

our $htmlhead = "<link rel='stylesheet' href='docker.css'>";

LoxBerry::Web::lbheader(
    "Docker Systemdiagnose (Pro)",
    undef,
    undef
);

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
my $arch   = `uname -m 2>/dev/null`;
my $kernel = `uname -r 2>/dev/null`;

chomp $arch;
chomp $kernel;

# ---------------------------------------------------------
# DOCKER VERSION
# ---------------------------------------------------------
my $docker_version = `docker --version 2>/dev/null`;

chomp $docker_version;

$docker_version ||= "nicht installiert";

# ---------------------------------------------------------
# ROBUSTER PACKAGE CHECK
# ---------------------------------------------------------
sub pkg_installed {

    my ($pkg) = @_;

    my $out = `dpkg -s $pkg 2>/dev/null`;

    return (
        $out =~ /Status:\s+install ok installed/
    ) ? 1 : 0;
}

my $docker_io   = pkg_installed("docker.io");
my $docker_ce   = pkg_installed("docker-ce");
my $docker_cli  = pkg_installed("docker-ce-cli");
my $containerd  = pkg_installed("containerd.io");

# ---------------------------------------------------------
# INSTALLATION TYPE
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# CONFLICT CHECK
# ---------------------------------------------------------
my $conflict_state = "OK";
my $conflict_text  = "Keine Konflikte erkannt";

if ($docker_io && ($docker_ce || $docker_cli)) {

    $conflict_state = "CRITICAL";

    $conflict_text =
        "Mischinstallation erkannt (docker.io + docker-ce)";

}
elsif ($docker_io) {

    $conflict_state = "WARNING";

    $conflict_text =
        "docker.io installiert (nicht empfohlen)";

}
elsif ($docker_ce && $docker_cli && $containerd) {

    $conflict_state = "OK";

    $conflict_text =
        "Docker CE Installation sauber";

}
elsif ($docker_version eq "nicht installiert") {

    $conflict_state = "UNKNOWN";

    $conflict_text =
        "Docker ist nicht installiert";
}

# ---------------------------------------------------------
# ROOT CAUSE
# ---------------------------------------------------------
my $root_cause = "Keine Probleme erkannt";

if ($conflict_state eq "CRITICAL") {

    $root_cause =
        "Mischinstallation docker.io + docker-ce";

}
elsif ($conflict_state eq "WARNING") {

    $root_cause =
        "Debian docker.io aktiv";

}
elsif ($conflict_state eq "UNKNOWN") {

    $root_cause =
        "Docker fehlt";
}

# ---------------------------------------------------------
# RECOMMENDATION
# ---------------------------------------------------------
my $recommendation = "";

if ($conflict_state eq "CRITICAL") {

    $recommendation = qq{
<b>Empfehlung</b><br><br>
Mischinstallation erkannt – Bereinigung empfohlen:<br><br>
<code>apt remove docker.io</code><br><br>
Anschließend optional:<br><br>
<code>curl -fsSL https://get.docker.com | sh</code>
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
Installation empfohlen:<br><br>
<code>curl -fsSL https://get.docker.com | sh</code>
    };

}
else {

    $recommendation = qq{
<b>System OK</b><br><br>
Docker ist sauber installiert.
    };
}

# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------
print "<h3>System</h3>";

print "<pre>";
print "Architektur: $arch\n";
print "Kernel: $kernel";
print "</pre>";

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

print "<h3>Root Cause</h3>";
print "<pre>$root_cause</pre>";

print "<h3>Bewertung</h3>";

print "<div class='diagnose-section'>";
print $recommendation;
print "</div>";

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
