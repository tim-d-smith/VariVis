#!C:/Perl/bin/perl

#Perl Settings
use strict;
use warnings;
use VVIni;

#CGI
use CGI qw(:cgi-lib :standard);

###################################
my $options = VVIni->new(filename=>'varivis.ini') || die "Could not access configuration file. Try running install again. Stopped";
my $VVFolder = $options->get_value("vvfolderpath") || die "Could not access configuration file. Try running install again. Stopped";

#Make sure we can output to browser
print header();
print start_html(-head=>[Link({-rel=>"stylesheet", -type=>"text/css", -href=>"$VVFolder/gel.css"})]);

print qq~
<h1>Legend</h1>
<table class="three" style="text-align:left">
   <tbody>
      <tr>
         <td class="pr">&nbsp;</td>
         <td style="width:2em;">&nbsp;</td>
         <td style="color:black">Promoter Sequence</td>
      </tr>
      <tr>
         <td class="r">&nbsp;</td>
         <td style="width:2em;">&nbsp;</td>
         <td style="color:black">mRNA Sequence</td>
      </tr>
      <tr>
         <td class="f">&nbsp;</td>
         <td style="width:2em;">&nbsp;</td>
         <td style="color:black">5' Untranslated Region</td>
      </tr>
      <tr>
         <td class="t">&nbsp;</td>
         <td style="width:2em;">&nbsp;</td>
         <td style="color:black">3' Untranslated Region</td>
      </tr>
      <tr>
         <td class="a">&nbsp;</td>
         <td style="width:2em;">&nbsp;</td>
         <td style="color:black">Poly A Signal</td>
      </tr>
</tbody>
</table>

~;

print end_html;

