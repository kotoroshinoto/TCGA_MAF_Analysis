use strict;
use warnings;
use Cwd;
use Cwd 'abs_path';
use File::Basename;
use Getopt::Long qw(:config no_ignore_case bundling);
use List::MoreUtils qw(uniq);
use FileHandle;
use Scalar::Util;
use MAFentry;
use MAFcounters;

#define object types used in this process:
#TODO change count mechanism to use geneID as storage key

package main;
my $help=0;#indicates usage should be shown and nothing should be done
my ($illuminaFile,$solidFile,$opts);
our ($countGene,$countPatient,$countMutType)= (0) x 3;

$opts = GetOptions ("Illumina|f=s" => \$illuminaFile,	# path to illumina data
						"Solid|F=s"   => \$solidFile,	# path to solid data
						"countGene|G" => \$countGene, #list of steps to assume were already run, assume order as well (acts like pipeline)
						"countPatient|P" => \$countPatient,
						"countMutType|M" => \$countMutType,
						"help|h" =>\$help);
#print "$joinSOLO, $joinSTEPS, $splitCROSS\n";
sub ShowUsage {
	my $errmsg=shift;
	my $scriptname=basename($0);
	my $usage="Usage: $scriptname [options]\n";
	if(!defined($errmsg)||$errmsg eq ""){
		$errmsg="";
	} else {
		$errmsg.="\n";
	}
	print STDERR "$errmsg$usage\n";
	exit(1);
}
if($help){
	ShowUsage();
	exit (0);#being asked to show help isn't an error
}
if(((not defined($illuminaFile)) and (not defined($solidFile))) or (length($illuminaFile) == 0 and length($solidFile) == 0)){
	ShowUsage("must provide at least one of the MAF files");
}
if (not($countGene or $countPatient or $countMutType)){
	ShowUsage("must choose at least one of the count options");
}
#create count objects and store as references
sub CountMafFile{
	my @counters;
	my $mafFile=$_[0];
	if($countGene){
		my $tmp=GeneMutCounter->new();
		$tmp->{name}="Genes";
		push(@counters,$tmp);
	}
	if($countPatient){
		my $tmp=SampMutCounter->new();
		$tmp->{name}="Samples";
		push(@counters,$tmp);
	}
	if($countMutType){
		my $tmp=MutTypeCounter->new();
		$tmp->{name}="MutationTypes";
		push(@counters,$tmp);
	}
	my $maf=FileHandle->new($mafFile,'r');
	unless(defined($maf)){die "Could not open maf file: $mafFile"};
	#count line-by-line
	my $linecount=0;
	foreach my $line (<$maf>){
		#skip first line (its the header)
		if($linecount){
			my $entry=MAFentry->processline($line);
			if(isCountable($entry)){
				foreach my $counter(@counters){
					$counter->count($entry);
				}
			}
		}
		$linecount++;       
	}
	$maf->close();
	return @counters;
}
sub isCountable{
	my $maf=$_[0];
	#TODO logic on whether to keep entry in count
	return 1;
}

my @IlluminaCounters;
if(defined($illuminaFile) and length($illuminaFile) > 0){
	@IlluminaCounters=CountMafFile($illuminaFile);
}

my @SOLiDCounters;
if(defined($solidFile) and length($solidFile) > 0){
	@SOLiDCounters=CountMafFile($solidFile);
}

foreach my $Illuminacounter(@IlluminaCounters){
#	print ($Illuminacounter->toString());
	$Illuminacounter->writeFile("Illumina","");
}

foreach my $SOLiDCounter(@SOLiDCounters){
#	print ($SOLiDCounter->toString());
	$SOLiDCounter->writeFile("SOLiD");
}
