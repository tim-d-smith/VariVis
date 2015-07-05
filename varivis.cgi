#!C:/Perl/bin/perl

#VariVis custom classes
use VVSeq;
use VVVar;
use VVIni;
use Bio::Perl;

#VariVis Libraries
use VVRefFetch;
use VVMutFetch;
use program;
my $program = program->new();

#Perl Settings
#use strict;
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

print start_html(-head=>[Link({-rel=>"stylesheet", -type=>"text/css", -href=>"$VVFolder/varivis.css"}),script({-type=>'text/javascript',-src=>"$VVFolder/j/varivis.js"},undef),script({-type=>"text/javascript"},"window.onload=function(){enableTooltips('main')};this.focus()")],-title=>"$GeneName - Standard View");

#Get Reference Sequence Data
my $RefSeq = VVRefFetch::Fetch($options->get_value("gene"),$options->get_value("refloc"),$options->get_value("acc"),$options->get_value("vvfolderpath"),$options->get_value("formatloc"),$options->get_value("locpath"));


##############################
# Decide which output to use #
##############################

if(defined param('upper') || defined param('var')) {
overview();detail();
}else {overview()}

print end_html;
exit 0;

#######################
# The Overview Output #
#######################
sub overview {
print "<div id=\"overview_wrapper\">";
print "<div id=\"width_restraint\"><div id=\"overview_legend\"><div class=\"top\"><span class=\"c\">&nbsp;</span> Coding Region<br/><span class=\"nc\">&nbsp;</span> Non-coding Region</div><div class=\"bottom\">Click on a segment to see detail</div></div>";
print "<h1>Gene Structure</h1>";
print "<div id=\"overview\">\n";

my $length=0;
my $current = $RefSeq->get_annotation(0,2);

my $start=1;

for(my $i = $start-1; $i < $RefSeq->get_length; $i++) {

        if($RefSeq->get_annotation($i,2) eq $current) {
                $length++;
        } else {
                my $width = (($length / $RefSeq->get_length) * 400);
                if($current eq '') {
                        print a({-href=>"varivis.cgi?lower=$start&upper=$i",-title=>"$start to $i"},img({-src=>"$VVFolder/i/nc.gif",-alt=>'',-height=>'32px',-width=>$width.'px'}));
                } else {
                        print a({-href=>"varivis.cgi?lower=$start&upper=$i",-title=>"$start to $i"},img({-src=>"$VVFolder/i/c.gif",-alt=>'',-height=>'32px',-width=>$width.'px'}));
                }
                $length = 1;
                $start = $i+1;
        }

        $current = $RefSeq->get_annotation($i,2);
}


my $width = (($length / $RefSeq->get_length) * 400);
my $end = $RefSeq->get_length;
if($current eq '') {
        print a({-href=>"varivis.cgi?lower=$start&upper=$end",-title=>"$start to $end"},img({-src=>"$VVFolder/i/nc.gif",-alt=>'',-height=>'32px',-width=>$width.'px'}));
} else {
        print a({-href=>"varivis.cgi?lower=$start&upper=$end",-title=>"$start to $end"},img({-src=>"$VVFolder/i/c.gif",-alt=>'',-height=>'32px',-width=>$width.'px'}));
}


print "</div></div></div>"
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

print qq~<div id="detail"><h1>Standard View</h1>~;
#TOOLS
print qq~<div id="tools"><form action="varivis.cgi" method="get">zoom: ~;
print "<a href=\"javascript:;\" onclick=\"change('main', 'one');\"><img src=\"".$VVFolder."/i/z1.gif\" alt=\"Max Zoom\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'two');\"><img src=\"".$VVFolder."/i/z2.gif\" alt=\"\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'three');\"><img src=\"".$VVFolder."/i/z3.gif\" alt=\"Medium Zoom\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'four');\"><img src=\"".$VVFolder."/i/z4.gif\" alt=\"\" /></a> <a href=\"javascript:;\" onclick=\"change('main', 'five');\"><img src=\"".$VVFolder."/i/z5.gif\" alt=\"Min Zoom\" /></a>";
print " | <a href=\"sequence.cgi?upper=".$upperbound."&amp;lower=".$lowerbound."\">Copy Sequence</a>";
print "<br/>range: <input size=\"4\" type=\"text\" name=\"lower\" value=\"" . $lowerbound . "\" /> to <input size=\"4\" type=\"text\" name=\"upper\" value=\"" . $upperbound . "\" />";
print qq~&nbsp;<button type="submit">Go</button></form>~;
print "view: <a href=\"gel.cgi?lower=$lowerbound&amp;upper=$upperbound\">'Gel' View</a> | <a href=\"legend.cgi\" target=\"sub2\">Legend</a></div>";

#SUBDOC
print qq~<div id="subdoc"><iframe src="" name="sub2" width="280" height="300" scrolling="no" frameborder="0">[Your user agent does not support frames or is currently configured not to display frames. Frames are required to view the extended information in VariVis.]</iframe></div>~;

#Set up table
print "<table id=\"main\" class=\"three\">";

my $row_length = 40;
my $row_start = $lowerbound - 1;
my $row_end = $row_start + $row_length - 1;
my $num_rows = ($upperbound - $row_start) / $row_length;
use POSIX;
$num_rows = ceil($num_rows);
my $AACounter = -1;

for(my $row_count = 1; $row_count <= $num_rows; $row_count++) {

        #VARIANT TRACK - also does AA Variants
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                
                my $Position = $RefSeq->get_annotation($i,1);
                
                #Get the variation data for this position...
                my @tempVar = $Variation->get_variation($Position, $i);
                my $A = "";
                my $T = "";
                my $C = "";
                my $G = "";
                my $D = "";
                my $Insert = "";
                my $Invert = "";

                #Loop through the tempVar array as there may be more than one variant at each position
                for(my $j = 0; $j<=$#tempVar; $j++) {
                        #substitutions
                        if($tempVar[$j][1] eq "S") {
                                if($tempVar[$j][5] eq "A") {$A .= $tempVar[$j][6]}
                                elsif ($tempVar[$j][5] eq "T") {$T = $tempVar[$j][6]}
                                elsif ($tempVar[$j][5] eq "C") {$C = $tempVar[$j][6]}
                                elsif ($tempVar[$j][5] eq "G") {$G = $tempVar[$j][6]}}
                        #Deletions
                        elsif($tempVar[$j][1] eq "D") {$D .= $tempVar[$j][6] . "|"}
                        #Duplications
                        elsif($tempVar[$j][1] eq "U") {
                                if($tempVar[$j][2] eq $RefSeq->get_annotation($i,1)){$Insert .= $tempVar[$j][6] . "|"}}
                        #Insertions
                        elsif($tempVar[$j][1] eq "I") {
                                if($tempVar[$j][0] eq $RefSeq->get_annotation($i,1)){$Insert .= $tempVar[$j][6] . "|"}}
                        #InDels
                        elsif($tempVar[$j][1] eq "N") {
                                $D .= $tempVar[$j][6] . "|";
                                if($tempVar[$j][0] eq $RefSeq->get_annotation($i,1)){$Insert .= $tempVar[$j][6] . "|"}}
                        elsif($tempVar[$j][1] eq "V") {
                                if($tempVar[$j][0] eq $RefSeq->get_annotation($i,1)){$Invert .= $tempVar[$j][6] . "|"}
                                if($tempVar[$j][2] eq $RefSeq->get_annotation($i,1)){$Invert .= $tempVar[$j][6] . "|"}
                        }
                }
                print "<td class=\"m\">";
                
                #A
                if ($A) {
                        print "<a href=\"subdoc.cgi?var=$A\" title=\"$A\" target=\"sub2\">A</a><br/>";
                }

                #T
                if ($T) {
                        print "<a href=\"subdoc.cgi?var=$T\" title=\"$T\" target=\"sub2\">T</a><br/>";
                }
                
                #C
                if ($C) {
                        print "<a href=\"subdoc.cgi?var=$C\" title=\"$C\" target=\"sub2\">C</a><br/>";
                }

                #G
                if ($G) {
                        print "<a href=\"subdoc.cgi?var=$G\" title=\"$G\" target=\"sub2\">G</a><br/>";
                }
                
                #D
                if ($D) {
                        chop $D;
                        print "<a href=\"subdoc.cgi?var=$D\" target=\"sub2\" title=\"$D\">-</a><br/>";
                }

                chop $Invert; print "<a title=\"$Invert\" href=\"subdoc.cgi?var=$Invert\" target=\"sub2\">|</a><br/>" if $Invert;

                #Insert
                if ($Insert) {
                        chop $Insert;
                        print "<a href=\"subdoc.cgi?var=$Insert\" target=\"sub2\" title=\"$Insert\">+</a><br/>";
                }
                print '</td>';
        }
        print "<td class=\"n\"></td></tr>";




        #SEQUENCE TRACK with Numbering
        print "<tr>";
        my $real_num = $row_start + 1;
        print "<td class=\"num_l\">".$RefSeq->get_annotation($row_start,1)."<br/>($real_num)</td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                $real_num = $i;
                if ($i >= $upperbound) {last;}
                print "<td class=\"b\">".$RefSeq->get_sequence_by_position($i)."</td>";
                $real_num = $i+1;

        }
        if($row_end > $upperbound) {$row_end = $upperbound -1};
        print "<td colspan=\"10\" class=\"num_r\">".$RefSeq->get_annotation($row_end,1)."<br/>($real_num)</td>";
        print "</tr>";
        
        #CDS TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                if ($RefSeq->get_annotation($i,2) eq "C") {print "<td class=\"c\"></td>";}
                else {print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";

        #PROMOTER TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                if ($RefSeq->get_annotation($i,4) eq "P") {print "<td class=\"pr\" title=\"Promoter\"></td>";}
                else {print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";

        #5'UTR TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                if ($RefSeq->get_annotation($i,5) eq "5") {print "<td class=\"f\" title=\"5' UTR\"></td>";}
                else {print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";
        #3'UTR TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                if ($RefSeq->get_annotation($i,6) eq "3") {print "<td class=\"t\" title=\"3' UTR\"></td>";}
                else {print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";
        #Poly_A TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                if ($RefSeq->get_annotation($i,7) eq "A") {print "<td class=\"a\" title=\"Poly A Signal\"></td>";}
                else {print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";

        #mRNA TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}
                if ($RefSeq->get_annotation($i,3) eq "M") {print "<td class=\"r\"></td>";}
                else {print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";
        
        #AMINO ACID TRACK
        print "<tr><td class=\"n\"></td>";
        for (my $i = $row_start; $i <= $row_end; $i++) {
                if ($i >= $upperbound) {last;}

                if($RefSeq->get_annotation($i,2) eq "C") {
                                $AACounter = floor(($RefSeq->get_annotation($i,1) - $RefSeq->get_digit_codon_start)/3);

                        #Get the AA at the 1st position in each codon
                        if(($RefSeq->get_annotation($i,1) - $RefSeq->get_digit_codon_start) % 3 == 0) {
                                print "<td class=\"p\">".$RefSeq->get_translation_by_position($AACounter);

                                #Protein level changes
                                print $Variation->get_protein_variation($AACounter+1,'<br/>','sub2');

                                print "</td>";
                        } else { print "<td class=\"n\"></td>";}
                } else { print "<td class=\"n\"></td>";}
        }
        print "<td class=\"n\"></td></tr>";
        
        
        $row_start = $row_end + 1;
        $row_end = $row_start + $row_length - 1;
        
        print "<tr><td colspan=\"$row_length\" class=\"spacer\">&nbsp;</td></tr>";
}
###############################
# Back to the page formatting #
###############################
print "</table>";
print "</div>";
print '<div style="border-top:1px solid silver;">' . $program->get('info') . ' version ' . $program->get('version') . '</div>';
}
