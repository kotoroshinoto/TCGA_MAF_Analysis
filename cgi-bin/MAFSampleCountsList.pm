
package MAFSampleCountsList;
	use strict;
	use warnings;
	use Carp qw(cluck);
	use Cwd;
	use Cwd 'abs_path';
	use File::Basename;
	use Getopt::Long qw(:config no_ignore_case bundling);
	use List::MoreUtils qw(uniq firstidx);
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
			_keys=>[]
		};
		bless $self,$class;
		return $self;
	}
	
	sub getCount{
		my $self=shift;
		my $item=shift or Carp::croak("setCount not given any arguments, needs name and count");
		if (defined($self->{counts}{$item})){
			return $self->{counts}{$item};
		}
		return undef;
	}
	
	sub setCount{
		my $self=shift;
		my $item=shift or Carp::croak("setCount not given any arguments, needs name and count");
		my $count=shift or Carp::croak("setCount not given a count argument");
		if(!defined($self->{counts}{$item})){
			push($self->{_keys},$item);
		}
		$self->{counts}{$item}=$count;
	}
	
	sub readFile{
		my $self=shift;
		my $fn=shift;
		if(! defined($fn)){Carp::croak("No filename provided to readFile");}
		my $fh=FileHandle->new($fn,"r");
		if(! defined($fh)){die("Could not open file: $fn\n");}
		foreach my $line(<$fh>){
			my @splitline=split('\t',$line);
#			print(join(',',@splitline));
			$self->setCount($splitline[0],$splitline[1]+0);
		}
	}
	
	sub fixBoundaries{
		my @boundaries=@_;
		if(@boundaries < 1){Carp::croak("No boundary arguments supplied to fixBoundaries")}
		@boundaries=uniq(@boundaries);
		@boundaries=sort {$a <=> $b} @boundaries;
		my @result;
		foreach my $value(@boundaries){
			if($value >= 0){
				push(@result,$value);
			} else {
				print STDERR "WARNING: $value removed as it is not a valid boundary\n";
			}
		}
		
		return @result;
	}
	#split will have it args sorted and have duplicates removed prior to running _split
	sub split{
		my $self=shift;
		my @boundaries=@_;
		if(@boundaries < 1){Carp::croak("No boundary arguments supplied to split")}
		@boundaries=MAFSampleCountsList::fixBoundaries(@boundaries);
		print ("splitting on boundaries: ",join(',',@boundaries),"\n");
		my @tmparr;
		my @result;
		my $tmpval=$self;
		foreach my $boundary(@boundaries){
			@tmparr=@{$tmpval->_split($boundary)};
			push(@result,$tmparr[0]);
			$tmpval=$tmparr[1];
		}
		push(@result,$tmpval);
		return \@result;
	}
	#_split is for a single split, taking care of the more complex operation
	sub _split{
		my $self=shift;
		my $boundary=shift;
		if(!defined($boundary)){Carp::croak("No boundary argument supplied to _split")}
		#create 2 new lists, selecting destination list based on counts
		my @splitlists;
		push(@splitlists,MAFSampleCountsList->new());#lower
		push(@splitlists,MAFSampleCountsList->new());#higher and equal
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