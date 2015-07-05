package VVRefFetch;

use strict;
use warnings;
use VVSeq;

sub Fetch {

        my($GeneName,$RefLoc,$AccNum,$VVFolder,$Format, $locpath) = @_;
        
        unless($GeneName && $RefLoc && $AccNum && $VVFolder && $Format) {
                die "Arguments not passed. Stopped ";
        }
        
        #Define VVSeq object to pass back
        my $ObjRef = VVSeq->new(genename=>$GeneName);
        
        #Define BioPerl Objects
        my $SeqIO;
        my $BPSeq;

        #Create correct BioPerl Objects based on user settings
        if($RefLoc eq "Genbank") {
                eval {
                        use Bio::DB::GenBank;
                        $SeqIO = new Bio::DB::GenBank();
                        $BPSeq = $SeqIO->get_Seq_by_version($AccNum);
                };
                if($@){
                        die "Could not access Genbank. Check that the accession and version numbers for your gene are correct. Ensure you are connected to the internet. Stopped ";
                }

        }
        elsif($RefLoc eq "Local") {
                eval {
                        use Bio::SeqIO;
                        $SeqIO= Bio::SeqIO->new(-file => $locpath.$AccNum, -format => lc($Format) );
                        $BPSeq = $SeqIO->next_seq;
                };
                if($@){
                        die "Could not access local sequence file. Check that the file name and format of your file are correct. At the moment we're looking for a <code>".$Format."</code> file located here: <code>".$locpath.$AccNum."</code>. Stopped ";
                }
        }
        elsif($RefLoc eq "RefSeq") {
                eval {
                        use Bio::DB::RefSeq;
                        $SeqIO = new Bio::DB::RefSeq();
                        $BPSeq = $SeqIO->get_Seq_by_version($AccNum);
                };
                if($@){
                        die "Could not access RefSeq database. Check that the accession and version numbers for your gene are correct. Ensure you are connected to the internet. Stopped ";
                }
        }
        elsif($RefLoc eq "Embl") {
                eval {
                        use Bio::DB::EMBL;
                        $SeqIO = new Bio::DB::EMBL();
                        $BPSeq = $SeqIO->get_Seq_by_version($AccNum);
                };
                if($@){
                        die "Could not access Embl database. Check that the accession and version numbers for your gene are correct. Ensure you are connected to the internet. Stopped ";
                }
        }
        else {  #Bad Setting in .ini file
                die "Invalid location defined. \'$RefLoc\' is not an accepted value. Stopped ";
        }


        ###################################
        # Conversion from BP to VV Object #
        ###################################
        
        if(ref($BPSeq) eq "Bio::Seq::RichSeq") {
                #Create an array of all the RichSeq features
                #and step through it looking for relevant primary tags
                my @features = $BPSeq->get_SeqFeatures();

                foreach my $feat ( @features ) {

                        #Find the source and get the chromosome location
                        if($feat->primary_tag eq "source") {
                                $ObjRef->set_map($feat->get_tag_values('map')) if $feat->has_tag('map');
                                $ObjRef->set_species($feat->get_tag_values('organism')) if $feat->has_tag('organism');
                                $ObjRef->set_start($feat->start);
                                $ObjRef->set_sequence($feat->spliced_seq->seq);
                        }

                        #Find the CDS region
                        if($feat->primary_tag eq "CDS") {
                                                #If the CDS is a split location then deal with all of them
                                                if($feat->location->isa('Bio::Location::SplitLocationI')){
                                                        foreach my $location( $feat->location->sub_Location ) {
                                                                $ObjRef->add_CDS_feature($location->start,$location->end)
                                                        }
                                                }
                                                #otherwise it's just a straight through
                                                else {
                                                        $ObjRef->add_CDS_feature($feat->start,$feat->end);
                                                }

                                                #Set Extra info
                                                $ObjRef->set_codon_start($feat->get_tag_values('codon_start')) if $feat->has_tag('codon_start');
                                                $ObjRef->set_product($feat->get_tag_values('product')) if $feat->has_tag('product');
                                                $ObjRef->set_translation($feat->get_tag_values('translation')) if $feat->has_tag('translation');
                        }

                        # find mRNA sequence if available
                        if($feat->primary_tag eq "mRNA") {
                                #If the mRNA is a split location then deal with all of them
                                if($feat->location->isa('Bio::Location::SplitLocationI')){
                                        foreach my $location( $feat->location->sub_Location ) {
                                                $ObjRef->set_annotation($location->start,$location->end,3,"M")
                                        }
                                }
                                #otherwise it's just a straight through
                                else {
                                        $ObjRef->set_annotation($feat->start,$feat->end,3,"M")
                                }
                        }
                        
                        # find Promoter sequence if available
                        if($feat->primary_tag eq "promoter") {
                                #If the promoter is a split location then deal with all of them
                                if($feat->location->isa('Bio::Location::SplitLocationI')){
                                        foreach my $location( $feat->location->sub_Location ) {
                                                                $ObjRef->set_annotation($location->start,$location->end,4,"P")
                                        }
                                }
                                #otherwise it's just a straight through
                                else {
                                        $ObjRef->set_annotation($feat->start,$feat->end,4,"P")
                                }
                        }
                        # find 3' UTR sequence if available
                        if($feat->primary_tag eq "3'UTR") {
                                #If the promoter is a split location then deal with all of them
                                if($feat->location->isa('Bio::Location::SplitLocationI')){
                                        foreach my $location( $feat->location->sub_Location ) {
                                                                $ObjRef->set_annotation($location->start,$location->end,6,"3")
                                        }
                                }
                                #otherwise it's just a straight through
                                else {
                                        $ObjRef->set_annotation($feat->start,$feat->end,6,"3")
                                }
                        }
                        # find Poly 5'UTR sequence if available
                        if($feat->primary_tag eq "5'UTR") {
                                #If the promoter is a split location then deal with all of them
                                if($feat->location->isa('Bio::Location::SplitLocationI')){
                                        foreach my $location( $feat->location->sub_Location ) {
                                                                $ObjRef->set_annotation($location->start,$location->end,5,"5")
                                        }
                                }
                                #otherwise it's just a straight through
                                else {
                                        $ObjRef->set_annotation($feat->start,$feat->end,5,"5")
                                }
                        }
                        # find Poly A sequence if available
                        if($feat->primary_tag eq "polyA_signal") {
                                #If the promoter is a split location then deal with all of them
                                if($feat->location->isa('Bio::Location::SplitLocationI')){
                                        foreach my $location( $feat->location->sub_Location ) {
                                                                $ObjRef->set_annotation($location->start,$location->end,7,"A")
                                        }
                                }
                                #otherwise it's just a straight through
                                else {
                                        $ObjRef->set_annotation($feat->start,$feat->end,7,"A")
                                }
                        }

                }
        }
        elsif (ref($BPSeq) eq "Bio::Seq") {
                $ObjRef->set_start(1);
                $ObjRef->set_sequence($BPSeq->seq);
                $ObjRef->add_CDS_feature(1,$BPSeq->length)
        }
        else {die "Invalid Sequence Object. Stopped "};

        if($ObjRef->get_num_CDS == -1) {
                $ObjRef->set_start(1);
                $ObjRef->set_sequence($BPSeq->seq);
                $ObjRef->add_CDS_feature(1,$BPSeq->length)
        }

        #Apply Official HGVS Numbering
        $ObjRef->apply_HGVS_numbering;

        return $ObjRef;
}

1;
