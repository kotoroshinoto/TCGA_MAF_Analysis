
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
		
	}
	
	sub readFile{
		
	}
	
	sub _clear{
		
	}

1;