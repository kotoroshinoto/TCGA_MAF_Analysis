#!/usr/bin/env perl
use strict;
use warnings;
use Cwd;
use Cwd 'abs_path';
use File::Basename;
#use Getopt::Long qw(:config no_ignore_case bundling);
use Getopt::ArgParse;
use List::MoreUtils qw(uniq);
use FileHandle;
use Scalar::Util;
use vars qw/$dirname/;
use File::Util;
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

sub parse_arguments {
    my $ap = Getopt::ArgParse->new_parser(
        description => 'This script counts elements that apear in MAF files',
        help => 'maf element counter',
        epilog      => '--end of help --',
    );
    $ap->add_arguments(
#    ['--inputFile',     '-f',type=>'Scalar',required => 1,nargs => '+'],
    ['--countGene',     '-G',type=>'Bool'],
    ['--countPatient',  '-P',type=>'Bool'],
    ['--countMutType',  '-M',type=>'Bool'],
    ['--outname',       '-o',type=>'Scalar',required => 1]
    );
    if (scalar(@ARGV) == 0){
        $ap->print_usage();
        exit(1);
    }
    my $parser_namespace = $ap->parse_args(@ARGV);
    $countGene = $parser_namespace->countGene;
    $countPatient = $parser_namespace->countPatient;
    $countMutType = $parser_namespace->countMutType;
    $outpath = $parser_namespace->outname;
	if(-f $outpath){
		$outpath=dirname($outpath);
	}
	if(!(-e $outpath)){
		mkdir($outpath) or die "could not create path $outpath\n";
	}

    if (not($countGene or $countPatient or $countMutType)){
        print(STDERR "must choose at least one of the count options\n");
        $ap->print_usage();
        exit(1);
    }

    #my @argv = ; # called after parse_args
    ProcessInputFileArg($ap->argv);
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
		print "output from $splitarg[0] will be routed to file: $outnames{$splitarg[0]}\n";
	}
}

sub main{
    parse_arguments();
	foreach my $item (keys(%outnames)){
		$counters{$item}=CountMafFile($item);
		foreach my $counter(@{$counters{$item}}){
#			print ($counter->toString());
			$counter->writeFile($outpath.SL.$outnames{$item});
		} 
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
