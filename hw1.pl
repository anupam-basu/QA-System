# Kevin Corder
# perl script to wrap python3 script
# requires:
#   python3
#   nltk (for python)
 
use strict;
use warnings;
 
my $pythonBin = 'python';      # python3 executable
#my $hwScript = 'kcorder_hw1.py';   # my python script name!
my $hwScript = 'qa1.py';
my @argsArray = ("$pythonBin", "$hwScript"); # array to pass into system()
my $num_args = $#ARGV + 1;
my $INCORRECTARGS = "This script requires 1 or 2 arguments. " .
    "Call as:\n\nperl hw1.pl <articleFile> (<questionsFile>)\n\n";
# if filenames are provided, add them to @argsArray
 
if ($num_args > 2 or $num_args == 0){
    print "$INCORRECTARGS"; exit;
} elsif ($num_args == 1 or $num_args == 2){
    push @argsArray, $ARGV[0];
    if ($num_args == 2){
        push @argsArray, $ARGV[1];
    }
}
 
my $ret = system(@argsArray); # call the script!
# like: system(python3 kcorder_hw1.py <articleFile> (<questionsFile>))
if ($ret != 0){
    print "$hwScript returned with errors; exit code: $ret\n";
}
 