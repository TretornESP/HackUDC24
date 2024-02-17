#!/bin/sh
buildbot create-master .
buildbot upgrade-master .
buildbot start .
tail -f twistd.log