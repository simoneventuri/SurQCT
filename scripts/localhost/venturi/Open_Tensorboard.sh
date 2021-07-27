#!/bin/bash

/usr/bin/open -a "/Applications/Google Chrome.app" 'http://localhost:6007'
ssh -t -L localhost:6007:localhost:6006 venturi@128.174.245.172
