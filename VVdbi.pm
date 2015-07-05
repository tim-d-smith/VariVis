package VVdbi;

use strict;
use warnings;
use DBI;
use VVIni;

sub Query {
        my($strSQL,$queCol,$queTerm) = @_;
        
        #Test attributes
        $queTerm = "" unless defined $queTerm;
        $queCol = "" unless defined $queCol;
        die "No SQL Query passed. Stopped " unless defined $strSQL;

        #Get varivis.ini settings
        my $options = VVIni->new(filename=>'varivis.ini') || die "Could not access configuration file. Try running install again. Stopped ";

        #Define array to hold results
        my @results;


        #Define DB handle
        my $dbh;
        
        my $DBname; my $DBHost; my $DBPort;my $dsn;
        
        #Connect to database defined in varivis.ini
        if($options->get_value("DBtype") eq "CSV") {
                eval {
                        my $SepChar = $options->get_value("SepChar");
                        my $CSVPath = $options->get_value("CSVPath");
                        $dbh = DBI->connect(qq{DBI:CSV:csv_sep_char=\\$SepChar;f_dir=$CSVPath}) or die;
                        $dbh->{RaiseError} = 1;
                        $dbh->{PrintError} = 0;
                        $dbh->{'csv_tables'}->{"default"} = { 'file' => $options->get_value("CSVfile")};

                };
                die "Unable to connect to CSV file. Check the path and file name are correct. Stopped " if $@;

        } elsif($options->get_value("DBtype") eq "mySQL") {
                eval {
                        $DBname = $options->get_value("DBname");
                        $DBHost = $options->get_value("DBhost");
                        $DBPort = $options->get_value("port");
                        $dsn = "DBI:mysql:database=$DBname;host=$DBHost;port=$DBPort";
                        $dbh = DBI->connect($dsn, $options->get_value("user"), $options->get_value("pass")) or die;
                        $dbh->{RaiseError} = 1;
                        $dbh->{PrintError} = 0;
                };
                die "Unable to connect to MySQL server. Check the service is running and the database name, host, port, username and password are correct. Stopped " if $@;
                
        } elsif($options->get_value("DBtype") eq "PostgresSQL") {
                eval {
                        $DBname = $options->get_value("DBname");
                        $DBHost = $options->get_value("DBhost");
                        $DBPort = $options->get_value("port");
                        $dsn = "DBI:Pg:database=$DBname;host=$DBHost;port=$DBPort";
                        $dbh = DBI->connect($dsn, $options->get_value("user"), $options->get_value("pass")) or die;
                        $dbh->{RaiseError} = 1;
                        $dbh->{PrintError} = 0;
                };
                die "Unable to connect to PostgresSQL server. Check the server is working and the database name, host, port, username and password are correct. Stopped " if $@;
                
        } elsif($options->get_value("DBtype") eq "Oracle") {
                eval {
                        $DBname = $options->get_value("DBname");
                        $DBHost = $options->get_value("DBhost");
                        $DBPort = $options->get_value("port");
                        $dsn = "dbi:Oracle:$DBname";
                        $dbh = DBI->connect($dsn, $options->get_value("user"),$options->get_value("pass")) or die;
                        $dbh->{RaiseError} = 1;
                        $dbh->{PrintError} = 0;
                };
                die "Unable to connect to Oracle server. Check the server is working and the database name, host, port, username and password are correct. Stopped " if $@;
        }

        $@ = '';
        eval {
                #prepare and execute the SQL statement
                if($queCol ne "") {$queTerm = $dbh->quote($queTerm);$strSQL .= " WHERE $queCol = $queTerm"}

                my $sth = $dbh->prepare($strSQL) or die;
                $sth->execute() or die;

                while (my $row = $sth->fetchrow_hashref) {
                        push @results, {%$row};
                }

                $sth->finish;
                $dbh->disconnect();
        };
        if ($@) { die 'Unable to query database. We\'re connected, but not getting any data. Check that you correctly specified the column headings during installation. The query we\'re trying to execute is <code>'.$strSQL.'</code>. Stopped ';}
        
        return @results;
}

1;
