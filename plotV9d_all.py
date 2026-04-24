import ROOT
from TIMBER.Analyzer import analyzer, HistGroup
from TIMBER.Tools.Plot import *
from collections import OrderedDict

ROOT.gROOT.SetBatch(True)

####################################
# Store some global variables here #
####################################
# Dictionary of samples we will plot, along with their LaTeX titles
samples = {	
        "StoAA100"  : "signal 1000/100",
        "StoAA150"  : "signal 1000/150",
        "StoAA"  : "signal 1000/200",
#	"StoAA_1000_200"  : "signal 1000/200",
#	"StoAA_1000_200X" : "signal 1000/200X",
	"ttbar" 	: "t#bar{t}",
    	"QCDHT700"	: "QCD",
    	"QCDHT1000"	: "QCD",
    	"QCDHT1500"	: "QCD",
    	"QCDHT2000"	: "QCD",
    	"QCD"		: "QCD"		# used to concatenate both singletop processes
}

# Add any signals you've processed here
#signals = ['signalLH{}'.format(mass) for mass in [2000]]#range(1400,4200,600)]
signals = ['StoAA','StoAA150','StoAA100']
#for sig in signals:
#    samples.update({sig : 'b*_{LH} %s (GeV)'%(sig[-4:])})
#for sig in signals:
#    samples.update({sig : ''})
samples.update({'StoAA100' : '1000/100'})
samples.update({'StoAA150' : '1000/150'})
samples.update({'StoAA' : '1000/200'})

# Store colors for each sample
colors = {}
for p in samples.keys():
#    if 'signal' in p:
#	 colors[p] = ROOT.kCyan-int((int(p[-4:])-1400)/600)
    if 'StoAA100' in p:
        colors[p] = ROOT.kGreen
    elif 'StoAA150' in p:
        colors[p] = ROOT.kCyan
    elif 'StoAA' in p:
        colors[p] = ROOT.kViolet
    elif 'ttbar' in p:
	colors[p] = ROOT.kRed
#    elif p == 'singletop':
#	colors[p] = ROOT.kBlue
    elif p == 'QCD':
	colors[p] = ROOT.kYellow

# Store the variables you want to plot, along with their LaTeX titles
varnames = {
	# SELECTION ARGS -----------------------------------
#        'lead_tau32'             : '#tau_{32}^{jet0}',
#        'sublead_tau32'          : '#tau_{32}^{jet1}',
#        'lead_tau21'             : '#tau_{21}^{jet0}',
#        'sublead_tau21'          : '#tau_{21}^{jet1}',
#        'nbjet_loose'            : 'loosebjets',
#        'nbjet_medium'           : 'mediumbjets',
#        'nbjet_tight'            : 'tightbjets',
        'pt'             : 'p_{T}^{jet0}',
        'Apt'                      : 'p_{T}^{#gamma 0}',
#        'sublead_jetPt'          : 'p_{T}^{jet1}',
#        'deltaphi'               : '#Delta#phi_{jet0,jet1}',
#        'deltaEta'               : '#Delta#eta_{jet0,jet1}',
#        'AdeltaEta'                : '#Delta#eta_{#gamma 0,#gamma 1}',
        'mtop'     : 'm_{SD}^{jet0}',
#        'Smass'                   : 'M_{#gamma #gamma}',
        'deltaR'                  : '{#Delta}R_{#gamma,#gamma}',
        'dPhi'                  : '{#Delta}#phi_{jj}',
        'AdPhi'                  : '{#Delta}#phi_{#gamma,#gamma}',
#        'sublead_softdrop_mass'  : 'm_{SD}^{jet1}',
        'topTag'                  : 'AK8 ParticleNet TvsQCD^{jet0}',
#        'photonMvaID'             : 'Photon mva ID',
        'photonTag'               : 'Photon cutBased^{#gamma 0}',
#        'tmass'                   : 'M_{jj}',
#        'sublead_deepAK8_TvsQCD' : 'Deep AK8 TvsQCD^{jet1}',
#        'lead_deepAK8_WvsQCD'    : 'Deep AK8 WvsQCD^{jet0}',
#        'sublead_deepAK8_WvsQCD' : 'Deep AK8 WvsQCD^{jet1}',
	# N minus 1 ARGS -----------------------------------
#    	'deltaY' : '|#Delta y|',
#    	'tau21'  : '#tau_{2} / #tau_{1}',
#    	'tau32'  : '#tau_{3} / #tau_{2}',
#    	'mW'     : 'm_{W} [GeV]',
#        'Smass'  : 'M_{#gamma #gamma} [GeV]',
    	'mtop'   : 'm_{SD}^{jet0} [GeV]',
        'pt'     : 'p_{T}^{jet0}',
#        'deltaEta': '#Delta#eta_{jet0,jet1}',
        'deltaR'  : '{#Delta}R_{#gamma 0,#gamma 1}',
        'dPhi'                  : '{#Delta}#phi_{jj}',
        'AdPhi'                  : '{#Delta}#phi_{#gamma,#gamma}',
        'topTag' : 'AK8 ParticleNet TvsQCD^{jet0}',
#        'photonMvaID'             : 'Photon mva ID'
        'photonTag' : 'Photon cutBased^{#gamma 0}',
#        'tmass'                   : 'M_{jj} [GeV]'
}

########################################################################

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-y', type=str, dest='year',
                        action='store', required=True,
                        help='Year of set (16, 17, 18).')
    parser.add_argument('--nminus1',
			action='store_true',
			help='If flag passed, plot N-1 distributions instead of selection')
    parser.add_argument('--logy',
                        action='store_true',
                        help='If flag passed, plot logarithmic distributions')
    parser.add_argument('--soverb',
                        action='store_true',
                        help='If flag passed, add a sub pad with signal/sqrt(background) calculation')
    args = parser.parse_args()

    # Store all of the histograms we want to track
    histgroups = {}

    # Open the rootfiles we created previously
    # Syntax is either <setname>_<year>.root for selection distributions
    # or <setname>_<year>_Nminus1.root for N-1 distributions
    for sample in samples.keys():
#	if (sample=='QCD') or (sample=='StoAA'): 
#DP EDIT FOR NOW ONLY ONE SAMPLE!!!  NO NEED TO CONCATENATE
        if (sample=='QCD'):
	    # These are just stored to concatenate the QCD/singletop backgrounds, ignore
	    continue
#	 inFile = ROOT.TFile.Open('rootfiles/Nminus1_jets_{}_{}{}.root'.format(sample, args.year, '_Nminus1_jets' if args.nminus1 else '_selection'))
#DP EDIT !!!! MUST ADD CASE OF selection LATER!!!!
#        inFile = ROOT.TFile.Open('rootfiles/NMinus1_jets_{}_{}{}.root'.format(sample, args.year))
        inFile = ROOT.TFile.Open('rootfiles/NMinus1_v9d_{}_{}_1of1.root'.format(sample, args.year))
	if inFile == None:
#	    print('WARNING: rootfiles/NMinus1_jets_{}_{}{}.root does not exist, please create first\n'.format(sample, args.year, '_Nminus1_jets' if args.nminus1 else ''))
           print('WARNING: rootfiles/NMinus1_v9d_{}_{}_1of1.root does not exist, please create first\n'.format(sample, args.year))
	   continue	

	# Put histograms into the HistGroups
	histgroups[sample] = HistGroup(sample)
	for key in inFile.GetListOfKeys():	# loop over histograms in the file
	    keyname = key.GetName()
	    # Selection and N-1 file histograms are named slightly differently
	    if args.nminus1:
		varname = keyname
	    else:
		if sample not in keyname: continue  # should never happen, but just in case
		varname = keyname[len(sample+'_'+args.year)+1:] # get the variable name, e.g. lead_tau32
	    inhist = inFile.Get(key.GetName()) # get it from the file
	    inhist.SetDirectory(0) # set the directory so hist is stored in memory and not as reference to TFile (this way it doesn't get tossed by python garbage collection when infile changes)
	    histgroups[sample].Add(varname,inhist) # add to our group
	    print('Added {} distribution for sample {}'.format(varname, sample))

	# Close the input ROOT file
	inFile.Close()

    ''' # You can treat the histgroup just like a nested dictionary, i.e. 
    for i in histgroups.keys():		# this will print the sample name (e.g. 'ttbar', 'QCDHT700', etc)
	print(i)
	for j in histgroups[i].keys():	# this will print the variable name (e.g. lead_tau32)
	    print(j)
    '''

    # Get the variable names list. The following format ensures that, as long as one file has been processed, 
    # the proper variable names will be found without the user having to specify anything additional.
    ExistingVarnames = histgroups[list(histgroups.keys())[0]].keys()

    # Now plot the variables up in the global definitions above
    for varname in ExistingVarnames:
	plot_filename = 'plots/{}_{}{}{}{}.png'.format(varname, args.year, '_Nminus1_v9d' if args.nminus1 else '','_SoverB' if args.soverb else '', '_logy' if args.logy else '')
	# Setup ordered dictionaries so processes plot in the order we specify
	bkg_hists, signal_hists = OrderedDict(), OrderedDict()
	# First do bkgs, plotting largest first
# DP EDIT  INCLUDE ttbar ONCE IT IS DONE!!!!!
#        for bkg in ['QCDHT700','QCDHT1000','QCDHT1500','QCDHT2000','ttbar','singletop_tW','singletop_tWB']:
        tot_bkg_int = 0
	for bkg in ['QCDHT700','QCDHT1000','QCDHT1500','QCDHT2000','ttbar']:
	    if bkg not in histgroups.keys(): continue	# ensures user doesn't have to modify above list
	    histgroups[bkg][varname].SetTitle('{} 20{}'.format(varname, args.year))
	    if 'QCD' in bkg:
		if 'QCD' not in bkg_hists.keys():
		    bkg_hists['QCD'] = histgroups[bkg][varname].Clone('QCD_'+varname)
		else:
		    bkg_hists['QCD'].Add(histgroups[bkg][varname])
	    elif 'StoAA' in bkg:
		if 'StoAA' not in bkg_hists.keys():
		    bkg_hists['StoAA'] = histgroups[bkg][varname].Clone('StoAA_'+varname)
		else:
		    bkg_hists['StoAA'].Add(histgroups[bkg][varname])
	    else:
		# Only bkg left is ttbar, which doesn't get concatenated
		bkg_hists[bkg] = histgroups[bkg][varname]
                print('doing ttbar background')
#            tot_bkg_int += bkg_hists[bkg].Integral()
        print(varname)
#        print(tot_bkg_int)
	# Now, add the signals
	for sig in samples.keys():
#	     if 'signal' not in sig: continue
            if 'StoAA' not in sig: continue
	    signal_hists[sig] = histgroups[sig][varname]

	# Plot everything together!
	CompareShapes(
	    outfilename = plot_filename,
	    year = args.year,
	    prettyvarname = varnames[varname],
	    bkgs = bkg_hists,
	    signals = signal_hists,
	    colors = colors,
	    names = samples,
	    logy = args.logy,
	    doSoverB = args.soverb,
	    stackBkg = True
	)
