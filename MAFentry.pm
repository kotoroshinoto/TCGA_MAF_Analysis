package MAFentry;
use strict;
use warnings;
our %col2index;
_initializeVars();
sub _initializeVars{
	my @columns;
	my $i;
	push(@columns,'Hugo_Symbol','hEntrez_Gene_Id','Center','Ncbi_Build','Chrom','Start_Position','End_Position','Strand','Variant_Classification','Variant_Type','Reference_Allele','Tumor_Seq_Allele1','Tumor_Seq_Allele2','Dbsnp_Rs','Dbsnp_Val_Status','Tumor_Sample_Barcode','Matched_Norm_Sample_Barcode','Match_Norm_Seq_Allele1','Match_Norm_Seq_Allele2','Tumor_Validation_Allele1','Tumor_Validation_Allele2','Match_Norm_Validation_Allele1','Match_Norm_Validation_Allele2','Verification_Status','Validation_Status','Mutation_Status','Sequencing_Phase','Sequence_Source','Validation_Method','Score','Bam_File','Sequencer','Tumor_Sample_UUID','Matched_Norm_Sample_UUID','File_Name','Archive_Name','Line_Number');
	$i=0;
	foreach my $col(@columns){
		$MAFentry::col2index{$col}=$i;
		$i++;
	}
#	GetIndex('Hugo_Symbol');
}
sub GetIndex{
#	my $class=shift;
	my $colname=shift;
	if(defined($col2index{$colname})){
		my $retval=$col2index{$colname};
#		print "$colname : $retval\n";
		return $retval;
	} else {
#		print "$colname not a defined column\n";
		return undef;
	}
}
sub new{
	my $class = shift;
	my $self = {
		Hugo_Symbol=>"",
		Entrez_Gene_Id=>"",
		Center=>"",
		Ncbi_Build=>"",
		Chrom=>"",
		Start_Position=>"",
		End_Position=>"",
		Strand=>"",
		Variant_Classification=>"",
		Variant_Type=>"",
		Reference_Allele=>"",
		Tumor_Seq_Allele1=>"",
		Tumor_Seq_Allele2=>"",
		Dbsnp_Rs=>"",
		Dbsnp_Val_Status=>"",
		Tumor_Sample_Barcode=>"",
		Matched_Norm_Sample_Barcode=>"",
		Match_Norm_Seq_Allele1=>"",
		Match_Norm_Seq_Allele2=>"",
		Tumor_Validation_Allele1=>"",
		Tumor_Validation_Allele2=>"",
		Match_Norm_Validation_Allele1=>"",
		Match_Norm_Validation_Allele2=>"",
		Verification_Status=>"",
		Validation_Status=>"",
		Mutation_Status=>"",
		Sequencing_Phase=>"",
		Sequence_Source=>"",
		Validation_Method=>"",
		Score=>"",
		Bam_File=>"",
		Sequencer=>"",
		Tumor_Sample_UUID=>"",
		Matched_Norm_Sample_UUID=>"",
		File_Name=>"",
		Archive_Name=>"",
		Line_Number=>""
	};
	return bless $self, $class;
}
sub processline{
	my ($class,@params)= @_;
	if (Scalar::Util::blessed($class)){die "used as an object method";}
	if (scalar(@params) != 1){die "method takes 1 and only 1 argument";}
	my @columns=split('\t',$params[0]);
	if (scalar(@columns) != 37){die "line does not have correct # of columns (37)"}
	my $newobj=$class->new();
	$newobj->{Hugo_Symbol}=$columns[0];
	$newobj->{Entrez_Gene_Id}=$columns[1];
	$newobj->{Center}=$columns[2];
	$newobj->{Ncbi_Build}=$columns[3];
	$newobj->{Chrom}=$columns[4];
	$newobj->{Start_Position}=$columns[5];
	$newobj->{End_Position}=$columns[6];
	$newobj->{Strand}=$columns[7];
	$newobj->{Variant_Classification}=$columns[8];
	$newobj->{Variant_Type}=$columns[9];
	$newobj->{Reference_Allele}=$columns[10];
	$newobj->{Tumor_Seq_Allele1}=$columns[11];
	$newobj->{Tumor_Seq_Allele2}=$columns[12];
	$newobj->{Dbsnp_Rs}=$columns[13];
	$newobj->{Dbsnp_Val_Status}=$columns[14];
	$newobj->{Tumor_Sample_Barcode}=$columns[15];
	$newobj->{Matched_Norm_Sample_Barcode}=$columns[16];
	$newobj->{Match_Norm_Seq_Allele1}=$columns[17];
	$newobj->{Match_Norm_Seq_Allele2}=$columns[18];
	$newobj->{Tumor_Validation_Allele1}=$columns[19];
	$newobj->{Tumor_Validation_Allele2}=$columns[20];
	$newobj->{Match_Norm_Validation_Allele1}=$columns[21];
	$newobj->{Match_Norm_Validation_Allele2}=$columns[22];
	$newobj->{Verification_Status}=$columns[23];
	$newobj->{Validation_Status}=$columns[24];
	$newobj->{Mutation_Status}=$columns[25];
	$newobj->{Sequencing_Phase}=$columns[26];
	$newobj->{Sequence_Source}=$columns[27];
	$newobj->{Validation_Method}=$columns[28];
	$newobj->{Score}=$columns[29];
	$newobj->{Bam_File}=$columns[30];
	$newobj->{Sequencer}=$columns[31];
	$newobj->{Tumor_Sample_UUID}=$columns[32];
	$newobj->{Matched_Norm_Sample_UUID}=$columns[33];
	$newobj->{File_Name}=$columns[34];
	$newobj->{Archive_Name}=$columns[35];
	$newobj->{Line_Number}=$columns[36];
	return $newobj;
	
}
1;