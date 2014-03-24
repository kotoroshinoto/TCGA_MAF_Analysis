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
my $help=0;#indicates usage should be shown and nothing should be done
my ($MAF_File,$CountFile,$opts);
#our ($countGene,$countPatient,$countMutType)= (0) x 3;

$opts = GetOptions (
						"MAF_file|m=s" => \$MAF_File,	# path to illumina data
						"Count_File|c=s"   => \$CountFile,	# path to solid data
#						"countGene|G" => \$countGene, #list of steps to assume were already run, assume order as well (acts like pipeline)
#						"countPatient|P" => \$countPatient,
#						"countMutType|M" => \$countMutType,
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
if(((not defined($MAF_File)) and (not defined($CountFile))) or (length($MAF_File) == 0 and length($CountFile) == 0)){
	ShowUsage("must provide at least one of the MAF files");
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
#	my $maf=MAFfile->open($_[0]);
#	#count line-by-line
#	my $entry;	
#	while ($maf->hasMoreEntries()){
#		$entry=$maf->getNextEntry();
#		#skip first line (its the header)
#		if(isCountable($entry)){
#			foreach my $counter(@counters){
#				$counter->count($entry);
#			}
#		}
#	}
#	$maf->close();
#	return @counters;
}

sub getGroupIndex{
	
}

sub prepareGroups{
	my $filename=shift;
	my @boundaries=MAFSampleCountsList::fixBoundaries(@_);
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
	return $countlist;
}

sub main{
	my @IlluminaList;
	if(defined($MAF_File) and length($MAF_File) > 0){
		@IlluminaList=@{prepareGroups($MAF_File)};
	} else {
		
	}
	
	my @SOLiDList;
	if(defined($CountFile) and length($CountFile) > 0){
		@SOLiDList=@{prepareGroups($CountFile)};
	} else {
		
	}
	
	foreach my $Illuminalist(@IlluminaList){
	#	print ($Illuminacounter->toString());
	}
	
	foreach my $SOLiDCounter(@SOLiDList){
	#	print ($SOLiDCounter->toString());
	}
}
main();
