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
	$dirname = dirname(__FILE__);
}
use lib $dirname;
use MAFentry;
use MAFfile;
use MAFcounters;


#define object types used in this process:

package main;
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

our ($countGene,$countPatient,$countMutType)= (0) x 3;
our (%counters,%outnames);
our($outpath);
sub main{
	my $help=0;#indicates usage should be shown and nothing should be done
	my ($opts);
	
	$opts = GetOptions (
#						"Input MAF file|f =s " => \@maf_File,	# path to illumina data
						"countGene|G" => \$countGene, #list of steps to assume were already run, assume order as well (acts like pipeline)
						"countPatient|P" => \$countPatient,
						"countMutType|M" => \$countMutType,
						"outname|o=s" => \$outpath,
						"help|h" =>\$help);
	
	if($help){
	ShowUsage();
	exit (0);#being asked to show help isn't an error
	}
	if(-f $outpath){
		$outpath=dirname($outpath);
	}
	if(!(-e $outpath)){
		mkdir($outpath) or die "could not create path $outpath\n";
	}
	
	if (not($countGene or $countPatient or $countMutType)){
		ShowUsage("must choose at least one of the count options");
	}
	
	
	ProcessInputFileArg(@ARGV);
	foreach my $item (keys(%outnames)){
		$counters{$item}=CountMafFile($item);
		foreach my $counter(@{$counters{$item}}){
#			print ($counter->toString());
			$counter->writeFile($outnames{$item});
		} 
	}
}

sub ProcessInputFileArg{
	foreach my $item(@_){
		#TODO check
		if(scalar(@_) < 1 or !defined($_[0]) or length($_[0]) == 0){
			Carp::carp("No arguments given to ProcessInputFileArg");
		}
		my @splitarg=split(',',$item);
		if(scalar(@splitarg) == 1 or !defined($splitarg[1]) or length($splitarg[1]) == 0){
			$outnames{$splitarg[0]}=basename($splitarg[0]).".counts";	
		} else {
			$outnames{$splitarg[0]}=$splitarg[1].".counts";
		}
#		print "linking $splitarg[0] path to name $outnames{$splitarg[0]}\n";
	}
}
#create count objects and store as references
sub CountMafFile{
	my @counters;
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
	my $maf=MAFfile->open($_[0]);
	#count line-by-line
	my $entry;	
	while ($maf->hasMoreEntries()){
		$entry=$maf->getNextEntry();
		#skip first line (its the header)
		if(isCountable($entry)){
			foreach my $counter(@counters){
				$counter->count($entry);
			}
		}
	}
	$maf->close();
	return \@counters;
}

sub isCountable{
	my $maf=$_[0];
	#TODO logic on whether to keep entry in count
	return 1;
}

main();
