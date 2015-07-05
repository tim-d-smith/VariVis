#!C:/Perl/bin/perl

use strict;
use warnings;

use VVIni;

use CGI qw(:cgi-lib :standard);
use CGI::Carp qw/fatalsToBrowser/;

###############################################
use program;
my $program = program->new();
my $style = $program->get('style');

my $query = new CGI;
my $options = VVIni->new(filename=>'varivis.ini') || die "Could not access configuration file. Try running install again. Stopped ";

print $query->header;
print $query->start_html(-style=>{-code=>$style},-title=>"Install VariVis");

print $query->start_form;

if($query->param("initauth")) {

        #Encryption
        my $password = $query->param("initauth");
        $password = crypt($password,'vv');
        
        
        $options->set_value("auth",$password);
        $options->wrap_it;
        $query->param("initauth",undef);
        print h2("VariVis Installation");
        print '<hr />';
        print p("Password set!");
        print a({-href=>"install.cgi"},"Click to continue");
        print $program->get('legal');
        print p('VariVis '.$program->get('version'));
        print end_form;
        print end_html;
        exit;
}

if($options->get_value("auth") eq "") {
        print h2("Thank you for choosing VariVis");
        print p("To start using VariVis, just fill in the options as they appear.");
        print p("First, you must define a password to access this installation page in the future.");
        print p("Password:",$query->password_field("initauth"),$query->submit("Ok"));
        print $query->end_form;
        print $program->get('legal');
        print p('VariVis '.$program->get('version'));
        print end_html;
        exit;
}
if($query->param('Save') eq 'Save') {
        my $errors;

        if(!$query->param('vvfolderpath')) {$errors .= '<li>Relative path to \'varivis\' folder</li>';}
        if(!$query->param('gene')) {$errors .= '<li>Gene Symbol</li>';}
        if(!$query->param('acc')) {$errors .= '<li>Accession Number or filename</li>';}
        if(!$query->param('DBcolumnname')) {$errors .= '<li>DNA Level Variant Name Field</li>';}
        if(!$query->param('DBProtname')) {$errors .= '<li>Protein Level Variant Name Field</li>';}
        
        if($query->param('DBtype') eq 'CSV') {
                if(!$query->param('CSVPath')) {$errors .= '<li>CSV file system path</li>';}
                if(!$query->param('CSVfile')) {$errors .= '<li>CSV filename</li>';}
                if(!$query->param('SepChar')) {$errors .= '<li>CSV separating character</li>';}
        } else {
                if(!$query->param('DBname')) {$errors .= '<li>Database name</li>';}
                if(!$query->param('DBtablename')) {$errors .= '<li>Database table</li>';}
                if(!$query->param('DBhost')) {$errors .= '<li>Database host</li>';}
                if(!$query->param('port')) {$errors .= '<li>Database port</li>';}
                if(!$query->param('user')) {$errors .= '<li>Username</li>';}
                if(!$query->param('pass')) {$errors .= '<li>Password</li>';}
        }
        
        
        if($errors) {
                $errors ='<div class="error">Unable to complete installation. The following fields are required:<ul>'.$errors;
                print $errors;
                print '</ul></div><p>Please go <a href="install.cgi">back</a> and try again.</p>';
                print $query->end_form;
                print $program->get('legal');
                print p('VariVis '.$program->get('version'));
                print end_html;
                exit;
        }
                
        
        foreach my $key ($query->param) {
                $options->set_value($key,$query->param($key));
        }
        $options->wrap_it;
        print h2("Installation Complete");
        print '<hr />';
        print p('Installation of VariVis is now complete. Click <a href="test.cgi">here</a> to test your installation');
        print $query->end_form;
        print $program->get('legal');
        print p('VariVis '.$program->get('version'));
        print end_html;
        exit;
}
if($query->param("auth")) {
        print h2("VariVis Installation");
        print '<hr />';

        #Check Password
        my $bail = 0;
        my $u_pass = $query->param("auth");
        $u_pass = crypt($u_pass,'vv');
        my $actual_pass = $options->get_value('auth');
   
        if($u_pass ne $actual_pass) {
                print '<div class="error">Incorrect Password</div>';
                $bail =1;
        }
   
        my $default = undef;
        my $help_url = $program->get('help_url');

        #TEST BioPerl is present
        eval 'use Bio::Perl';
        if ($@) {
                print '<div class="error">We were unable to detect the <strong>BioPerl modules</strong> on this server. Please check to make sure they are installed. For more information refer to the <a href="' . $help_url . '#bioperl" target="_blank">VariVis help site</a> or <a href="http://www.bioperl.org/">BioPerl.org</a>.</div>';
                $bail = 1;
        }
        #TEST DBI...
        eval 'use DBI';
        if ($@) {
                print '<div class="error">We were unable to detect the <strong>Perl DBI</strong> on this server. Please check to make sure it is installed. For more information refer to the <a href="' . $help_url . '#dbi" target="_blank">VariVis help site</a> or <a href="http://dbi.perl.org/">dbi.perl.org</a>.</div>';
                $bail = 1;
        }
        #TEST CGI.pm is present
        eval 'use CGI';
        if ($@) {
                print '<div class="error">We were unable to detect the <strong>CGI module</strong> on this server. Please check to make sure it is installed. For more information refer to the <a href="' . $help_url . '#cgi" target="_blank">VariVis help site</a> or <a href="http://search.cpan.org/dist/CGI.pm/CGI.pm">http://search.cpan.org/dist/CGI.pm/CGI.pm</a>.</div>';
                $bail = 1;
        }

        if(!$bail) {

        print "<table><caption>Program Settings</caption>";
        $default = $options->get_value('vvfolderpath') ? $options->get_value('vvfolderpath') : 'varivis';
        print Tr(th("Relative path to 'varivis' folder: *"),td($query->textfield(-name=>'vvfolderpath',-default=>$default)),td({-class=>'note'},'Exclude the trailing "/"'),td('<strong><a href="'.$help_url.'#relpath" target="_blank">?</a></strong>'));
        print "</table>";

        print "<table><caption>Reference Sequence</caption>";
        $default = $options->get_value('gene') ? $options->get_value('gene') : undef;
        print Tr(th("Gene symbol: *"),td($query->textfield(-name=>'gene',-default=>$default)),td({-class=>'note'},'Case Sensitive'),td('<strong><a href="'.$help_url.'#symbol" target="_blank">?</a></strong>'));
        $default = $options->get_value('refloc') ? $options->get_value('refloc') : undef;
        print Tr(th("Reference sequence location: *"),td($query->popup_menu(-name=>'refloc',-Values=>['Local','Genbank','RefSeq','Embl'],-default=>$default)),td({-class=>'note'},'&nbsp;'),td('<strong><a href="'.$help_url.'#refloc" target="_blank">?</a></strong>'));
        $default = $options->get_value('acc') ? $options->get_value('acc') : undef;
        print Tr(th("Accession Number or filename: *"),td($query->textfield(-name=>'acc',-default=>$default)),td({-class=>'note'},'Accession.Version (e.g: 111111.1)'),td('<strong><a href="'.$help_url.'#acc" target="_blank">?</a></strong>'));
        $default = $options->get_value('locpath') ? $options->get_value('locpath') : 'c:/htdocs/';
        print Tr(th("LOCAL sequence file path:"),td($query->textfield(-name=>'locpath',-default=>$default)),td({-class=>'note'},'Include the trailing "/"'),td('<strong><a href="'.$help_url.'#locpath" target="_blank">?</a></strong>'));
        $default = $options->get_value('formatloc') ? $options->get_value('formatloc') : undef;
        print Tr(th("LOCAL sequence file format:"),td($query->popup_menu(-name=>'formatloc',-Values=>['ABI','ACE','ALF','ASCIITree','BSML','CHADO','CTF','EMBL','EXP','FASTA','FASTQ','GAME','GCG','GenBank','KEGG','LocusLink','MetaFASTA','PHD','PIR','PLN','Qual','Raw','SCF','Tab','TIGR','ZTR'],-default=>$default)),,td({-class=>'note'},'For LOCAL files only'),td('<strong><a href="'.$help_url.'#local" target="_blank">?</a></strong>'));
        print "</table>";

        print "<table><caption>Variation Data</caption>";
        $default = $options->get_value('DBtype') ? $options->get_value('DBtype') : 'CSV';
        print Tr(th("Database type: *"),td($query->popup_menu(-name=>'DBtype',-Values=>['CSV','mySQL','Oracle','PostgresSQL'],-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#type" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBcolumnname') ? $options->get_value('DBcolumnname') : undef;
        print Tr(th("DNA Level Variant Name Field: *"),td($query->textfield(-name=>'DBcolumnname',-default=>$default)),td({-class=>'note'},'<a href="http://www.hgvs.org/mutnomen/">HGVS Nomenclature</a>'),td('<strong><a href="'.$help_url.'#columns" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBProtname') ? $options->get_value('DBProtname') : undef;
        print Tr(th("Protein Level Variant Name Field: *"),td($query->textfield(-name=>'DBProtname',-default=>$default)),td({-class=>'note'},'<a href="http://www.hgvs.org/mutnomen/">HGVS Nomenclature</a>'),td('<strong><a href="'.$help_url.'#columns" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBREname') ? $options->get_value('DBREname') : undef;
        print Tr(th("Restriction Enzyme Site Change Field:"),td($query->textfield(-name=>'DBREname',-default=>$default)),td({-class=>'note'},'Free text'),td('<strong><a href="'.$help_url.'#columns" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBDiseasename') ? $options->get_value('DBDiseasename') : undef;
        print Tr(th("Phenotype Description Field:"),td($query->textfield(-name=>'DBDiseasename',-default=>$default)),td({-class=>'note'},'Free text'),td('<strong><a href="'.$help_url.'#columns" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBRemarksname') ? $options->get_value('DBRemarksname') : undef;
        print Tr(th("Remarks Field:"),td($query->textfield(-name=>'DBRemarksname',-default=>$default)),td({-class=>'note'},'Free text'),td('<strong><a href="'.$help_url.'#columns" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBRefname') ? $options->get_value('DBRefname') : undef;
        print Tr(th("PubMed ID Field:"),td($query->textfield(-name=>'DBRefname',-default=>$default)),td({-class=>'note'},'Pubmed ID'),td('<strong><a href="'.$help_url.'#columns" target="_blank">?</a></strong>'));
        print "</table>";

        print "<table><caption>CSV Settings</caption>";
        $default = $options->get_value('CSVPath') ? $options->get_value('CSVPath') : 'c:/htdocs/';
        print Tr(th("CSV file system path:"),td($query->textfield(-name=>'CSVPath',-default=>$default)),td({-class=>'note'},'Include the trailing "/"'),td('<strong><a href="'.$help_url.'#csvpath" target="_blank">?</a></strong>'));
        $default = $options->get_value('CSVfile') ? $options->get_value('CSVfile') : undef;
        print Tr(th("CSV filename:"),td($query->textfield(-name=>'CSVfile',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#csvfile" target="_blank">?</a></strong>'));
        $default = $options->get_value('SepChar') ? $options->get_value('SepChar') : ',';
        print Tr(th("CSV separating character:"),td($query->textfield(-name=>'SepChar',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#sepchar" target="_blank">?</a></strong>'));
        print "</table>";

        print "<table><caption>MySQL/Oracle/Postgres Settings</caption>";
        $default = $options->get_value('DBname') ? $options->get_value('DBname') : undef;
        print Tr(th("Database name:"),td($query->textfield(-name=>'DBname',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#dbname" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBtablename') ? $options->get_value('DBtablename') : 'default';
        print Tr(th("Database table:"),td($query->textfield(-name=>'DBtablename',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#dbtable" target="_blank">?</a></strong>'));
        $default = $options->get_value('DBhost') ? $options->get_value('DBhost') : 'localhost';
        print Tr(th("Database host:"),td($query->textfield(-name=>'DBhost',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#dbhost" target="_blank">?</a></strong>'));
        $default = $options->get_value('port') ? $options->get_value('port') : '3306';
        print Tr(th("Database port:"),td($query->textfield(-name=>'port',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#dbport" target="_blank">?</a></strong>'));
        $default = $options->get_value('user') ? $options->get_value('user') : undef;
        print Tr(th("Username:"),td($query->textfield(-name=>'user',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#user" target="_blank">?</a></strong>'));
        $default = $options->get_value('pass') ? $options->get_value('pass') : undef;
        print Tr(th("Password:"),td($query->password_field(-name=>'pass',-default=>$default)),td({-class=>'note'},'&nbsp'),td('<strong><a href="'.$help_url.'#pass" target="_blank">?</a></strong>'));
        print "</table>";
        
        print $query->submit("Save");
        }
        
        print $program->get('legal');
        print p('VariVis '.$program->get('version'));
        print end_form;
        print end_html;
        exit;
        
}



print h2("VariVis Installation");
print '<hr />';
print p({-style=>"font-weight:bold;"},"Login: ",$query->password_field('auth'),$query->submit("Ok"));
print $program->get('legal');
print p('VariVis '.$program->get('version'));
print $query->end_form;
print $query->end_html;

