package VVMutFetch;

use strict;
use warnings;
use VVVar;
use VVdbi;

sub Fetch {
        my($dnaColumn, $protColumn, $Table) = @_;

        my $ObjRef = VVVar->new();
        
        if(!$Table) {$Table = 'default';}
        
        my @Variations = VVdbi::Query("SELECT $dnaColumn FROM $Table");
        
        my $size = @Variations;
        
        for(my $i = 0; $i < $size; $i++) {
                $ObjRef->add_variation($Variations[$i]{$dnaColumn});
        }
        
        my @proteins = VVdbi::Query("SELECT $protColumn FROM $Table");
        my $p_size = @proteins;

        for(my $j = 0; $j < $p_size; $j++) {
                $ObjRef->add_protein_variation($proteins[$j]{$protColumn});
        }
        
        return $ObjRef;
}
1;
