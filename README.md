Integration between GenAV Flight Office and Wi-Flight
=====================================================

Overview
--------

[Wi-Flight](https://www.wi-flight.net) is an automated flight data
collection and monitoring system with web-based flight playback
capability. Wi-Flight uses flight data recorders aboard aircraft that
upload their data over the Internet.

[GenAV Flight Office](http://www.genavsystems.com/) is a complete
office management solution for flight schools.

This connector implements one-way integration between these two systems.
Bookings for aircraft are downloaded from GenAV Flight Office and
imported into Wi-Flight as reservations. Wi-Flight's normal matching
between flights and reservations takes place so that when Wi-Flight
flights are recorded and uploaded, they are associated with the
corresponding Flight Office booking.

The connector is currently in early stages of development and is
missing the key feature of enabling the system to offer web-based
access to Wi-Flight flights to Flight Office users where the Wi-Flight
flight and Flight Office booking have been associated together.

How to use
----------

Currently the connector does not have the ability to run as a daemon
and passively receive notifications from Flight Office concerning
new, changed, or deleted bookings. Instead, the connector must run
at regular intervals and probe for new bookings.

The more often the connector is run, the more promptly new or changed
bookings will be imported to Wi-Flight, but running the connector too
often will result in excessive network traffic between the connector
and Flight Office, and excessive load on Flight Office. There is no
communication between the connector and Wi-Flight if the connector is
run and there are no new or changed bookings detected.

The connector should be run as a cron job (scheduled job) at the
chosen interval.

The connector requires the following software to be installed:

- Python (version 2.7 tested)
- [SQLAlchemy](http://www.sqlalchemy.org/), Debian package python-sqlalchemy
- Any local database that is compatible with SQLAlchemy (MySQL tested)
- [pywiflight](https://github.com/vandry/pywiflight)
- [PycURL](http://pycurl.sourceforge.net/), Debian package python-pycurl

After software is installed:

- (OPTIONAL) Create a dedicated user account for use by the connector.
If no dedicated user account shall be used then choose which existing
user account will run the connector.
- Create database schema and credentials (username and password) for
the connector to access its local database. This is probably required
for every database type except SQLite.
- Create a configuration file `.genav_connector.dburi` in the user's
home directory containing a SQLAlchemy URL for database access. An
example for MySQL is

mysql://username:password@localhost/database-name?charset=utf8

- Create the database tables (and test database access at the same time!)
by running the script `create_schema`.
- Create directories `genav_config` and `.genav_password` in the user's
home directory.
- For each organization whose bookings the connector will be responsible
for importing, create a configuration file in `~/genav_config` named
after the company code (sCompCode), e.g. `~/genav_config/ABC123`.
The configuration file should contain something like this:

    user <Wi-Flight API username>
    url http://flight-office-download-base-url-supplied-by-genav
    domain <domain-attached-to-reservations-supplied-by-wi-flight>

- There should also be a file with the same name in ~/.genav_password with
the Wi-Flight API password on one line.
- Create a cron job to run the `pull_updates` script at chosen intervals
with a single command line argument: the company code
(e.g. `pull_updates ABC123`)
