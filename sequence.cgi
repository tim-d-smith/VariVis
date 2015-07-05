#!C:/Perl/bin/perl

#VariVis custom classes
use VVSeq;
use VVIni;

#VariVis Libraries
use VVRefFetch;
use program;
my $program = program->new();

#Perl Settings
use strict;
use warnings;

#CGI
use CGI qw(:cgi-lib :standard);
use CGI::Carp qw/fatalsToBrowser/;

###################################
print header();


#######################
# Standard Procedures #
#######################

#Get user settings
my $options = VVIni->new(filename=>'varivis.ini') || die "Could not access configuration file. Try running install again. Stopped";
my $GeneName = $options->get_value("gene") || die "Could not access configuration file. Try running install again. Stopped";
my $VVFolder = $options->get_value("vvfolderpath") || die "Could not access configuration file. Try running install again. Stopped";

#Set up HTML

print start_html(-head=>[Link({-rel=>"stylesheet", -type=>"text/css", -href=>"$VVFolder/varivis.css"})],-title=>"$GeneName - Sequence");

#Get Reference Sequence Data
my $RefSeq = VVRefFetch::Fetch($options->get_value("gene"),$options->get_value("refloc"),$options->get_value("acc"),$options->get_value("vvfolderpath"),$options->get_value("formatloc"),$options->get_value("locpath"));

#Get upper and lower bounds from user, otherwise use defaults
my ($upperbound,$lowerbound);

if(defined param('upper')) {$upperbound = param('upper')}
else {$upperbound = $RefSeq->get_length};
if($upperbound > $RefSeq->get_length) {$upperbound = $RefSeq->get_length};

if(defined param('lower')) {$lowerbound = param('lower')}
else {$lowerbound = 1};
if($lowerbound < 1) {$lowerbound = 1};

print "<textarea rows=\"20\" cols=\"60\" name=\"sequence\">";
for(my $counter = $lowerbound-1; $counter < $upperbound; $counter++) {
        print $RefSeq->get_sequence_by_position($counter);
}

print "</textarea>";
print "<form action=\"sequence.cgi\" action=\"GET\">";
print "<p style=\"font-size : 80%;\">range: <input size=\"4\" type=\"text\" name=\"lower\" value=\"" . $lowerbound . "\"  /> to <input size=\"4\" type=\"text\" name=\"upper\" value=\"" . $upperbound . "\" />&nbsp;<button type=\"submit\">Go</button></p>";
print "</form>";

print '<p>'. $program->get('info') . ' version ' . $program->get('version') . '</p>';
print end_html;

