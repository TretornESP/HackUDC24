#!/bin/sh
/usr/local/bin/buildbot-worker start .
tail -f /worker/twistd.log