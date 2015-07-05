#!C:/Perl/bin/perl

#VariVis custom classes
use VVIni;
use VVMutFetch;
use VVdbi;

#Perl Settings
use strict;
use warnings;

#CGI
use CGI qw(:cgi-lib :standard);

###################################

#Make sure we can output to browser
print header();

#Get user settings
my $options = VVIni->new(filename=>'varivis.ini') || die "Could not access configuration file. Try running install again. Stopped ";
my $VVFolder = $options->get_value("vvfolderpath") || die "Could not access configuration file. Try running install again. Stopped";

#Get Variant to display
my $Variant;
if(param('var')) {$Variant = param('var')} else {$Variant = "VariVis"}

my $ArrayIndex;
if(param('index')) {$ArrayIndex = param('index')} else {$ArrayIndex = 0}

###################################


print start_html(-head=>[Link({-rel=>"stylesheet", -type=>"text/css", -href=>"$VVFolder/subdoc.css"})],-title=>"$Variant");
print "<h1>Variant Details</h1>";

if($Variant eq "VariVis") {print end_html;}
else {
        my @SplitVar = split(/\|/,$Variant);
        my $Size = @SplitVar;
        
        if ($Size > 1) {

                print div({-class=>'name'},"Multiple Variants");
                print "<div class=\"main\">";
                print p("Please select one of the variants below");
                print "<ul>";
                
                for(my $i = 0; $i < $Size; $i++) {
                        print li({-type=>"disc"},a({-href=>"subdoc.cgi?var=$SplitVar[$i]",-title=>$SplitVar[$i]},$SplitVar[$i]))
                }
                
                print "</ul></div>";
                print end_html;

        } else {

                my $colDNA = $options->get_value("DBcolumnname");
                my $colProtein = $options->get_value("DBProtname");
                my $colRE = ','.$options->get_value("DBREname") if $options->get_value("DBREname");
                my $colDisease = ','.$options->get_value("DBDiseasename") if $options->get_value("DBDiseasename");
                my $colRemarks = ','.$options->get_value("DBRemarksname") if $options->get_value("DBRemarksname");
                my $colReference = ','.$options->get_value("DBRefname") if $options->get_value("DBRefname");
                my $table = $options->get_value("DBtablename"); if(!$table) {$table = 'default'};
                my $GeneName = $options->get_value('gene');

                my @AllVariants = VVdbi::Query("SELECT $colDNA, $colProtein $colRE $colDisease $colRemarks $colReference from $table", $colDNA,$Variant);
                my $allVarSize = @AllVariants;

                if($allVarSize <=0){
                        @AllVariants = VVdbi::Query("SELECT $colDNA, $colProtein $colRE $colDisease $colRemarks $colReference from $table", $colProtein,$Variant);
                        $allVarSize = @AllVariants;
                }

                $colRE =~ s/,//;
                $colDisease =~ s/,//;
                $colRemarks =~ s/,//;
                $colReference =~ s/,//;

                my $DNA = $AllVariants[$ArrayIndex]{$colDNA};
                my $Protein = $AllVariants[$ArrayIndex]{$colProtein};
                my $RE = $AllVariants[$ArrayIndex]{$colRE};
                my $Disease = $AllVariants[$ArrayIndex]{$colDisease};
                my $Remarks = $AllVariants[$ArrayIndex]{$colRemarks};
                my $Reference = $AllVariants[$ArrayIndex]{$colReference};

                print "<table><tr><td class=\"cat_name\">Variant Name:</td><td class=\"name\">$DNA</td></tr>";
                print "<tr><td class=\"category\">Protein:</td><td class=\"data\">$Protein</td></tr>";
                print "<tr><td class=\"category\">RE-Site:</td><td class=\"data\">$RE</td></tr>" if $RE;
                print "<tr><td class=\"category\">Phenotype:</td><td class=\"data\">$Disease</td></tr>" if $Disease;
                print "<tr><td class=\"category\">Remarks:</td><td class=\"remarks\" colspan=\"3\">$Remarks</td></tr>" if $Remarks;
                print "<tr><td class=\"info\" colspan=\"2\">Further Information:</td></tr>";
                print "<tr><td colspan=\"2\">";
                print a({-target=>"_top",-href=>"http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=$Reference", -title=>"PubMed"},img({-alt=>"PubMed", src=>"$VVFolder/i/pm.gif", height=>49, width=>111})) if $Reference;
                print a({-target=>"_top",-href=>"http://scholar.google.com/scholar?q=$GeneName+\"$Variant\"", -title=>"Google Scholar"},img({-alt=>"Google Scholar", -src=>"$VVFolder/i/gs.gif", -height=>49, -width=>111}));
                print "</td></tr></table>";
                print "<div style=\"text-align:left\">";
                if($allVarSize > 1 && $ArrayIndex > 0) {
                        my $prevIndex = $ArrayIndex -1;
                        print a({-href=>"subdoc.cgi?var=$Variant&index=$prevIndex"},"Prev");
                }
                print "  ";
                if($allVarSize > 1 && $ArrayIndex < $allVarSize-1) {
                        my $newIndex = $ArrayIndex +1;
                        print a({-href=>"subdoc.cgi?var=$Variant&index=$newIndex"},"Next");
                }
                print "</div>";
                print end_html;

        }
}


