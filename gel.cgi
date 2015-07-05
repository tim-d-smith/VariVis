#!C:/Perl/bin/perl

#VariVis custom classes
use VVSeq;
use VVVar;
use VVIni;

#VariVis Libraries
use VVRefFetch;
use VVMutFetch;
use program;
my $program = program->new();

#Perl Settings
#use strict;
use warnings;

use Bio::Perl;
use POSIX;

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

print start_html(-head=>[Link({-rel=>"stylesheet", -type=>"text/css", -href=>"$VVFolder/gel.css"}),script({-type=>'text/javascript',-src=>"$VVFolder/j/varivis.js"},undef),script({-type=>"text/javascript"},"window.onload=function(){enableTooltips('main')};this.focus()")],-title=>"$GeneName - Gel View");

#Get Reference Sequence Data
my $RefSeq = VVRefFetch::Fetch($options->get_value("gene"),$options->get_value("refloc"),$options->get_value("acc"),$options->get_value("vvfolderpath"),$options->get_value("formatloc"),$options->get_value("locpath"));


##############################
# Decide which output to use #
##############################
#if(defined param('upper') || defined param('var')) {
        overview();detail();
#}else {overview()}

print end_html;
exit 0;

#######################
# The Overview Output #
#######################
sub overview {
print "<div id=\"overview_wrapper\"><h1>Gene Structure</h1>";
print "<div id=\"overview\">\n";

my $length=0;
my $current = $RefSeq->get_annotation(0,2);

my $start=1;

for(my $i = $start-1; $i < $RefSeq->get_length; $i++) {

        if($RefSeq->get_annotation($i,2) eq $current) {
                $length++;
        } else {
                my $height = (($length / $RefSeq->get_length) * 400);
                if($current eq '') {
                        print a({-href=>"gel.cgi?lower=$start&upper=$i",-title=>"$start to $i"},img({-src=>"$VVFolder/i/nc.gif",-alt=>'',-width=>'32px',-height=>$height.'px'}))."<br/>";
                } else {
                        print a({-href=>"gel.cgi?lower=$start&upper=$i",-title=>"$start to $i"},img({-src=>"$VVFolder/i/c.gif",-alt=>'',-width=>'32px',-height=>$height.'px'}))."<br/>";
                }
                $length = 1;
                $start = $i+1;
        }

        $current = $RefSeq->get_annotation($i,2);
}


my $height = (($length / $RefSeq->get_length) * 400);
my $end = $RefSeq->get_length;
if($current eq '') {
        print a({-href=>"gel.cgi?lower=$start&upper=$end",-title=>"$start to $end"},img({-src=>"$VVFolder/i/nc.gif",-alt=>'',-width=>'32px',-height=>$height.'px'}));
} else {
        print a({-href=>"gel.cgi?lower=$start&upper=$end",-title=>"$start to $end"},img({-src=>"$VVFolder/i/c.gif",-alt=>'',-width=>'32px',-height=>$height.'px'}));
}

print "</div>";
print "<div id=\"overview_legend\"><div class=\"top\"><span class=\"c\">&nbsp;</span> Coding Region<br/><span class=\"nc\">&nbsp;</span> Non-coding Region</div><div class=\"bottom\">Click on a segment to see detail</div></div>";
print "</div>";
}
#######################
# The Detailed Output #
#######################
sub detail {

#Get upper and lower bounds from user, otherwise use defaults
my ($upperbound,$lowerbound,$var);

if(defined param('upper')) {$upperbound = param('upper')}
else {$upperbound = $RefSeq->get_length};
if(defined param('lower')) {$lowerbound = param('lower')}
else {$lowerbound = 1};

#Get Variation Data
my $Variation = VVMutFetch::Fetch($options->get_value("DBcolumnname"),$options->get_value("DBProtname"),$options->get_value("DBtablename"));
#This turns off the "Being displayed now" flag on ALL variants
$Variation->master_switch(0);

if(defined param('var')) {
   $var = param('var');
   @namedVariant = $Variation->get_variation_by_name($var);

   $upperbound = $lowerbound = 0;

   if(defined $namedVariant[0][0]) {
      if(defined $namedVariant[0][3]) {
         if($namedVariant[0][3] eq 'c.') {
            $lowerbound = $RefSeq->HGVStoRealPos($namedVariant[0][0]);
         } else {
            $lowerbound = $namedVariant[0][0];
         }
      } else {
         $lowerbound = $namedVariant[0][0];
      }

      if(defined $namedVariant[0][2]) {
         if($namedVariant[0][2] eq 'c.') {
            $upperbound = $RefSeq->HGVStoRealPos($namedVariant[0][2]);
         }else {
            $upperbound = $namedVariant[0][2];
         }
      } else {
         $upperbound = $lowerbound;
      }

      if(($upperbound ne -1) && ($lowerbound ne -1)) {
         $upperbound = $upperbound +20;
         $lowerbound = $lowerbound -20;
      }
   }
}

if($upperbound > $RefSeq->get_length) {$upperbound = $RefSeq->get_length};
if($lowerbound < 1) {$lowerbound = 1};

#TOOLS
print qq~<div id="tools"><form action="gel.cgi" method="get">zoom: ~;
print "<a href=\"javascript:;\" onclick=\"change('main', 'one');\"><img src=\"".$VVFolder."/i/z1.gif\" alt=\"Max Zoom\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'two');\"><img src=\"".$VVFolder."/i/z2.gif\" alt=\"\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'three');\"><img src=\"".$VVFolder."/i/z3.gif\" alt=\"Medium Zoom\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'four');\"><img src=\"".$VVFolder."/i/z4.gif\" alt=\"\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'five');\"><img src=\"".$VVFolder."/i/z5.gif\" alt=\"Min Zoom\" /></a>";
print " | <a href=\"sequence.cgi?upper=".$upperbound."&amp;lower=".$lowerbound."\">Copy Sequence</a>";
print "<br/>range: <input size=\"4\" type=\"text\" name=\"lower\" value=\"" . $lowerbound . "\" /> to <input size=\"4\" type=\"text\" name=\"upper\" value=\"" . $upperbound . "\" />";
print qq~&nbsp;<button type="submit">Go</button></form>~;
print "view: <a href=\"varivis.cgi?lower=$lowerbound&amp;upper=$upperbound\">Standard View</a> | <a href=\"legend.cgi\" target=\"sub\">Legend</a></div>";

#SUBDOC
print qq~<div id="subdoc"><iframe src="" name="sub" width="500" height="300" scrolling="no" frameborder="0">[Your user agent does not support frames or is currently configured not to display frames. Frames are required to view the extended information in VariVis.]</iframe></div>~;

#Set up table
print qq~<div id="detail">\n<h1 style="padding-left:80px">"Gel" View</h1>\n<table id="main" class="three">\n~;

#Counter to keep track of Amino Acids
my $AACounter = -1;

#The loop that does all the work
for(my $counter = $lowerbound-1; $counter < $upperbound; $counter++) {

        my $Position = $RefSeq->get_annotation($counter,1);


        #Get the variation data for this position...
        my @tempVar = $Variation->get_variation($Position, $counter);


        #Declare an empty string to build each table row in and return at the end
        my $tempRow = "";

        #################
        my $A = "";
        my $T = "";
        my $C = "";
        my $G = "";
        my $D = "";
        my $Insert = "";
        my $Invert = "";

        my $ReferenceNucleotide = $RefSeq->get_sequence_by_position($counter);

        #Loop through the tempVar array as there may be more than one variant at each position
        for(my $j = 0; $j<=$#tempVar; $j++) {


                #Substitutions
                if($tempVar[$j][1] eq "S") {
                        if($tempVar[$j][5] eq "A") {$A .= $tempVar[$j][6]}
                        elsif ($tempVar[$j][5] eq "T") {$T = $tempVar[$j][6]}
                        elsif ($tempVar[$j][5] eq "C") {$C = $tempVar[$j][6]}
                        elsif ($tempVar[$j][5] eq "G") {$G = $tempVar[$j][6]}}
                #Deletions
                elsif($tempVar[$j][1] eq "D") {$D .= $tempVar[$j][6] . "|"}
                #Duplications
                elsif($tempVar[$j][1] eq "U") {
                        if($tempVar[$j][2] eq $RefSeq->get_annotation($counter,1)){$Insert .= $tempVar[$j][6] . "|"}}
                #Insertions
                elsif($tempVar[$j][1] eq "I") {
                        if($tempVar[$j][0] eq $RefSeq->get_annotation($counter,1)){$Insert .= $tempVar[$j][6] . "|"}}
                #InDels
                elsif($tempVar[$j][1] eq "N") {
                        $D .= $tempVar[$j][6] . "|";
                        if($tempVar[$j][0] eq $RefSeq->get_annotation($counter,1)){$Insert .= $tempVar[$j][6] . "|"}}
                elsif($tempVar[$j][1] eq "V") {
                        if($tempVar[$j][0] eq $RefSeq->get_annotation($counter,1)){$tempRow .= "<tr><td class=\"num\"><a title=\"".$tempVar[$j][6]."\" href=\"subdoc.cgi?var=" . $tempVar[$j][6] . "\" target=\"sub\">&raquo;</a></td><td class=\"i\" colspan=\"6\"></td></tr>";}
                        if($tempVar[$j][2] eq $RefSeq->get_annotation($counter,1)){$Invert .= "<tr><td class=\"num\"><a title=\"".$tempVar[$j][6]."\" href=\"subdoc.cgi?var=" . $tempVar[$j][6] . "\" target=\"sub\">&laquo;</a></td><td class=\"i\" colspan=\"6\"></td></tr>"}}
        }

        #First thing is the Table Row tag (<tr>)
        #The style class of which is dependant on whether we're in a coding or non-coding region
        #However, if the user has turned off intron display, then we need to exit the whole sub early
        if($RefSeq->get_annotation($counter,2) eq "C") {
                $tempRow .= "<tr class=\"c\">";
        } else {
                $tempRow .= "<tr class=\"n\">";
        }

        #Define a 'show' variable so we can only put specific numbering in
        my $show = -1;
        my $real_num = $counter + 1;

        #This pattern match gets the digit and not the symbol to allow numeric operators to work
        #It also just gets the Intron base number and not the exon identifier
        #We get the remainder of a division by 5 so we can display every 5th number
        #However, we also display anything that is 1 i.e. -1, 1, 1+1,1-1 and *1
        if($RefSeq->get_annotation($counter,1) =~ /^(\d+)$/) {
                if($1 == 1) {$show=0}else{$show = $1 % 5}
        }elsif($RefSeq->get_annotation($counter,1) =~ /^[*-](\d+)$/) {
                if($1 == 1) {$show=0}else{$show = $1 % 5}
        }elsif($RefSeq->get_annotation($counter,1) =~ /^\d+[+-](\d+)$/) {
                if($1 == 1) {$show=0}else{$show = $1 % 5}
        }

        #So if show is zero, either because the number is a one or
        #the division by 5 returned no remainder (the number is a multiple of five,
        #we output the number. In all other cases, an empty cell
        if($show == 0) {
                $tempRow .= "<td class=\"num\">(".$real_num.") ".$RefSeq->get_annotation($counter,1)."</td>";
        } else {
                $tempRow .= "<td class=\"num\"></td>"
        }

        #Now we put in the 4 Bases A,T,C,G
        #A
        if($ReferenceNucleotide eq "A") {$tempRow .= "<td class=\"ref\">A</td>"}
        elsif ($A ne "") {
                $tempRow .= "<td class=\"m\"><a href=\"subdoc.cgi?var=$A\" title=\"$A\" target=\"sub\">A</a></td>";
        } else {$tempRow .= "<td class=\"b\">A</td>"}

        #T
        if($ReferenceNucleotide eq "T") {$tempRow .= "<td class=\"ref\">T</td>"}
        elsif ($T ne "") {
                $tempRow .= "<td class=\"m\"><a href=\"subdoc.cgi?var=$T\" title=\"$T\" target=\"sub\">T</a></td>";
        } else {$tempRow .= "<td class=\"b\">T</td>"}

        #C
        if($ReferenceNucleotide eq "C") {$tempRow .= "<td class=\"ref\">C</td>"}
        elsif ($C ne "") {
                $tempRow .= "<td class=\"m\"><a href=\"subdoc.cgi?var=$C\" title=\"$C\" target=\"sub\">C</a></td>";
        } else {$tempRow .= "<td class=\"b\">C</td>"}

        #G
        if($ReferenceNucleotide eq "G") {$tempRow .= "<td class=\"ref\">G</td>"}
        elsif ($G ne "") {
                $tempRow .= "<td class=\"m\"><a href=\"subdoc.cgi?var=$G\" title=\"$G\" target=\"sub\">G</a></td>";
        } else {$tempRow .= "<td class=\"b\">G</td>"}

        #-
        if($D ne "") {
                chop $D;
                $tempRow .= "<td class=\"m\"><a href=\"subdoc.cgi?var=$D\" target=\"sub\" title=\"$D\">-</a></td>"
        } else {$tempRow .= "<td class=\"b\">-</td>"}

        #+
        if($Insert ne "") {
                chop $Insert;
                $tempRow .= "<td class=\"m\"><a href=\"subdoc.cgi?var=$Insert\" target=\"sub\" title=\"$Insert\">+</a></td>"
        } else {$tempRow .= "<td class=\"b\">+</td>"}
        

        #Promoter annotation
        if($RefSeq->get_annotation($counter,4) eq "P") {
                $tempRow .= "<td class=\"pr\" title=\"Promoter\"></td>";
        } else {
                $tempRow .= "<td class=\"nm\"></td>";
        }
        
        #5' UTR annotation
        if($RefSeq->get_annotation($counter,5) eq "5") {
                $tempRow .= "<td class=\"f\" title=\"5' UTR\"></td>";
        } else {
                $tempRow .= "<td class=\"nm\"></td>";
        }
        
        #3' UTR annotation
        if($RefSeq->get_annotation($counter,6) eq "3") {
                $tempRow .= "<td class=\"t\" title=\"3' UTR\"></td>";
        } else {
                $tempRow .= "<td class=\"nm\"></td>";
        }
        
        #Poly A annotation
        if($RefSeq->get_annotation($counter,7) eq "A") {
                $tempRow .= "<td class=\"a\" title=\"Poly A Signal\"></td>";
        } else {
                $tempRow .= "<td class=\"nm\"></td>";
        }

        #mRNA annotation
        if($RefSeq->get_annotation($counter,3) eq "M") {
                $tempRow .= "<td class=\"r\ title=\"mRNA\"></td>";
        } else {
                $tempRow .= "<td class=\"nm\"></td>";
        }



        #AMINO ACID TRACK
        $tempRow .= "<td class=\"p\">";
        if($RefSeq->get_annotation($counter,2) eq "C") {
                $AACounter = floor(($RefSeq->get_annotation($counter,1) - $RefSeq->get_digit_codon_start)/3);

                #Get the AA at the 1st position in each codon
                if(($RefSeq->get_annotation($counter,1) - $RefSeq->get_digit_codon_start) % 3 == 0) {
                        $tempRow .= $RefSeq->get_translation_by_position($AACounter);

                        #Protein level changes
                        $tempRow .= $Variation->get_protein_variation($AACounter+1,' ','sub');
                }
        }
        $tempRow .= "</td>";
        #End the row
        $tempRow .= "</tr>\n";
        #Put in end of Inversion range if required
        if($Invert ne "") {$tempRow .= $Invert}

        print $tempRow;
}

#Reset the "Being displayed now" flag on ALL variants
#All the flags should be off at this stage, but just to be on the safe side
$Variation->master_switch(0);

###############################
# Back to the page formatting #
###############################
print "</table>";
print '<div style="border-top:1px solid silver;">' . $program->get('info') . ' version ' . $program->get('version') . '</div>';
print "</div>";
}
