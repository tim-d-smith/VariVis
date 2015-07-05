#!C:/Perl/bin/perl

use strict;
use warnings;

use VVIni;

use CGI qw(:cgi-lib :standard);
use CGI::Carp qw/fatalsToBrowser/;
###############################################
use program;
my $program = program->new();

my $query = new CGI;
my $options = VVIni->new(filename=>'varivis.ini');
my $GeneName = $options->get_value("gene") || die "Could not access configuration file. Try running install again. Stopped";

my $style = $program->get('style');

print $query->header;
print $query->start_html(-style=>{-code=>$style},-title=>"Testing Installation");

my $imgpath = $options->get_value('vvfolderpath');

print h2("Installation Test");
print '<hr/>';

#PROGRAM SETTINGS TEST...
print "<table><tr><th>Relative path to 'varivis' folder:</th><td><img src=\"".$imgpath."/i/dna.gif\" />Can you see the DNA icon? If not, please <a href=\"install.cgi\">adjust</a> your settings.</td></tr>";


#REFERENCE SEQUENCE TEST
print '<tr><th>Reference Sequence Access:</th><td>';
eval{
        use Bio::Perl;
        use VVRefFetch;
        my $GeneName = $options->get_value("gene") || die "Could not access configuration file. Try running install again. Stopped";
        my $RefSeq = VVRefFetch::Fetch($options->get_value("gene"),$options->get_value("refloc"),$options->get_value("acc"),$options->get_value("vvfolderpath"),$options->get_value("formatloc"),$options->get_value("locpath"));
};
if($@) {print '<span class="error">Error: </span>'.$@;}else{print '<span class="ok">OK</span>';};
print '</td></tr>';


#VARIATION DATA TEST
print '<tr><th>Database Access:</th><td>';
eval{
        my $colDNA = $options->get_value("DBcolumnname");
        my $colProtein = $options->get_value("DBProtname");
        my $colRE = ', '.$options->get_value("DBREname") if $options->get_value("DBREname");
        my $colDisease = ', '.$options->get_value("DBDiseasename") if $options->get_value("DBDiseasename");
        my $colRemarks = ', '.$options->get_value("DBRemarksname") if $options->get_value("DBRemarksname");
        my $colReference = ', '.$options->get_value("DBRefname") if $options->get_value("DBRefname");
        my $table = $options->get_value("DBtablename"); if(!$table) {$table = 'default'};
        use VVdbi;
        my @AllVariants = VVdbi::Query("SELECT $colDNA, $colProtein $colRE $colDisease $colRemarks $colReference from $table");
        
};
if($@) {print '<span class="error">Error: </span>'.$@;}else{print '<span class="ok">OK</span>';};
print '</td></tr>';

print '</table>';

print p('If all three tests have been passed, then you\'re ready to <a href="varivis.cgi">go</a>. Otherwise, you need to <a href="install.cgi">adjust</a> your settings.');

print $program->get('legal');
print p('VariVis '.$program->get('version'));
print end_form;
print end_html;

