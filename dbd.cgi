#!C:/Perl/bin/perl


use warnings;
use strict;

use CGI qw(:cgi-lib :standard);
use CGI::Carp qw/fatalsToBrowser/;

use DBI;
###############################################
use program;
my $program = program->new();
my $style = $program->get('style');

my $query = new CGI;

print $query->header;
print $query->start_html(-style=>{-code=>$style},-title=>"VariVis - DBD Test");
print "<h2>Available Database Drivers</h2>";
print '<hr/>';

my @drivers = DBI->available_drivers();

die "No database drivers found! \n Stopped " unless @drivers;

print '<ul>';

foreach my $driver (@drivers) {
        print "<li>".$driver."</li>";
}

print '</ul>';
print $program->get('legal');
print p('VariVis '.$program->get('version'));
print end_html;

