package VVVar;

use strict;
use warnings;

#Class Data and Methods
{
  my %_attributes = (
    _variations => [],
    _protein_variations => [],
    _p_number => 0,
    _number => 0
  );
  
  
  
  
sub _all_attributes {
    keys %_attributes;
}

sub _attribute_value {
    my($self,$attribute) = @_;
    $_attributes{$attribute};
}


sub new {
    my ($class, %arg) = @_;
    
    #create a new object
    my $self = bless {}, $class;
    
    #Set the attributes for given arguments
    foreach my $attribute ($self->_all_attributes) {

        #Strip the _ off the attribute name to get argument
        my($argument) = ($attribute =~ /^_(.*)/);

        
        #Set to default argument
        $self->{$attribute} = $self->_attribute_value($attribute);
        
        #Replace default with given argument
        if (exists $arg{$argument}) {
                if($argument eq 'variations') {
                        die "Cannot set in this method";
                }
                $self->{$attribute} = $arg{$argument};
        }
    }
    return $self;
}

sub add_variation {
        my($self,$var)=@_;
        
   if($var) {
        
        my @variant = [];
        
        #some databases put whitespace around the data
        #so we strip it off
        $var =~ s/^\s+//;
	$var =~ s/\s+$//;
        
        #Here we have some pattern matches to determine
        #what TYPE of variant we're dealing with
        #and then populate a temp array with the subset data we need
        
        # SUBSTITUTION EVENT
        if($var =~ m/^([cg]\.)?(-?\*?\d+[-+]?\d*)([ATCG])>([ATCG])$/i) {
                $variant[1] = "S";
                $variant[3] = $1 if $1;
                $variant[0] = $2;
                $variant[4] = $3;
                $variant[5] = $4;
                $variant[6] = $var;}
                
        # DELETION EVENT
        elsif ($var =~ m/^([cg]\.)?(-?\*?\d+[-+]?\d*)_(-?\*?\d+[-+]?\d*)del([ATCG]+)?$/i) {
                $variant[1] = "D";
                $variant[3] = $1 if $1;
                $variant[0] = $2;
                $variant[2] = $3;
                $variant[5] = $4 if $4;
                $variant[6] = $var;}

        # DUPLICATION EVENT
        elsif ($var =~ m/^([cg]\.)?(-?\*?\d+[-+]?\d*)_(-?\*?\d+[-+]?\d*)dup([ATCG\d]+)?$/i) {
                $variant[1] = "U";
                $variant[3] = $1 if $1;
                $variant[0] = $2;
                $variant[2] = $3;
                $variant[4] = $4 if $4;
                $variant[6] = $var;}

        # INSERTION EVENT
        elsif ($var =~ m/^([cg]\.)?(-?\*?\d+[-+]?\d*)_(-?\*?\d+[-+]?\d*)ins([ATCG]+)?$/i) {
                $variant[1] = "I";
                $variant[3] = $1 if $1;
                $variant[0] = $2;
                $variant[2] = $3;
                $variant[4] = $4 if $4;
                $variant[6] = $var;}

        # DELETION/INSERTION EVENT
        elsif ($var =~ m/^([cg]\.)?(-?\*?\d+[-+]?\d*)_(-?\*?\d+[-+]?\d*)del([ATCG]+)?ins([ATCG]+)$/i) {
                $variant[1] = "N";
                $variant[3] = $1 if $1;
                $variant[0] = $2;
                $variant[2] = $3;
                $variant[4] = $4 if $4;
                $variant[5] = $5;
                $variant[6] = $var;}

        # INVERSION EVENT
        elsif ($var =~ m/^([cg]\.)?(-?\*?\d+[-+]?\d*)_(-?\*?\d+[-+]?\d*)inv(\d+)?$/i) {
                $variant[1] = "V";
                $variant[3] = $1 if $1;
                $variant[0] = $2;
                $variant[2] = $3;
                $variant[4] = $4 if $4;
                $variant[6] = $var;}
    

        push(@{$self->{_variations}},[@variant]);
        $self->{_number}++;
   }
}


sub add_protein_variation {
        my($self,$p_var)=@_;

   if($p_var){

        my @p_variant = [];

        #some databases put whitespace around the data
        #so we strip it off
        $p_var =~ s/^\s+//;
	$p_var =~ s/\s+$//;
	
        #TEST FOR DUPLICATES
        my $duplicate_flag = 0;
        for(my $dup_counter = 0; $dup_counter < $self->{_p_number}; $dup_counter++) {
             if(exists($self->{_protein_variations}[$dup_counter][6])) {
                  if($self->{_protein_variations}[$dup_counter][6] eq $p_var) {
                  $duplicate_flag = 1;
                  }
             }
        }
        
        if($duplicate_flag == 0) {

           #Here we have some pattern matches to determine
           #what TYPE of variant we're dealing with
           #and then populate a temp array with the subset data we need

           # SUBSTITUTION EVENT
           if($p_var =~ m/^(p\.)?(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+)(G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR|x|\?)(ext(X||G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|TCYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)-?\d+)?$/i) {
                $p_variant[1] = "S";
                $p_variant[3] = $1 if $1;
                $p_variant[0] = $3;
                $p_variant[4] = $2;
                if(length($4) == 3) {$p_variant[5] = $self->_convert($4);} else {$p_variant[5] = $4;};
                $p_variant[6] = $p_var;}
           #No protein detected or protein not analysed
           elsif($p_var =~ m/^(p\.)?(0|(=))?(\?)?$/i) {
                $p_variant[1] = "0";
                $p_variant[3] = $1 if $1;
                $p_variant[0] = 1;
                $p_variant[5] = 0;
                $p_variant[6] = $p_var;}
           # DELETIONS
           elsif($p_var =~ m/^(p\.)?(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+)(_(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+))?(del)$/i) {
                $p_variant[1] = "D";
                $p_variant[3] = $1 if $1;
                $p_variant[0] = $3;
                $p_variant[2] = $6 if $6;
                $p_variant[4] = $2;
                $p_variant[5] = '-';
                $p_variant[6] = $p_var;}
           # DUPLICATION
           elsif($p_var =~ m/^(p\.)?(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+)(_(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+))?(dup)$/i) {
                $p_variant[1] = "U";
                $p_variant[3] = $1 if $1;
                if($6) {$p_variant[0] = $6;} else {$p_variant[0]=$3};
                $p_variant[4] = $2;
                $p_variant[5] = '*';
                $p_variant[6] = $p_var;}
           # INSERTION
           elsif($p_var =~ m/^(p\.)?(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+)(_(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+))(ins)/i) {
                $p_variant[1] = "I";
                $p_variant[3] = $1 if $1;
                $p_variant[0] = $3;
                $p_variant[4] = $2;
                $p_variant[5] = '*';
                $p_variant[6] = $p_var;}
           # INDEL
           elsif($p_var =~ m/^(p\.)?(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+)(_(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)(\d+))(delins)(X|G|P|A|V|L|I|M|C|F|Y|W|H|K|R|Q|N|E|D|S|T|CYS|ILE|SER|GLN|MET|ASN|PRO|LYS|ASP|THR|PHE|ALA|GLY|HIS|LEU|ARG|TRP|VAL|GLU|TYR)+$/i) {
                $p_variant[1] = "N";
                $p_variant[3] = $1 if $1;
                $p_variant[2] = $6;
                $p_variant[0] = $3;
                $p_variant[4] = $2;
                $p_variant[5] = '-';
                $p_variant[6] = $p_var;}
                
           push(@{$self->{_protein_variations}},[@p_variant]);
           $self->{_p_number}++;
        }
   }
}

sub get_protein_variation {
        my($self,$position,$sep,$target) = @_;
        
        my $results;

        for(my $counter = 0; $counter < $self->{_p_number}; $counter++) {

                #In order to display variants that act over a range,
                #we have a flag that tells the program to "keep displaying
                #this variant until we reach the end position"
                #
                #It's only needed on ranged variants, hence testing [][2].
                if(defined $self->{_protein_variations}[$counter][2]) {

                        #if we're at the start of a ranged variant, turn on the flag
                        if($self->{_protein_variations}[$counter][0] eq $position && $self->{_protein_variations}[$counter][7] == 0) {
                                $self->{_protein_variations}[$counter][7] = 1;

                        #if we're at the end, turn off the flag - but make sure the last one get's pushed!!!
                        #We also handle indels here
                        } elsif($self->{_protein_variations}[$counter][2] eq $position && $self->{_protein_variations}[$counter][7] == 1) {
                                $self->{_protein_variations}[$counter][7] = 0;
                                if($self->{_protein_variations}[$counter][1] eq 'N') {
                                $results .= $sep.'<a target="'.$target.'" href="subdoc.cgi?var='.$self->{_protein_variations}[$counter][6].'" title="'.$self->{_protein_variations}[$counter][6].'">*</a>';
                                } else {
                                $results .= $sep.'<a target="'.$target.'" href="subdoc.cgi?var='.$self->{_protein_variations}[$counter][6].'" title="'.$self->{_protein_variations}[$counter][6].'">' . $self->{_protein_variations}[$counter][5].'</a>';
                                }
                        }

                        #If the flag is on, push results
                        if($self->{_protein_variations}[$counter][7] == 1) {
                                $results .= $sep.'<a target="'.$target.'" href="subdoc.cgi?var='.$self->{_protein_variations}[$counter][6].'" title="'.$self->{_protein_variations}[$counter][6].'">' . $self->{_protein_variations}[$counter][5].'</a>';
                        }

                } elsif($self->{_protein_variations}[$counter][0] eq $position) {
                        $results .= $sep.'<a target="'.$target.'" href="subdoc.cgi?var='.$self->{_protein_variations}[$counter][6].'" title="'.$self->{_protein_variations}[$counter][6].'">' . $self->{_protein_variations}[$counter][5].'</a>';
                }
        }

        return $results;
        
}

sub get_variation_by_name {
   my($self,$name) = @_;
   
   my @results;
   
   for(my $counter = 0; $counter < $self->{_number}; $counter++) {
      if($self->{_variations}[$counter][6] eq $name) {
         push(@results,$self->{_variations}[$counter]);
      }
   }
   return @results;
}


sub get_variation {
        my($self,$c_position, $g_position)=@_;

        #We're going to return an array of variations at each position
        #so we define one here
        my @results;
        my $position;
        
        for(my $counter = 0; $counter < $self->{_number}; $counter++) {

              if(defined $self->{_variations}[$counter][3]) {
                 if($self->{_variations}[$counter][3] eq 'c.') {
                    $position = $c_position;
                 } elsif($self->{_variations}[$counter][3] eq 'g.') {
                    $position = $g_position;
                 } else {
                    $position = 0;
                 }
              }else {
                 $position = 0;
              }

        
               #In order to display variants that act over a range,
               #we have a flag that tells the program to "keep displaying
               #this variant until we reach the end position"
               #
               #It's only needed on ranged variants, hence testing [][2].
               if(defined $self->{_variations}[$counter][2]) {

                       #if we're at the start of a ranged variant, turn on the flag
                       if($self->{_variations}[$counter][0] eq $position && $self->{_variations}[$counter][7] == 0) {
                              $self->{_variations}[$counter][7] = 1;

                       #if we're at the end, turn off the flag - but make sure the last one get's pushed!!!
                       } elsif($self->{_variations}[$counter][2] eq $position && $self->{_variations}[$counter][7] == 1) {
                               $self->{_variations}[$counter][7] = 0;
                               push(@results,$self->{_variations}[$counter]);
                       }

                       #If the flag is on, push results
                       if($self->{_variations}[$counter][7] == 1) {
                               push(@results,$self->{_variations}[$counter]);
                       }

               } elsif($self->{_variations}[$counter][0] eq $position) {
                       push(@results,$self->{_variations}[$counter]);
               }
        }
        
        return @results;
}

sub master_switch {
        my($self, $flag) = @_;
        
        if($flag < 0 && $flag > 1) {return 0}
        
        for(my $counter = 0; $counter < $self->{_number}; $counter++) {
                $self->{_variations}[$counter][7] = $flag;
        }
        
        for(my $master_counter = 0; $master_counter < $self->{_p_number}; $master_counter++) {
                $self->{_protein_variations}[$master_counter][7] = $flag;
        }
}


sub _convert {
        my($self,$aa3code)=@_;
        
        my %codes = ('GLY' => 'G',
                     'PRO' => 'P',
                     'ALA' => 'A',
                     'VAL' => 'V',
                     'LEU' => 'L',
                     'ILE' => 'I',
                     'MET' => 'M',
                     'CYS' => 'C',
                     'PHE' => 'F',
                     'TYR' => 'Y',
                     'TRP' => 'W',
                     'HIS' => 'H',
                     'LYS' => 'K',
                     'ARG' => 'R',
                     'GLN' => 'Q',
                     'ASN' => 'N',
                     'GLU' => 'E',
                     'ASP' => 'D',
                     'SER' => 'S',
                     'THR' => 'T'
        );
        $aa3code = uc $aa3code;
        if(exists $codes{$aa3code}) {
                return $codes{$aa3code};
        } else {return $aa3code;}

}

}
1;

