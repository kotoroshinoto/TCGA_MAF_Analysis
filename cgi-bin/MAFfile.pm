use strict;
use warnings;
use Carp qw(cluck);
use Cwd;
use Cwd 'abs_path';
use File::Basename;
use Getopt::Long qw(:config no_ignore_case bundling);
use List::MoreUtils qw(uniq);
use FileHandle;
use Scalar::Util;
use vars qw/$dirname/;
BEGIN {
	$dirname = dirname(__FILE__);
}
use lib $dirname;
use MAFentry;
package MAFfile;
sub open{
	my $class =shift;
	my $self={
		_fn=>undef,
		_fh=>undef,
		_nextline=>undef,
		_linecount=>0#number of lines returned from object
	};
	bless $self, $class;
	#now open a file provided by next argument
	if (@_ != 1) {
  		Carp::croak ("Filename argument required");
  		exit 1;
	}
	$self->{_fn}=shift;
	$self->{_fh}=FileHandle->new($self->{_fn},"r");
	unless(defined($self->{_fh})){Carp::croak ("Could not open maf file: $self->{_fn}")};
	#load first line
	$self->{_nextline} = $self->{_fh}->getline();
	if(defined($self->{_nextline})){chomp($self->{_nextline});}
	if($self->{_nextline} eq "Hugo_Symbol	Entrez_Gene_Id	Center	Ncbi_Build	Chrom	Start_Position	End_Position	Strand	Variant_Classification	Variant_Type	Reference_Allele	Tumor_Seq_Allele1	Tumor_Seq_Allele2	Dbsnp_Rs	Dbsnp_Val_Status	Tumor_Sample_Barcode	Matched_Norm_Sample_Barcode	Match_Norm_Seq_Allele1	Match_Norm_Seq_Allele2	Tumor_Validation_Allele1	Tumor_Validation_Allele2	Match_Norm_Validation_Allele1	Match_Norm_Validation_Allele2	Verification_Status	Validation_Status	Mutation_Status	Sequencing_Phase	Sequence_Source	Validation_Method	Score	Bam_File	Sequencer	Tumor_Sample_UUID	Matched_Norm_Sample_UUID	File_Name	Archive_Name	Line_Number" ){
		print STDERR ("First line in $self->{_fn} was a header line, ignoring it\n");
		$self->{_nextline} = $self->{_fh}->getline();
		if(defined($self->{_nextline})){chomp($self->{_nextline});}
		$self->{_linecount}++;
	}
	return $self;
}

sub close{
	my $self = shift;
	$self->{_fh}->close();
	$self->{_fn}=undef;
	$self->{_nextline}=undef;
	$self->{_linecount}=undef;
}

sub getNextEntry{
	my $self= shift;
	my $entryobj=MAFentry->processline($self->{_nextline});
	$self->{_nextline} = $self->{_fh}->getline();
	if(defined($self->{_nextline})){chomp($self->{_nextline});}
	if(defined($entryobj)){
		$self->{_linecount}++;
	}
	return $entryobj;
}
sub hasMoreEntries{
	my $self= shift;
	if (defined($self->{_nextline})){
		return 1;
	}else {
		return 0;
	}
}
1;