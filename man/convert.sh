#!/bin/bash
for f in *.1.md; do pandoc "$f" -s -t man -o "${f%.md}"; done
