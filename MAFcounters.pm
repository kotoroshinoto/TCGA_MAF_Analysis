package FeatureCounter;
use strict;
use warnings;
use MAFentry;
sub new{
	my $class = shift;
	my $self = {
		counts=>{},
		name=>undef
		#TODO provide interaction methods
	};
	return bless $self, $class;
}
sub determineMutation{
#	my $class = shift;
	if (scalar(@_) != 4){die "wrong # of arguments given to determineMutation: got scalar(@_) needed 4"}
	my @nrm;
	push (@nrm,shift);
	push (@nrm,shift);
	my @tmr;
	push (@tmr,shift);
	push (@tmr,shift);
	if(length($tmr[0])>1 or length($tmr[1])>1 or length($nrm[0])>1 or length($nrm[1])>1){
		die ("Invalid arguments, alleles given to determineMutation must be 1 character long");
	}
	my @mutation;
	if($tmr[0] eq $nrm[0]){	
		if($tmr[1] eq $nrm[1]){
			#TODO this isn't a mutation
			return "";
		} else {
			#TODO record change from $nrm[1] to $tmr[1]
			return $nrm[1].'_'.$tmr[1];
		}
	}elsif($tmr[1] eq $nrm[1]){
		if($tmr[0] eq $nrm[0]){
			#TODO this isn't a mutation
			return "";
		} else {
			#TODO record change from $nrm[0] to $tmr[0]
			return $nrm[0].'_'.$tmr[0];
		}
	}elsif($tmr[0] eq $nrm[1]){
		if($tmr[1] eq $nrm[0]){
			#TODO this isn't a mutation
			return "";
		} else {
			#TODO record change from $nrm[0] to $tmr[1]
			return $nrm[0].'_'.$tmr[1];
		}
	}elsif($tmr[1] eq $nrm[0]){
		if($tmr[0] eq $nrm[1]){
			#TODO this isn't a mutation
			return "";
		} else {
			#TODO record change from $nrm[1] to $tmr[0] 
			return $nrm[1].'_'.$tmr[0];
		}
	}else {
		#cannot determine mutation type, both alleles different, no match
		return undef;
	}
}
sub __appendcount{
	my ($self,@params)= @_;
	if (scalar(@params) != 1){die "method takes 1 and only 1 argument";}
	if(defined($self->{counts}{$params[0]})){
		$self->{counts}{$params[0]}++;
	} else {
		$self->{counts}{$params[0]}=1;
	}
}
sub __countIf{
	my ($self,@params)= @_;
	if (scalar(@params) != 2){die "method takes 2 and only 2 arguments";}
	if($params[1]){
		$self->__appendcount($params[0]);
	}
}
sub toString{
#	print "toString run\n";
	my $self=shift;
	my @keys=sort(keys($self->{counts}));
	my $retval='';
	foreach my $key(@keys){
		$retval.="$key\t$self->{counts}{$key}\n";
	}
	return $retval;
}
sub writeFile{
	my $self=shift;
	my $prefix=shift;
	my $path=shift;
	if (!defined($path) or length($path)==0){
		$path=".";
	}
#TODO remove trailing slash, or use some other path combination method
	if (defined($self->{name}) and length($self->{name}) > 0){
		my $ofname;
		if(defined($prefix) and length($prefix) > 1){
			$ofname=$path.'/'.$prefix.'_'.$self->{name}.".txt";			
		} else {
			$ofname=$path.'/'.$self->{name}.".txt";
		}
#		print "$ofname\n";
		my $of=FileHandle->new($ofname,'w');
		$of->write($self->toString());
		$of->close();
	}else {
		die "writeFile used on counter with no name";
	}
}
1;
package GeneMutCounter;
use parent -norequire, 'FeatureCounter';
sub count{
#	print "Gene  mutationcount run\n";
	my ($self,@params)= @_;
	if (scalar(@params) != 1){die "method takes 1 and only 1 argument";}
	my $maf=$params[0];
	$self->__appendcount($maf->{Hugo_Symbol});
}
1;
package SampMutCounter;
use parent -norequire, 'FeatureCounter';
sub count{
#	print "Sample mutation count run\n";
	my ($self,@params)= @_;
	if (scalar(@params) != 1){die "method takes 1 and only 1 argument";}
	my $maf=$params[0];
	$self->__appendcount($maf->{Tumor_Sample_Barcode});
}
1;
package MutTypeCounter;
use parent -norequire, 'FeatureCounter';
sub count{
#	print "Mutation type count run\n";
	my ($self,@params)= @_;
	if (scalar(@params) != 1){die "method takes 1 and only 1 argument";}
	my $maf=$params[0];
#TODO count mutations by type
my (@tmr,@nrm);
	push(@tmr,uc($maf->{Tumor_Seq_Allele1}));
	push(@tmr,uc($maf->{Tumor_Seq_Allele2}));
	push(@nrm,uc($maf->{Match_Norm_Seq_Allele1}));
	push(@nrm,uc($maf->{Match_Norm_Seq_Allele2}));
	if(length($tmr[0])>1 or length($tmr[1])>1 or length($nrm[0])>1 or length($nrm[1])>1){
		#TODO maybe append count of MNPs
		$self->__appendcount("MNC");
		return;
	}
	
	my $mutation=FeatureCounter::determineMutation(@nrm,@tmr);
	if (defined($mutation)){
		if(length($mutation) > 0){
			$self->__appendcount($mutation);
		}
	} else {
		#count as 'double_mut'
		$self->__appendcount("DMA");
	}
}
1;