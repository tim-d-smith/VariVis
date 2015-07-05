#VariVis
The VariVis system is a collection of Perl scripts designed to provide a basic set of sequence and variation visualisation tools specifically for LSDBs. It is designed to work in parallel with a database's existing user interface and storage and retrieval back-end. For this reason, VariVis has been designed so that it can gather data from a wide variety of sources including Database Management Systems (DBMSs) such as MySQL, Oracle, PostgreSQL through to flat-file repositories such as Comma or Tab delimited text files. Gene sequences and annotations can be provided to the software either locally, using a large number of sequence file formats, such as FASTA, BSML and Tinyseq; or VariVis can be directed to automatically retrieve such data from any of several online sequence databases such as GenBank or EMBL.

VariVis is capable of producing two different conceptual views based on the sequence and variation data provided. The first displays the gene sequence and overlays positions where variation is present. Clicking the variant symbols provides the user with a brief overview of the data extracted from the database, from which the user can link to the variant entry in the database, or perform simple PubMed and Google Scholar searches to find published articles on the variant.

The second view, the "Gel View," has the same functionality as the first viewing option, but this time orientates the sequence vertically, allowing for an unbroken stream of data. Theoretically, it is possible that any given nucleotide in a gene can be mutated to any other nucleotide base, deleted entirely, or have an adjacent insertion. The "Gel View" displays all possible nucleotide combinations for each position, highlighting the nucleotides present in the reference sequence and any variations in contrasting colours.

In both views, the software also displays any structural annotations, such as promoter sequences, poly-A sites, and UTRs that are present in the sequence file being used. The software also provides access to the raw sequence data, allowing users to copy or download the entire sequence, or specific chunks, negating the need to navigate to a dedicated sequence database.

VariVis can be run on any web server capable of executing Perl 5.6.1 CGI scripts. The system makes use of the external BioPerl, DBI and CGI modules, and these must be installed prior to use. Installation of both modules can be performed using either the CPAN or ActiveState Package Managers.

##Installation

Make sure you have Perl installed on your web server, as well as the required external code modules. A list of the external modules and installation instructions can be found below

Extract the VariVis files to your cgi-bin directory. The folder called 'varivis' contains style-sheets and some simple javascript files and may need to be placed in your root htdocs folder.

There are seven files with .cgi extensions. The first line of each of these scripts needs to point to the location of Perl on your server. The files are configured for the most common web server setups and currently read #!/usr/bin/perl. You may need to change the first line of each file to point to the correct location of Perl for your particular setup. Windows users should use the form #!C:/Perl/bin/perl.

Navigate to the install.cgi file using your web-browser and fill out the options listed on the page. Once complete your installation will be tested, as will the connection to the variation and sequence data. You should configure your web server to block access to the varivis.ini file that the install.cgi script generates. A .htaccess for Apache and compatible servers is included in the VariVis package. Users of other server packages should consult their server documentation. This step is extremely important for databases running on mySQL to prevent your mySQL account details being released.

Comprehensive help on the individual steps in the installation script, can be found below.

###External Modules

VariVis is heavily dependant on a number of external code modules in order to function. These need to be installed prior to VariVis being installed. The sections below briefly outline the installation for these modules in both Linux and Windows environments as well as providing links to the official documentation. Most Perl distributions already have CGI.pm and the Perl DBI installed, but it pays to check. BioPerl will almost definitely have to be installed.

####BioPerl Modules

CPAN Package Manager (Linux & Windows):
>perl -MCPAN -e shell
>install S/SE/SENDU/bioperl-1.5.2_102.tar.gz

ActiveState Package Manager (Windows):
Type the following at a command prompt
>ppm-shell
>search bioperl
>install #
(where the number matches the bioperl version needed)

More detailed instructions can be found at the BioPerl Website: http://www.bioperl.org/wiki/Installing_BioPerl

####DBI

CPAN Package Manager (Linux & Windows):
>perl -MCPAN -e shell
>install Bundle::DBI

ActiveState Package Manager (Windows):
Type the following at a command prompt
>ppm-shell
>install DBI

You will also need the appropriate database driver (see below)

More detailed instructions can be found at the Perl DBI Website: http://dbi.perl.org

####CGI

CPAN Package Manager (Linux & Windows):
>perl -MCPAN -e shell
>install CGI

ActiveState Package Manager (Windows):
Type the following at a command prompt
>ppm-shell
>install CGI

####Database Drivers

The database drivers are Perl Modules that tell the Perl DBI how to connect to a specific type of database. They can be installed by searching for "DBD" and the appropriate extension in both the ActiveState PPM and CPAN repositories.

You will require the DBD module for your specific database systems. Below is a list of the currently supported database systems in VariVis and the name of the corresponding driver.
* Comma Separated Value (CSV) Files	DBD::CSV
* MySQL (DBD::mysql)
* Oracle	(DBD::Oracle)
* PostgresSQL (DBD::Pg)

A list of the database drivers currently installed on your server can be obtained by running the dbd.cgi script that is included in the VariVis package.

###Program Settings

####Relative path to 'varivis' folder

The VariVis folder is included in the VariVis package and contains images and style-sheets to correctly format the program's output. The default setting for this option is varivis, or, that the folder is located in the same directory as the .cgi files (usually cgi-bin). However, some web servers do not like having non-cgi files in the cgi-bin directory. If this is the case with your server, move the folder to the html root folder (e.g. /htdocs/) and specify the relative path from your cgi directory to the VariVis folder in the html root directory. In most server set-ups, this is ../varivis.

####Reference Sequence
#####Gene Symbol

This option specifies the symbol of the gene being displayed. This is primarily needed to make sure we use the right information from the reference sequence file or database. It is a case sensitve value, so make sure you use the right cases (generally all uppercase).

#####Reference sequence location

This options defines where VariVis goes looking for sequence data. Choose local for a file stored on the web server, Genbank, RefSeq, or EMBL for either of those databases. As VariVis will query the file/database every time it is run, it is strongly recommended that you use a local file to cut down VariVis' run time, as well as avoiding unecessary load on the NCBI/EBI servers.

#####Accession Number or filename

This is either the Accession and Version numbers (e.g. AF307851.1) for the remote sequence record, or the filename of the local sequence file.

#####LOCAL sequence file path

The absolute path to the local sequence file on the web server. This value is ignored for remote sequence files.

#####LOCAL sequence file format

The format of the local sequence file. This value is ignored for remote sequence files.

####Variation Data

#####Database type

This option specifies the database system type that stores the variation data.

#####Database fields

These settings specify where VariVis looks within your database for the information it needs. In the case of CSV files, these will be the column headers - the records in the first row. For relational databases, the values are the field names within the database tables.
PLEASE NOTE: White space (e.g. spaces) within field names is not permitted and may result in VariVis to stop working.

Varivis makes use of the following data:
- **DNA Level Variant Name Field** Variant described at the DNA level using HGVS standard nomenclature
- **Protein Level Variant Name Field** Change to protein sequence as a result of gene sequence variation described using 						HGVS standard nomenclature
- **Restriction Enzyme Site Change Field** Any change to Restriction enzyme sites.
- **Phenotype Description Field** Phenotype description.
- **Remarks Field** Comments and remarks.
- **Pubmed ID Field** Pubmed ID of original publication reporting the variant.

####CSV Settings

#####CSV File Path

Absolute path to the directory containing the CSV file storing the variation data on the web server (e.g. C:/htdocs/). This value is ignored for relational databases.


#####CSV Filename

Filename of CSV file. This value is ignored for relational databases.

#####CSV separating character

Character used to separate values within records. Defaults to ','. This value is ignored for relational databases.

####MySQL/Oracle/Postgres Settings

#####Database name

The name of the database on the MySQL/Oracle/Postgres server that contains the table storing the variation data. If you don't know your database name, contaact your database administrator. This value is ignored for local flat-files.

#####Database table

The table within the specified database that holds the variation data. This value is ignored for local flat-files.

#####Database host

The host name of the database server. In most cases this will be localhost. This value is ignored for local flat-files.

#####Database port

The port on which the database server is listening. The default port for MySQL is 3306. This value is ignored for local flat-files.

#####Username

The username of a database user accout with access to the variation database. VariVis only requires select privileges, so it is recommended that a unique user account be created for VariVis to use. This value is ignored for local flat-files.

#####Password

The password of the database user account. This value is ignored for local flat-files.
