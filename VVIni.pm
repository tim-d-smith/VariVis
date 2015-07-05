package VVIni;

# A class to read .ini files

use strict;
use warnings;

#Class Data and Methods
{
  my %_attributes = (
    _data => {},
    _filename => '',
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

    #Filename must be given as argument
    unless($arg{filename}) {return undef}

    #Set the attributes for given arguments
    foreach my $attribute ($self->_all_attributes) {

        #Strip the _ off the attribute name to get argument
        my($argument) = ($attribute =~ /^_(.*)/);

        #Set to default argument
        $self->{$attribute} = $self->_attribute_value($attribute);

        #Replace default with given argument
        if (exists $arg{$argument}) {
            if($argument eq 'data') {return undef}
            $self->{$attribute} = $arg{$argument};
        }
    }
    if (-e $self->{_filename} && -r $self->{_filename}) {$self->_load}
    return $self;
}


sub _load {
    my($self) = @_;
    #Load the data
    open(MY_INI,$self->{_filename}) || return undef;

    while(<MY_INI>) {
        next unless /\S/;
        next unless /^([A-Z0-9]+)=([A-Z0-9 {}!#$%^&*(\-\[\]\|'"<>?`~)+=@\/\\._,;:]+)/i;
        $self->{_data}{$1} = $2;
    }
    close(MY_INI);
}


sub get_value {
        my($self,$key) = @_;
        unless($self->{_data}{$key}) {
                return "";
        }
}

sub set_value {
        my($self,$key,$value) = @_;
        $self->{_data}{$key} = $value;
}

sub wrap_it {
        my($self) = @_;

        my $filename = $self->{_filename};

        if(keys(%{$self->{_data}})==0) {return undef};

        open(MY_INI,">$filename") || return undef;

        foreach my $key (keys %{$self->{_data}}) {
                print MY_INI "$key=$self->{_data}{$key}\n";
        }
        
        close(MY_INI);
        
}
        
}
1;

