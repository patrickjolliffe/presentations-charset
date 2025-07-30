#!/usr/bin/perl
use strict;
use warnings;
use DBI;
use Encode qw(is_utf8 encode_utf8);

# DB connection
my $dsn  = "dbi:Oracle://localhost:1521/freepdb1";
my $user = 'pdbadmin';
my $pass = 'pdbadmin';

my $dbh = DBI->connect($dsn, $user, $pass, {
    RaiseError => 1,
    AutoCommit => 1,
});

my $sth = $dbh->prepare("SELECT name FROM dogs WHERE name LIKE ? ORDER BY name");
$sth->execute($ARGV[0] // '%');

my $total = 0;
my $bad = 0;

while (my ($name) = $sth->fetchrow_array) {
    $total++;
    my $hex = unpack("H*", $name);
    my $hex_spaced = join(' ', $hex =~ /../g);
    my $byte_count = length($hex) / 2;
    if ($hex =~ /(^|..)bf(..|$)/i) {
        $bad++;
        print "Bad $name [$hex_spaced] ($byte_count bytes)\n";
    } else {
        print "Good $name [$hex_spaced] ($byte_count bytes)\n";
    }
}

print "NLS_LANG=$ENV{NLS_LANG}\n";
my $good = $total - $bad;
print "✅ Good dogs: $good\n";
print "❌ Bad dogs: $bad\n";

$sth->finish;
$dbh->disconnect;