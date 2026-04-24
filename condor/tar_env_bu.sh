cmssw-el8 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs
cd $CMSSW_BASE/../
# DP EDIT....
tar --exclude-caches-all --exclude-vcs --exclude-caches-all --exclude-vcs -cvzf THBoostedAllHad.tgz CMSSW_11_1_4 --exclude=tmp --exclude=.scram --exclude=.SCRAM --exclude=CMSSW_11_1_4/src/timber-env --exclude=CMSSW_11_1_4/src/topHBoostedAllHad/TH*.root --exclude=CMSSW_11_1_4/src/topHBoostedAllHad/logs --exclude=CMSSW_11_1_4/src/TIMBER/docs --exclude=CMSSW_11_1_4/src/topHBoostedAllHad/plots --exclude=CMSSW_11_1_4/src/topHBoostedAllHad/rootfilesMClead"
#tar --exclude-caches-all --exclude-vcs --exclude-caches-all --exclude-vcs -cvzf THBoostedAllHad.tgz CMSSW_11_1_4 --exclude=tmp --exclude=".scram" --exclude=".SCRAM" --exclude=CMSSW_11_1_4/src/timber-env --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/TH*.root --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/logs --exclude=CMSSW_11_1_4/src/TIMBER/docs --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/plots
# also edited the following for my directory (top with capital Top)
xrdcp -f THBoostedAllHad.tgz root://cmseos.fnal.gov//store/user/$USER/THBoostedAllHad.tgz
cd $CMSSW_BASE/src/TopHBoostedAllHad/
