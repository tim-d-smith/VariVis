package VVSeq;

use strict;
use warnings;

#Class Data and Methods
{
  my %_attributes = (
        #SEQUENCE INFORMATION
    _sequence => [],
    _genename => '',
    _start => 1,
    _length => 0,
    _codon_start => 1,
    _digit_codon_start => 1,
    _product => '',
    _translation => [],
    _CDSFeatures => [],
    _map => '',
    _href => '',
    _species => '',
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
    
    #Gene Name must be given as argument
    unless($arg{genename}) {
        die "No Gene Name given";
    }
    
    #Set the attributes for given arguments
    foreach my $attribute ($self->_all_attributes) {

        #Strip the _ off the attribute name to get argument
        my($argument) = ($attribute =~ /^_(.*)/);

        
        #Set to default argument
        $self->{$attribute} = $self->_attribute_value($attribute);
        
        #Replace default with given argument
        if (exists $arg{$argument}) {
            if($argument eq 'sequence' || $argument eq 'length') {
                die "Cannot set in this method";
            }
            $self->{$attribute} = $arg{$argument};
        }
    }
    return $self;
}


sub get_length {
    my($self)=@_;
    $self->{_length};
}

sub get_genename {
    my($self) = @_;
    $self->{_genename};
}

sub set_species {
    my($self,$species) = @_;
    $self->{_species} = $species;
}

sub get_species {
    my($self) = @_;
    $self->{_species};
}

sub set_sequence {
    my($self,$inseq)=@_;
    $self->{_length}=length($inseq);

    for(my $a=0; $a < $self->{_length}; $a++) {
        my $subseq = substr($inseq,$a,1);
        $self->{_sequence}[$a]=[$subseq];
    }
}

sub get_sequence_by_position {
    my($self,$position) = @_;
    $self->{_sequence}[$position][0] if defined $self->{_sequence}[$position][0];
}

sub set_translation {
    my($self,$translation)=@_;

    for(my $a=0; $a < length($translation); $a++) {
        my $subseq = substr($translation,$a,1);
        $self->{_translation}[$a]=$subseq;
    }
}

sub get_translation_by_position {
    my($self,$position) = @_;
    $self->{_translation}[$position] if defined $self->{_translation}[$position];
}

sub set_start {
    my($self,$start)=@_;
    $self->{_start}=$start;
}

sub HGVStoRealPos {
   my($self,$HGVSpos)=@_;

   my $realpos = -1;
   for(my $q=0; $q<$self->{_length}; $q++) {
      if($self->{_sequence}[$q][1] eq $HGVSpos) {$realpos = $q +1;}
   }
   return $realpos;
}

sub get_start {
    my($self)=@_;
    $self->{_start};
}

sub set_map {
    my($self,$map)=@_;
    $self->{_map}=$map;
}

sub get_map {
    my($self)=@_;
    $self->{_map};
}

sub set_codon_start {
    my($self,$codonstart)=@_;

    $self->{_codon_start}=(($self->{_CDSFeatures}[0]-$self->{_start})-$codonstart+1);
    $self->{_digit_codon_start} = $codonstart;
}

sub get_codon_start {
    my($self)=@_;
    $self->{_codon_start};
}

sub get_digit_codon_start {
    my($self)=@_;
    $self->{_digit_codon_start};
}

sub set_product {
    my($self,$product)=@_;
    $self->{_product}=$product;
}

sub get_product {
    my($self)=@_;
    $self->{_product};
}

sub set_annotation {
    my($self,$Astart,$Aend,$NumType,$Code) = @_;
    
    my $position = ($Astart - $self->{_start});
    while ($position<=($Aend - $self->{_start})) {
        $self->{_sequence}[$position][$NumType]=$Code;
        $position++;
    }
}

sub get_annotation {
    my($self,$position,$NumType) = @_;
    $self->{_sequence}[$position][$NumType] if defined $self->{_sequence}[$position][$NumType];
}

sub add_CDS_feature {
    my($self,$CDSstart,$CDSend)=@_;
    push(@{$self->{_CDSFeatures}},$CDSstart,$CDSend);
    set_annotation($self,$CDSstart,$CDSend,2,"C");
}

sub get_CDS_feature {
    my($self,$index) = @_;
    
    $self->{_CDSFeatures}[$index];
}

sub get_num_CDS {
        my($self) = @_;
        
        return $#{$self->{_CDSFeatures}};
}

sub set_href {
    my($self,$link) = @_;
    
    $self->{_href}=$link;
}

sub get_href {
    my($self)=@_;
    $self->{_href};
}

sub apply_HGVS_numbering {
    my($self) = @_;
    
    #Some Counters for different number blocks
    my $CDSF_size = @{$self->{_CDSFeatures}};  #The size of our Features Array
    my $CDSnum = 1;  #Keeps track of numbering of CDS regions
    my $start_3p = $self->{_CDSFeatures}[$CDSF_size-1]-$self->{_start}+1;  #The first base of the 3' block
    my $num_3p = 1;  #Keeps track of 3' numbering
    my $FeatureStepper = 0;  #Steps through the Feature Region array
    my $Int_num = 0;  #Keeps track of Intron Numbering
    my $IntDirec = 0;  #Which way are we counting in the Intron
    my $inCDS = 0;  #Are we in a CDS Region or not
    my $length_5p = $self->{_CDSFeatures}[0]-$self->{_start};  #Length of the 5' block

    if($CDSF_size % 2 != 0) {die "Uneven number of elements in CDS Features Array"}

    #Loop through the entire sequence
    for(my $linepos=0; $linepos<$self->{_length}; $linepos++) {


        if($inCDS == 0) {
                if(defined $self->{_CDSFeatures}[$FeatureStepper] && $linepos==($self->{_CDSFeatures}[$FeatureStepper]-$self->{_start})) {
                        $FeatureStepper++;
                        if($inCDS==0) {$inCDS=1} else {$inCDS=0;$Int_num=0;$IntDirec=0;}
                }
        }
        else {
                if(defined $self->{_CDSFeatures}[$FeatureStepper] && $linepos==($self->{_CDSFeatures}[$FeatureStepper]-$self->{_start}+1)) {
                        $FeatureStepper++;
                        if($inCDS==0) {$inCDS=1} else {$inCDS=0;$Int_num=0;$IntDirec=0;}
                }
        }

        if($inCDS==1) {
                $self->{_sequence}[$linepos][1] = $CDSnum;
                $CDSnum++;
                $self->{_sequence}[$linepos][2] = "C";
        }
        else {  #5',3' and Intron Numbering

                #5' Numbering
                if($length_5p>0) {
                        $self->{_sequence}[$linepos][1] = "-$length_5p";
                        $length_5p--;
                }

                #3' Numbering
                elsif($linepos >= $start_3p) {
                        $self->{_sequence}[$linepos][1] = "*$num_3p";
                        $num_3p++;
                }

                #Intron Numbering
                else {
                        my $IntLen = ($self->{_CDSFeatures}[$FeatureStepper]-$self->{_CDSFeatures}[$FeatureStepper-1])-1;
                        my $Halfway=0;

                        if($IntLen % 2==1) {
                                $Halfway=$IntLen/2+0.5;
                        }
                        else {
                                $Halfway=$IntLen/2;
                        }

                        if($Int_num<$Halfway-1 && $IntDirec==0) {
                                my $temp=$CDSnum-1;
                                $Int_num++;
                                $self->{_sequence}[$linepos][1] = "$temp+$Int_num";
                        }
                        elsif($Int_num == $Halfway-1 && $IntDirec==0) {
                                my $temp=$CDSnum-1;
                                $Int_num++;
                                $self->{_sequence}[$linepos][1] = "$temp+$Int_num";
                                $IntDirec=1;
                        }
                        else {
                                if($Halfway==$IntLen/2) {
                                        $self->{_sequence}[$linepos][1] = "$CDSnum-$Int_num";
                                        $Int_num--;
                                }
                                else {
                                        $Int_num--;
                                        $self->{_sequence}[$linepos][1] = "$CDSnum-$Int_num";
                                }
                        }
                }
        }
    }

}

}
1;
