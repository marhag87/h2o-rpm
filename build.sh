#!/bin/bash

set -e

if [[ $1 == "-y" ]]; then
  noninteractive="-y"
fi

sudo=$(which sudo 2>/dev/null || echo -n)

topdir=$(git rev-parse --show-toplevel)
version=$(awk '/^Version/ {print $2}' ${topdir}/h2o.spec)
mkdir -p rpmbuild/{RPMS,SPECS,SOURCES,SRPMS,BUILD,BUILDROOT}
cp h2o.1 h2o.conf h2o.logrotate h2o.service rpmbuild/SOURCES/
cp h2o.spec rpmbuild/SPECS/
wget https://github.com/h2o/h2o/archive/v${version}.tar.gz -O $topdir/rpmbuild/SOURCES/h2o-$version.tar.gz
$sudo dnf builddep $noninteractive $topdir/rpmbuild/SPECS/h2o.spec
rpmbuild --define "_topdir $topdir/rpmbuild" -bb $topdir/rpmbuild/SPECS/h2o.spec
mv $topdir/RPMS/x86_64/* $topdir/
rm -rf rpmbuild
