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
		_linecount=>0
	};
	bless $self, $class;
	#now open a file provided by next argument
	if (@_ != 1) {
  		croak ("Filename argument required");
  		exit 1;
	}
	$self->{_fn}=shift;
	$self->{_fh}=FileHandle->open("< $self->{_fn}");
	unless(defined($self->{_fh})){die ("Could not open maf file: $self->{_fn}")};
	#load first line
	$self->{_nextline} = $self->{_fh}->getline();
	return $self;
}
sub getNextEntry{
	my $self= shift;
	my $entryobj=MAFentry->processline($self->{_nextline});
	$self->{_nextline} = $self->{_fh}->getline();
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