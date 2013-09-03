#!/bin/bash

VERSION_autocorrelation=1.1
URL_autocorrelation=http://localhost/download/autocorrelation-$(echo $VERSION_autocorrelation).tar.gz
DEPS_autocorrelation=(python)
MD5_autocorrelation=85a7dc45b86716e0aa642381835bbc9b
BUILD_autocorrelation=$BUILD_PATH/autocorrelation/$(get_directory $URL_autocorrelation)
RECIPE_autocorrelation=$RECIPES_PATH/autocorrelation

function prebuild_autocorrelation() {
	true
}

function build_autocorrelation() {
	cd $BUILD_autocorrelation

	push_arm

	try $BUILD_PATH/python-install/bin/python.host setup.py install -O2
	
	pop_arm
}

function postbuild_autocorrelation() {
	true
}
