#!/usr/bin/env zsh

cmake -H. -Bbuild && make -C build
mv ./build/videoAnalysis ./videoAnalysis
