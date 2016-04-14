#!/usr/bin/perl -w

use strict;

my $dirfile = "";
$dirfile=$ARGV[0];
if (!$dirfile) {
  $dirfile = $ENV{'DIRFILE'};
  if (!$dirfile) { $dirfile = "~/.dirs_bash.$ENV{'USER'}\@$ENV{'HOST'}"; }
}
if (! -r $dirfile) { exit; }
#my $dirtemp = $ENV{'DIRTEMP'};
#if (!$dirtemp) { $dirtemp = "$dirfile.$$"; }
my $dirsize = $ENV{'DIRSIZE'};
if (!$dirsize) { $dirsize = 500; }

$dirsize=4;
my @dirs;
my %dir;
if (-r $dirfile) { if (open (DIR, $dirfile)) { @dirs = <DIR>; close DIR; } }
#if (-r $dirtemp)
#  { if (open (DIR, $dirtemp)) { push (@dirs, <DIR>); close DIR; } }

#@dirs = qw( a b c d a f e f e f e);
if (!scalar @dirs) { exit; }

my $count=0;
my @dirs2;
while ($_ = pop @dirs) {
  if ($count >= $dirsize) { last; }
  chomp;
  if (defined($dir{$_})) { next; }
  $dir{$_} = 1;
  unshift @dirs2, $_;
  $count++;
}

if ( scalar @dirs2) {
  if (open (DIR, ">$dirfile")) {
    map { print DIR $_, "\n"; } @dirs2;
    close DIR;
  }
}

#if (-r $dirtemp) { unlink $dirtemp; }
