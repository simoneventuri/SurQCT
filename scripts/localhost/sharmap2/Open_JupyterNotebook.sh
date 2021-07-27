#!/bin/bash

/usr/bin/open -a "/Applications/Google Chrome.app" 'http://localhost:8889'
ssh -t -L localhost:8889:localhost:8888 sharmap2@mimmo.ae.illinois.edu
