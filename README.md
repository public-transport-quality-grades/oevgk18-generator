# OeVGK18 Generator

[![Build Status](https://travis-ci.org/public-transport-quality-grades/oevgk18-generator.svg?branch=master)](https://travis-ci.org/public-transport-quality-grades/oevgk18-generator)

The OeVGK18 Generator is a Python application to generate public transport quality gradings ("ÖV-Güteklassen").

It implements the specification OeVGK18, which you can find here: [public-transport-quality-grades/oevgk18-specification](https://github.com/public-transport-quality-grades/oevgk18-specification)

## Research

This project was created as part of a thesis for the University of Applied Sciences Rapperswil (HSR).
The full thesis text is available here: [public-transport-quality-grades/thesis](https://github.com/public-transport-quality-grades/thesis)

## Acknowledgements

* [geOps](http://gtfs.geops.ch/) for converting the public transit schedule to the GTFS format
* [Swisstopo](https://www.swisstopo.admin.ch/) for the digital elevation model
* [pgRouting](https://pgrouting.org/) for pedestrian routing
* [OpenStreetMap](https://www.openstreetmap.org) for the routing data

## Setup

In order to run this application, we set up a [Docker](https://www.docker.com/) environment to automate all the database setup and execution.
Head over to the [Docker README](https://github.com/public-transport-quality-grades/oevgk18-generator/tree/master/docker) for a step-by-step guide.