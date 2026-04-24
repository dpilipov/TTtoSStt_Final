#cmssw-el8 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs
#+DesiredOS = "SL7"
#cmssw-el7 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs
cd $CMSSW_BASE/../
# DP EDIT....
#       --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/TH*.root \
tar --exclude-caches-all --exclude-vcs --exclude-caches-all --exclude-vcs -cvzf THBoostedAllHad.tgz \
        --exclude=tmp --exclude=.scram --exclude=.SCRAM --exclude=CMSSW_11_1_4/src/timber-env \
        --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/THsnap*.root \
        --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/THsele*.root \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/logs \
	--exclude=CMSSW_11_1_4/src/TIMBER/docs \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/plots \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/rootfiles/*.root \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/rootfilesMClead/*.root \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/rootfilesMCsublead/*.root \
        --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/rootfilesSIGleading/*.root \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/rootfilesSIGsubleading/*.root \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/*.pdf \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/Nminus*.* \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/print*.py \
	--exclude=CMSSW_11_1_4/src/TTtoSStt \
	--exclude=CMSSW_11_1_4/src/TTtoSStt_Saa \
        --exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/Nminus* \
	--exclude=CMSSW_11_1_4/src/TopHBoostedAllHad/Analy*.docx \
	CMSSW_11_1_4
# also edited the following for my directory (top with capital Top)
xrdcp -f THBoostedAllHad.tgz root://cmseos.fnal.gov//store/user/$USER/THBoostedAllHad.tgz
cd $CMSSW_BASE/src/TopHBoostedAllHad/
