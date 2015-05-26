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
BEGIN {
	$dirname = dirname(__FILE__);
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
our($outname);

sub parse_arguments {

    my $ap = Getopt::ArgParse->new_parser(
        description => 'This script splits elements in MAF files into separate output files based on counts',
        help => 'maf splitter by count',
        epilog      => '--end of help --',
    );
    $ap->add_arguments(
    ['--MAF_File',      '-m',type=>'Scalar',required => 1],
    ['--Count_File',    '-c',type=>'Scalar',required => 1],
    ['--boundary',      '-b',type=>'Scalar',required => 1],
    ['--output',        '-o',type=>'Scalar',required => 1]
    );
    if (scalar(@ARGV) == 0){
        $ap->print_usage();
        exit(1);
    }
    my $parser_namespace = $ap->parse_args(@ARGV);

    if (scalar($ap->argv) != 0){
        $ap->print_usage();
        exit(1);
    }
	my @splitboundaryarg=split(",",$parser_namespace->boundary);
	@boundaries=MAFSampleCountsList::fixBoundaries(@splitboundaryarg);
	$MAF_File=$parser_namespace->MAF_File;
	$CountFile=$parser_namespace->Count_File;
	$outname=$parser_namespace->output;
}

sub main{
    parse_arguments();
	@MAFList=prepareGroups();
	exit(0);
	@MAF_FHs=createFilesForGroups();
	SplitMafFile();
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
	if(defined($outname)){
		$filename_base=$outname;
	}
	for (my $i=0;$i<scalar(@boundaries);$i++){
		$rcount=$boundaries[$i];
		my $tmp_fh=FileHandle->new($filename_base.".counts.".$lcount."-".($rcount-1),'w');
		if(!defined( $tmp_fh)){
		    die ("could not open file ".$filename_base.".counts.".$lcount."-".($rcount-1),'w'."\n");
		}
		push(@filehandles,);
		$lcount=$rcount;
	}
	push(@filehandles,FileHandle->new($filename_base.".counts.".$lcount."-above",'w'));
	return @filehandles;
}

sub printGroups{

}

sub getGroupIndex{
	my $name=shift;
	my $groupindex;
	for($groupindex=0;$groupindex<scalar(@MAFList);++$groupindex){
		if(defined($MAFList[$groupindex]->getCount($name))){
			return $groupindex;
		}
	}
	print STDERR "could not locate a group index for $name\n";
	return undef;
}

#create count objects and store as references
sub SplitMafFile{
	my $maf=MAFfile->open($MAF_File);
	my $filehandle_index;
	#count line-by-line
	my $entry;	
	while ($maf->hasMoreEntries()){
		$entry=$maf->getNextEntry();
		#skip first line (its the header)
		$filehandle_index=getGroupIndex($entry->{Tumor_Sample_Barcode});

		if( ! defined($filehandle_index) )
		{
		    print(STDERR "filehandle index not defined\n");
		}
		elsif ( ! defined( $MAF_FHs[$filehandle_index] ) )
		{
		    print(STDERR "filehandle for group # ".$filehandle_index." is undefined\n");
		}
		if(defined($filehandle_index) ){
		    $MAF_FHs[$filehandle_index]->print(($entry->getString()));
		}
	}
	$maf->close();
}

main();
