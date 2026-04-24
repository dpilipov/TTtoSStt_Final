'''
Cutflow information is stored differently in snapshots and selection files. 
Snapshots: stored in Events TTree
	NPROC, NFLAGS, NJETS, NPT, NKIN
Selection: stored in Histogram
	nTop_CR, nTop_SR
	higgsF_{}, higgsL_{}, higgsP_{}
'''
import ROOT
import glob, os
from argparse import ArgumentParser
from collections import OrderedDict
import numpy as np

def generateCutflow(setName, HT=900, selection=True):
    '''
	main function to generate the cutflow from snapshot and/or selection for a set
	setName   [str]  = set name as seen in snapshot/selection files
	selection [bool] = False if only snapshot, True if both
    '''
#DP EDIT
    selection = True
    print(selection)
    if selection:
#	snapVars = OrderedDict([('NPROC',0.),('NFLAGS',0.),('NJETS',0.),('NJETID',0),('NPT',0.),('NKIN',0.),('NDELTAETA',0.),('PreLepVeto',0.),('PostLepVeto',0.),('nTop_CR',0.),('higgsF_CR',0.),('higgsL_CR',0.),('higgsP_CR',0.),('nTop_SR',0.),('higgsF_SR',0.),('higgsL_SR',0.),('higgsP_SR',0.)])
#       snapVars = OrderedDict([('NPROC',0.),('NFLAGS',0.),('NJETS',0.),('NPHOTONS',0.),('NJETID',0),('NPT',0.),('NKIN',0.),('PreLepVeto',0.),('PostLepVeto',0.),('Tot_CR',0.),('FF_CR',0.),('F_CR',0.),('P_CR',0.),('Tot_SR',0.),('FF_SR',0.),('F_SR',0.),('P_SR',0.)])
       snapVars = OrderedDict([('NPROC',0.),('NFLAGS',0.),('NJETS',0.),('NPHOTONS',0.),('NJETID',0),('NPT',0.),('NKIN',0.),('NPHOTONKIN',0.),('NPHOTONNOTELEC',0.),('NPHOTONINBARR',0.),('PreLepVeto',0.),('PostLepVeto',0.),('Tot_CR',0.),('FF_CR',0.),('F_CR',0.),('P_CR',0.),('Tot_SR',0.),('FF_SR',0.),('F_SR',0.),('P_SR',0.)])
    else:
#	snapVars = OrderedDict([('NPROC',0.),('NFLAGS',0.),('NJETS',0.),('NJETID',0),('NPT',0.),('NKIN',0.),('NDELTAETA',0.),('PreLepVeto',0.),('PostLepVeto',0.)])
       snapVars = OrderedDict([('NPROC',0.),('NFLAGS',0.),('NJETS',0.),('NPHOTONS',0.),('NJETID',0),('NPT',0.),('NKIN',0.),('NPHOTONKIN',0.),('NPHOTONNOTELEC',0.),('NPHOTONINBARR',0.),('PreLepVeto',0.),('PostLepVeto',0.)])

    years = OrderedDict([('16',snapVars.copy()), ('16APV', snapVars.copy()), ('17', snapVars.copy()), ('18', snapVars.copy())])
#    years = OrderedDict([('16',snapVars.copy())]) 

    # do snapshots
    for year, varDict in years.items():
#      if (year==16):
	if not os.path.exists('dijet_nano/{}_{}_snapshot.txt'.format(setName,year)):
	    pass
	fileList = glob.glob('dijet_nano/{}*_{}_snapshot.txt'.format(setName,year))
        for snapFile in fileList:
       	    # need to get names of ROOT files from txt
	    fList = open(snapFile)
	    rFiles = [i.strip() for i in fList if i != '']
	    for fName in rFiles:
	        #print('opening {}'.format(fName))
	        f = ROOT.TFile.Open(fName, 'READ')
	        # check for empty TTrees
	        if not f.Get('Events'):
		    #print('Skipping file due to no Events TTree:\n\t{}'.format(fName))
		    continue
	        e = f.Get('Events')
	        if not e.GetEntry():
		    #print('Skipping file due to empty Events TTree:\n\t{}'.format(fName))
		    continue
		e.GetEntry()	# initialize all branches
	        for cut, num in varDict.items():
		    if ('SR' in cut) or ('CR' in cut):
		        pass		    
		    else:
			#print('Getting Leaf {}'.format(cut))
			if e.GetLeaf(cut):
	                    varDict[cut] += e.GetLeaf(cut).GetValue(0)
	        f.Close()

    if selection:
        # selection will have common sets joined by default (see rootfiles/get_all.py and perform_selection.py)
        # i.e.: 	THselection_ZJets_18.root
        for year, varDict in years.items():
#          if (year==16):
            if not os.path.exists('/uscms/home/dpilipov/nobackup/TwoDAlphabet/CMSSW_10_6_14/src/rootfiles/THselection_mvaID_HT{}_{}_{}.root'.format(HT, setName, year)):
#	    if not os.path.exists('rootfiles/THselection_mvaID_lead_HT{}_{}_{}.root'.format(HT, setName, year)):
	        pass
            f = ROOT.TFile.Open('/uscms/home/dpilipov/nobackup/TwoDAlphabet/CMSSW_10_6_14/src/rootfiles/THselection_mvaID_HT{}_{}_{}.root'.format(HT, setName, year))
#	    f = ROOT.TFile.Open('rootfiles/THselection_mvaID_lead_HT{}_{}_{}.root'.format(HT, setName, year))
            print(f)
	    h = f.Get('cutflow')
#	    for i in range(1, 9):	# cutflow has 8 bins w the cuts, starting from index 1
            for i in range(1, 9):       # cutflow has 8 bins w the cuts, starting from index 1
	        var = h.GetXaxis().GetBinLabel(i)
	        val = h.GetBinContent(i)
	        varDict[var] += val
                print(var,val)
	    f.Close()

    # returns dict of {year: cutflowDict}
    return years


def printYields(selection=True):
    '''prints the yields for bkg and data in Latex form'''
#DP EDIT
    print('in printYields')
#    labels = ["Sample","nProc","nFlags","nJets","nJetID","p_{t}","nKin","$|\Delta\eta|$"]
#snapVars = OrderedDict([('NPROC',0.),('NFLAGS',0.),('NJETS',0.),('NPHOTONS',0.),('NJETID',0),('NPT',0.),('NKIN',0.),('NPHOTONKIN',0.),('NDELTAETA',0.),('NPHOTONNOTELEC',0.),('NPHOTONINBARR',0.),('PreLepVeto',0.),('PostLepVeto',0.)])
    selection = True
    labels = ["Sample","nProc","nFlags","nJets","nPhotons","nJetID","p_{t}","nKin","nAKin","nAnotE","nAinB","PreLepVeto","PostLepVeto"]
    if selection:
	labels.extend(["Tot_CR","FF_CR","F_CR","P_CR","Tot_SR","FF_SR","F_SR","P_SR"])
#       labels.extend(["FF_CR","F_CR","P_CR","FF_SR","F_SR","P_SR"])
    sets = ["ttbar", "VJets", "Data"]
#    sets = ["ttbar", "WJets", "ZJets", "Data"]
#    sets = ["Data"]

    for s in sets:
        print(s)
        res = generateCutflow(s, 900, selection)
        print('\n------------------ {} -------------------'.format(s))
        for year, dicts in res.items():
	    print('----------------- {} -----------------'.format('20'+year))
	    latexRow = s + " &"
	    for var, val in dicts.items():
	        if (val > 10000):
		    latexRow += " {0:1.2e} &".format(val)
	        else:
		    latexRow += " {0:.3f} &".format(val)
            print(" & ".join(labels)+" \\\\")
            print(latexRow)

	#print(res)
        # just a short routine to check the impact of tight jetId cuts
	for year in ['16','16APV','17','18']:
#        for year in ['16']:
            nJetID = float(res[year]['NJETID'])
            nJets = float(res[year]['NJETS'])
            if nJets>0:
               print('20{} Percent loss from nJets -> nJetId cut: {}%'.format(year, (1.0 - nJetID/nJets)*100.))    

def printEfficiencies(selection=True):
    '''prints the efficiencies for various T' samples.
	First, for mT = 1800, mPhi = 75, 100, 125, 250, 500
	Then, for mPhi = 125, mT = 1400, 1500, 1600, 1700, 1800  (SKIP 1700 - it's missing 2018)
    '''
    print('in printEff')
#DP EDIT
#    labels = ["Sample","nProc","nFlags","nJets","nJetID","p_{t}","nKin","$|\Delta\eta|$","preLeptonVeto","postLeptonVeto"]
    selection = True
    labels = ["Sample","nProc","nFlags","nJets","nPhotons","nJetID","p_{t}","nKin","nAKin","nAnotE","nAinB","preLeptonVeto","postLeptonVeto"]

    if selection:
#       labels.extend(["Tot_SR","FF_SR","F_SR","P_SR"])
	labels.extend(["Tot_CR","FF_CR","F_CR","P_CR","Tot_SR","FF_SR","F_SR","P_SR"])
#       labels.extend(["FF_CR","F_CR","P_CR","FF_SR","F_SR","P_SR"])
    # first keep constant mT
# DP EDIT
    prefix = 'StoAA'
    mT = 1000
#    phiMasses = [50, 100, 150, 200, 250, 300, 350]
    phiMasses = [100, 200, 300]
    for mPhi in phiMasses:
	nProc = 0
#DP EDIT ... just for now!!! eventually will have more samples...
	res = generateCutflow('{}{}x{}'.format(prefix, mT, mPhi), 900, selection)
#	res = generateCutflow('{}{}'.format(prefix,mPhi), 0, selection)
	print('\n------------------ {} -------------------'.format('{}{}x{}'.format(prefix, mT, mPhi)))
#	print('\n------------------ {} -------------------'.format('{}{}'.format(prefix,mPhi)))
	for year, dicts in res.items():
	    print('----------------- {} -----------------'.format('20'+year))
	    latexRow = '{}{}x{}'.format(prefix, mT, mPhi) + " &"
#	    latexRow = '{}{}'.format(prefix,mPhi) + " &"
	    for var, val in dicts.items():
		if (var == 'NPROC'):
		    nProc = val
		    latexRow += " 1 &"
		else:
                    if (float(nProc) > 0.0):
		        latexRow += " {0:.3f} &".format(float(val)/float(nProc))
	    print(" & ".join(labels)+" \\\\")
	    print(latexRow)

    # now keep constant mPhi
# DP EDIT
#    mPhi = 125
    mPhi = 100
    Tmasses = [800,1000,1300,1500]
#    Tmasses = [800, 900, 1000, 1200, 1300, 1500]
#    Tmasses = [1000]
    for Tmass in Tmasses:
#      for mPhi in phiMasses:
	nProc = 0
#DP EDIT
	res = generateCutflow('{}{}x{}'.format(prefix, Tmass, mPhi), 900, selection)
	print('\n------------------ {} -------------------'.format('{}{}x{}'.format(prefix, Tmass, mPhi)))
#	res = generateCutflow('{}{}'.format(prefix,mPhi), 0, selection)
#	print('\n------------------ {} -------------------'.format('{}{}'.format(prefix,mPhi)))
	for year, dicts in res.items():
	    print('----------------- {} -----------------'.format('20'+year))
#DP EDIT
	    latexRow = '{}{}x{}'.format(prefix, Tmass, mPhi) + " &"
#	    latexRow = '{}{}'.format(prefix,mPhi) + " &"
	    for var, val in dicts.items():
                if (var == 'NPROC'):
                    nProc = val
                    latexRow += " 1 &"
                else:
                    if (float(nProc) > 0.0):
                        latexRow += " {0:.3f} &".format(float(val)/float(nProc))
            print(" & ".join(labels)+" \\\\")
            print(latexRow)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--selection', action='store_true',
			help='Get cutflow/yield info for selection too. Do not include if you only want snapshot info.')
    parser.add_argument('--HT', type=str, dest='HT',
                        action='store', default='900',
                        help='Value of HT to cut on')    
    args = parser.parse_args()

#DP EDIT ... do not use for now....
    print('at printYields')
    printYields(args.selection)
    print('at printEff')
    printEfficiencies(args.selection)
