#!/usr/bin/env perl
use strict;
use warnings;
use Cwd;
use Cwd 'abs_path';
use File::Basename;
use Getopt::Long qw(:config no_ignore_case bundling);
use List::MoreUtils qw(uniq);
use FileHandle;
use Scalar::Util;
use vars qw/$dirname/;
BEGIN {
#	print "loading perl library: ".__FILE__,"\n";
	$dirname = dirname(__FILE__);
#	print "loading perl library: $dirname\n";
}
use lib $dirname;
use MAFentry;
use MAFfile;
use MAFcounters;
use MAFSampleCountsList;

#define object types used in this process:

package main;

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
our(@boundaries,$MAF_File,$CountFile);
our(@MAFList,@MAF_FHs);
sub main{
	my $help=0;#indicates usage should be shown and nothing should be done
	my ($opts);
	my ($boundaryarg);
	#our ($countGene,$countPatient,$countMutType)= (0) x 3;
	
	$opts = GetOptions (
							"MAF_file|m=s" => \$MAF_File,	# path to illumina data
							"Count_File|c=s"   => \$CountFile,	# path to solid data
	#						"countGene|G" => \$countGene, #list of steps to assume were already run, assume order as well (acts like pipeline)
	#						"countPatient|P" => \$countPatient,
	#						"countMutType|M" => \$countMutType,
							"boundary|b=s" => \$boundaryarg,
							"help|h" =>\$help);
	#print "$joinSOLO, $joinSTEPS, $splitCROSS\n";
	if($help){
		ShowUsage();
		exit (0);#being asked to show help isn't an error
	}
	if(! (defined($boundaryarg) and length($boundaryarg) > 0)){
		ShowUsage("must provide at least one boundary\n");
	}
	if(! (defined($MAF_File) and length($MAF_File) > 0)){
		ShowUsage("must provide path to MAF file\n");
	}
	if(! (defined($CountFile) and length($CountFile) > 0)){
		ShowUsage("must provide path to counts file\n");
	}
	my @splitarg=split(",",$boundaryarg);
	@boundaries=MAFSampleCountsList::fixBoundaries(@splitarg);
	@MAFList=prepareGroups();
	@MAF_FHs=createFilesForGroups();
	SplitMafFile();
#	foreach my $Illuminalist(@MAFList){
#	#	print ($Illuminacounter->toString());
#	}
}

sub prepareGroups{
	my $filename=$CountFile;
	my $countlist=MAFSampleCountsList->new();
	$countlist->readFile($filename);
	my @splitList=@{$countlist->split(@boundaries)};
	my $lastval=0;
	for (my $i=0;$i < scalar(@boundaries+1);$i++){
		my $value=$boundaries[$i];
		if($i == scalar(@boundaries)){
			print ("\n$lastval <= count\n");
		} else {
			print ("\n$lastval <= count < $value\n");
		}
		foreach my $item(@{$splitList[$i]->{_keys}}){
			print("$item\t".$splitList[$i]->getCount($item)."\n");
		}
		$lastval=$boundaries[$i];
	}
	return @splitList;
}

sub createFilesForGroups{
	my @filehandles;
	my ($lcount,$rcount)=(0,0);
	my $filename_base=basename($MAF_File);
	for (my $i=0;$i<scalar(@boundaries);$i++){
		$rcount=$boundaries[$i];
		push(@filehandles,FileHandle->new($filename_base.".counts.".$lcount."-".($rcount-1),'w'));
		$lcount=$rcount;
	}
	push(@filehandles,FileHandle->new($filename_base.".counts.".$lcount."-above",'w'));
	return @filehandles;
}

sub getGroupIndex{
	my $name=shift;
	my $groupindex;
	for($groupindex=0;$groupindex<scalar(@MAFList);++$groupindex){
		if(defined($MAFList[$groupindex]->getCount($name))){
			return $groupindex;
		}
	}
	return undef;
}

#create count objects and store as references
sub SplitMafFile{
#	my @counters;
#	if($countGene){
#		my $tmp=GeneMutCounter->new();
#		$tmp->{name}="Genes";
#		push(@counters,$tmp);
#	}
#	if($countPatient){
#		my $tmp=SampMutCounter->new();
#		$tmp->{name}="Samples";
#		push(@counters,$tmp);
#	}
#	if($countMutType){
#		my $tmp=MutTypeCounter->new();
#		$tmp->{name}="MutationTypes";
#		push(@counters,$tmp);
#	}
	my $maf=MAFfile->open($MAF_File);
	#count line-by-line
	my $entry;	
	while ($maf->hasMoreEntries()){
		$entry=$maf->getNextEntry();
		#skip first line (its the header)
		print ($MAF_FHs[getGroupIndex($entry->{Tumor_Sample_UUID})],$entry->getString(),"\n");
	}
	$maf->close();
#	return @counters;
}

main();
