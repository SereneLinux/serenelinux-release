# Makefile for source rpm: fedora-release
# $Id: Makefile,v 1.1 2004/10/22 05:29:25 notting Exp $
NAME := fedora-release
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
