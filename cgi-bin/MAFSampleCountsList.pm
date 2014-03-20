
package MAFSampleCountsList;
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
	
#	use vars qw/$dirname/;
#	BEGIN {
#		$dirname = dirname(__FILE__);
#	}
#	use lib $dirname;
#	use MAFcounters;
	
	sub new{
		my $class =shift;
		my $self={
			counts=>{},
			_keys=>()
		};
		bless $self,$class;
		return $self;
	}
	
	sub getCount{
		my $self=shift;
		my $item=shift or Carp::croak("setCount not given any arguments, needs name and count");
		my $count=shift or Carp::croak("setCount not given a count argument");
		$self->{counts}{$item}=$count;
		if (defined($self->{counts}{$item})){
			return $self->{counts}{$item};
		}
		return undef;
	}
	
	sub setCount{
		my $self=shift;
		my $item=shift or Carp::croak("setCount not given any arguments, needs name and count");
		my $count=shift or Carp::croak("setCount not given a count argument");
		$self->{counts}{$item}=$count;
	}
	
	sub readFile{
		my $self=shift;
		my $fn=shift;
		if(! defined($fn)){Carp::croak("No filename provided to readFile");}
		my $fh=FileHandle->new($fn,"r");
	}
	
	sub split{
		my $self=shift;
		my $boundary=shift;
		#create 2 new lists, selecting destination list based on counts
		my @splitlists;
		push(MAFSampleCountsList->new(),@splitlists);#lower
		push(MAFSampleCountsList->new(),@splitlists);#higher and equal
		foreach my $item (@{$self->{_keys}}){
			my $count=$self->getCount($item);
			if(!defined($count)){die("item listed in keys was not defined in count hash");}
			if($count >=$boundary){
				$splitlists[1]->setCount($item,$count);
			} else {
				$splitlists[0]->setCount($item,$count);
			}
		}
		return \@splitlists;
	}
	
	sub _clear{
		my $self=shift;
		$self->{counts}={};
		$self->{_keys}=();
	}

1;