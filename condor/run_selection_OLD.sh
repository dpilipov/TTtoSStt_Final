#!/bin/bash
echo "Run script starting"
source /cvmfs/cms.cern.ch/cmsset_default.sh
xrdcp root://cmseos.fnal.gov//store/user/dpilipov/THBoostedAllHad.tgz ./
scramv1 project CMSSW CMSSW_11_1_4
tar -xzvf THBoostedAllHad.tgz
rm THBoostedAllHad.tgz
rm *.root

mkdir tardir; cp tarball.tgz tardir/; cd tardir/
tar -xzf tarball.tgz; rm tarball.tgz
cp -r * ../CMSSW_11_1_4/src/PostAPV/TopHBoostedAllHad/; cd ../CMSSW_11_1_4/src/
echo 'IN RELEASE'
pwd
ls
eval `scramv1 runtime -sh`
cd PostAPV/
#rm -rf timber-env
python -m virtualenv timber-env
source timber-env/bin/activate
cd TIMBER
source setup.sh
cd ../TopHBoostedAllHad

echo python TTselection.py $*
python TTselection.py $*

xrdcp -f rootfiles/TTselection_*.root root://cmseos.fnal.gov//store/user/dpilipov/topHBoostedAllHad/selection/

