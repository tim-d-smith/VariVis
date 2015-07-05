package program;

{
  my %_attributes = (
    _version => '1.3.5',
    _legal => '<div style="border-top:1px solid silver;"><p>This software is provided withouth warranty under the terms of the VariVis Software License. For more infomration refer to License.txt or <a href="http://www.genomic.unimelb.edu.au/varivis/license.html">http://www.genomic.unimelb.edu.au/varivis/license.html</a>. Copyright (c) Genomic Disorders Research Centre. All rights reserved.</p></div>',
    _info => 'Created with <a href="http://www.genomic.unimelb.edu.au/varivis/">VariVis</a>',
    _help_url => 'http://www.genomic.unimelb.edu.au/varivis/help.html',
    _style => <<END
    body {
        font-size : 10pt;
        font-style : Arial, sans-serif;
    }

    div.error {
	border: 2px solid red;
	background-color: #ff6666;
	padding: .5em 1em;
	margin-bottom: 2em;
	color: #000;
	}

    table {
        background-color: #ffffff;
        color: #000000;
        border : 1px solid #f0f0f0;
        width : 100%;
        border-spacing: 0px;
	border-collapse : collapse;
        padding : 0.6em;
        margin-bottom:32px;
      font-family: sans-serif;
    }
    caption {font-size:110%;font-weight:bold;}
    th {
      color: #000000;
      background-color : #cccccc;
      text-align : right;
      font-size : 100%;
      font-weight : bold;
      border:1px solid silver;
    }
    td.note {
        margin-left: 0;
        font-style : italic;
        font-size : 80%;
    }
    span.error {color:red;font-weight:bold;}
    span.ok {color:green;font-weight:bold;}
    td {margin-left:1em;padding-left:1em;border:1px solid silver;}

END
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
            $self->{$attribute} = $arg{$argument};
        }
    }
    return $self;
}

sub get{
        my($self,$key) = @_;
        unless($self->{"_$key"}) {
                return "";
        }
}

}
1;
