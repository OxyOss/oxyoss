#!/usr/bin/perl -w

# (C) Kim Holburn 2014 
# released  under GNU Public License http://www.gnu.org/copyleft/gpl.html
# script to generate pseudo-random things like words
# version 1.1

# To do: make it unicode compliant.

# I use these files among others:
# The complete works of Jane Austen:
# http://www.gutenberg.org/ebooks/31100.txt.utf-8
# The complete works of William Shakespeare:
# http://www.gutenberg.org/ebooks/100.txt.utf-8
#
# Creates unreal words from ngraphs based on text
# can be used to create words for password use
#
# reads the text files given to it and creates a frequency table
# of n characters based on the text.
# then creates a random sequence of ngraphs weighted by frequency.
# It massages the text first as gutenberg text has newline (\r\n)
# at the end of each line and double at the end of a paragraph
# (\r\n\r\n).  
# Handles end of line as \n, \r, \r\n so works with 
# unix, Mac or windows text files.
# Has an option for files where a paragraph is ended by newline 
# instead.

sub fail_usage {
  if (scalar @_) {
    print "$0: error: \n";
    map { print "   $_\n"; } @_;
  }
  print <<EOM;
$0: Usage: 
  -f|--file <file of text>
  -g|--ngraph <n>  (size of ngraph (3))
  -c|--count <n>   (number of character to output (100))
  -C|--paragraphs <n> (number of paragraphs to output default not used)
  -p|--popular <n> (only use words of frequency greater than pop (0))
  -l|--lower       (fold to lower case (default))
  -u|--upper       (fold to upper case)
  -L|--keep-case   (original case)
  -m|--format <n>  (1,2 (default 2))
       2=(blank line is end of paragraph, otherwise new lines ignored)
         (gutenberg text format)
       1=(new line is end of paragraph)
  -v|--verbose     (verbosity - can be used more than once)
  
  -x|--extract-text (output the final form of input text and exit)
  -y|--show-ngraphs (output the table of ngraphs and exit)
  -h|--help (this help screen)
  
  
EOM
  exit (scalar @_) ;
}

my @files = ();
my $verbose = 0;
my $ngraph = 2;
my $count = 100;
my $lower = 1;
my $pop = 0;
my $extract = 0;
my $outgraph = 0;
my $paras = 0;
my $format = 2;

while ($ARGV=$ARGV[0]) {
  my $myarg = $ARGV;
  if ($ARGV eq '-f' or $ARGV eq '--file') {
    shift @ARGV;
    if (!($ARGV = $ARGV[0])) { fail_usage ("$myarg needs an argument"); }
    if ($ARGV =~ /^-/) {fail_usage ("$myarg must be followed by an argument"); }
    if (! -e $ARGV) {fail_usage ("$myarg file ($ARGV) does not exist"); }
    if (! -r $ARGV) {fail_usage ("$myarg file ($ARGV) not readable"); }
    push (@files, $ARGV);
  }
  elsif ($ARGV eq '-g' or $ARGV eq '--ngraph') {
    shift @ARGV;
    if (!($ARGV = $ARGV[0])) { fail_usage ("$myarg needs an argument"); }
    if ($ARGV =~ /^-/) {fail_usage ("$myarg must be followed by an argument"); }
    if ($ARGV !~ /^\d{1,2}$/) {fail_usage ("$myarg ($ARGV) needs a small number"); }
    if ($ARGV > 10) {fail_usage ("$myarg ($ARGV) too large"); }
    $ngraph = $ARGV;
  }
  elsif ($ARGV eq '-c' or $ARGV eq '--count') {
    shift @ARGV;
    if (!($ARGV = $ARGV[0])) { fail_usage ("$myarg needs an argument"); }
    if ($ARGV =~ /^-/) {fail_usage ("$myarg must be followed by an argument"); }
    if ($ARGV !~ /^\d{1,4}$/) {fail_usage ("$myarg ($ARGV) needs a small number"); }
    if ($ARGV > 1000) {fail_usage ("$myarg ($ARGV) too large"); }
    $count = $ARGV;
  }
  elsif ($ARGV eq '-p' or $ARGV eq '--popular') {
    shift @ARGV;
    if (!($ARGV = $ARGV[0])) { fail_usage ("$myarg needs an argument"); }
    if ($ARGV =~ /^-/) {fail_usage ("$myarg must be followed by an argument"); }
    if ($ARGV !~ /^\d{1,5}$/) {fail_usage ("$myarg ($ARGV) needs a small number"); }
    if ($ARGV > 100000) {fail_usage ("$myarg ($ARGV) too large"); }
    $pop = $ARGV;
  }
  elsif ($ARGV eq '-C' or $ARGV eq '--paragraphs') {
    shift @ARGV;
    if (!($ARGV = $ARGV[0])) { fail_usage ("$myarg needs an argument"); }
    if ($ARGV =~ /^-/) {fail_usage ("$myarg must be followed by an argument"); }
    if ($ARGV !~ /^\d{1,5}$/) {fail_usage ("$myarg ($ARGV) needs a small number"); }
    if ($ARGV > 1000) {fail_usage ("$myarg ($ARGV) too large"); }
    $paras = $ARGV;
  }
  elsif ($ARGV eq '-m' or $ARGV eq '--format') {
    shift @ARGV;
    if (!($ARGV = $ARGV[0])) { fail_usage ("$myarg needs an argument"); }
    if ($ARGV =~ /^-/) {fail_usage ("$myarg must be followed by an argument"); }
    if ($ARGV !~ /^\d$/) {fail_usage ("$myarg ($ARGV) needs a small number"); }
    if ($ARGV == 1 or $ARGV == 2) {fail_usage ("$myarg ($ARGV) 1 or 2"); }
    $format = $ARGV;
  }
  elsif ($ARGV eq '-l' or $ARGV eq '--lower' ) { $lower = 1 ; }
  elsif ($ARGV eq '-u' or $ARGV eq '--upper' ) { $lower = 2 ; }
  elsif ($ARGV eq '-L' or $ARGV eq '--keep-case' ) { $lower = 0 ; }
  elsif ($ARGV eq '-x' or $ARGV eq '--extract-text' ) { $extract = 1 ; }
  elsif ($ARGV eq '-y' or $ARGV eq '--show-ngraphs' ) { $outgraph = 1 ; }
  elsif ($ARGV eq '-v' or $ARGV eq '--verbose' ) { $verbose ++ ; }
  elsif ($ARGV eq '-h' or $ARGV eq '--help' ) { fail_usage ; }
  elsif ($ARGV =~ /^-/ ) { fail_usage " invalid option ($ARGV)"; }
  else { fail_usage "Additional arguments", @ARGV; }
#  else { last ; }
  shift @ARGV;
}

if ($verbose) {
  print "args were : ";
  print " -f:\n    ";
  print join ("\n    ",@files), "\n";
  print " -v ($verbose)"; 
  print " -g ($ngraph)"; 
  print " -c ($count)"; 
  print " -C ($paras)"; 
  print " -l|-u|-L ($lower)"; 
  print " -x ($extract)"; 
  print " -y ($outgraph)"; 
  print " -m ($format)"; 
  print "\n";
#  print "additional arguments were: ", join (':', @ARGV), "\n";
}

my $content="";

for my $file (@files) {
  my $FILE;
  if (!open ($FILE, '<', $file)) { print  "Couldn't read file ($file)\n"; }
  else {
    $content .= do { local $/ = undef; <$FILE>; };
    close $FILE;
    $content .= "\n\n";
  }
}
if (!$content) { fail_usage "no file data found"; }

my $formpat = qr/\n\n|\r\r|\r\n\r\n/;
if ($format == 1) { $formpat = qr/\r\n|\n|\r/; }

my @lines = split ($formpat, $content);
# this is for text files that have two line feeds for a paragraph
# like the shakespeare file
# read into an array of paragraphs 
#{ local $/="\n\n"; @lines = <$FILE>; }

map {
  # a word character, non grammatical word chars, another word -> replace with space
  s/([a-zA-Z0-9])[^!\&',\.;\?a-zA-Z0-9 \t\s\n-]+([a-zA-Z0-9])/$1 $2/g; 
  # non gramatical word char -> remove
  s/[^!\&',\.;\?a-zA-Z0-9 \t\s\r\n-]+//g; 
  # there were rows of dashes - remove
  s/---+//g;
  # -- is used for long dash
  s/--/-/g;
  # compress bunches of white space
  s/[ \s\t\n\r]+/ /sg;
  # trim beginning and end
  s/^ +//;
  s/ +$//;
} @lines;

# remove lines with no printable characters 
my @newlines = grep { /[^\s]/ }  @lines;
# make all lower case
if ($lower==1) { map {  s/.*/\L$&\E/g; } @newlines; }
# make all upper case
elsif ($lower==2) { map {  s/.*/\U$&\E/g; } @newlines; }
# join lines together with new line char
# so we can include paragraph endings as a valid character
my $string = join ("\n", @newlines);

if ($extract) {
  print $string, "\n";
  exit;
}

my $length = length $string;
my %nfreq=();
my $ntotal = 0;
# here is wheere we count ngraphs
for my $pos (0 .. $length-$ngraph) {
  my $s = substr $string, $pos, $ngraph;
  $nfreq{$s} ++;
  $ntotal++;
}

if ($verbose and $pop) {
  print "before prune ";
  my $words=0; for (values %nfreq) { $words += $_; }
  print "letters=($ngraph), total words=($ntotal), wc=($words) ngraphs=(", scalar keys %nfreq,")\n";
}

if ($pop) {
  # remove entries lower freqency (popularity) than $pop
  while (my ($key, $value) = each %nfreq) {
    if ($pop >= $value) { delete $nfreq{$key}; $ntotal-= $value; } 
  }
}

if ($outgraph) {
  my $ll=0;
  for (sort {($nfreq{$b} <=> $nfreq{$a}) || ($b cmp $a)} keys %nfreq) {
    print "($_)=$nfreq{$_} \n";
    $ll++;
  }
  exit;
}

if ($verbose) {
  if ($pop) { print "after prune "; }
  my $words=0; for (values %nfreq) { $words += $_; }
  print "letters=($ngraph), total words=($ntotal), wc=($words) ngraphs=(", scalar keys %nfreq,")\n";
  if ($verbose>2) {
    my $ll=0;
    for (sort {($nfreq{$b} <=> $nfreq{$a}) || ($b cmp $a)} keys %nfreq) {
      print "($_)=$nfreq{$_} \n";
      $ll++;
      if ($verbose<4 and $ll>30) { last; }
    }
  }
}

if (scalar keys %nfreq <= 1) { fail_usage "not enough frequent words to continue"; }

my $choice="";
my $counted=0;
my $parased=$paras;

#if ($verbose) { print " ngraphs=($ntotal) \n"; }
#while ($counted < $count) {
while (($paras and ($parased > 0)) or ($counted < $count)) {
  my $rand = int rand $ntotal;
  if ($verbose>1) { print " count($count) counted($counted) rand = ($rand) \n"; }
  my $lastkey="";
  my $tried=0;
  keys %nfreq; # reset the each interator
  while (my ($key, $weight) = each %nfreq ) {
    $tried++;
    if (($rand -= $weight) < 0) {
      $lastkey = $key;
      if ($paras and $key =~ /\n/) { $parased--; }
      $choice.=$key;
      $counted+=$ngraph;
      last;
    }
  } 
  if ($verbose>1) {
    print "  tried=($tried) rand=($rand) key=($lastkey) freq=", $lastkey?$nfreq{$lastkey}:"", " \n"; 
  }
}

if ($verbose) { print " count($count) counted($counted) paras=($paras)\n"; }
if ($verbose) { print "debug finished\n"; }

print "$choice\n";
