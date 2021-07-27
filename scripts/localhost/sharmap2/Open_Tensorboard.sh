#!/bin/bash

/usr/bin/open -a "/Applications/Google Chrome.app" 'http://localhost:6007'
ssh -t -L localhost:6007:localhost:6006 sharmap2@mimmo.ae.illinois.edu
