#!/bin/bash

/usr/bin/open -a "/Applications/Google Chrome.app" 'http://localhost:8889'
ssh -t -L localhost:8889:localhost:8888 venturi@128.174.245.172
