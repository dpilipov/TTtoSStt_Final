import ROOT, time
from collections import OrderedDict
from TIMBER.Analyzer import HistGroup, Correction
from TIMBER.Tools.Common import CompileCpp
ROOT.gROOT.SetBatch(True)

#DP EDIT
from TTClass import TTClass

def getSaaEfficiencies(analyzer, tagger, SRorCR, PASSorFAIL, wp):
    ''' 
	call this function after ApplyTopPick() has been called
	Therefore, we have to prepend the tagger with 'Higgs_'
    '''
    print('Obtaining efficiencies in {}'.format(SRorCR))
#DP EDIT
    tagger = 'Diphoton_' + tagger
    start = analyzer.GetActiveNode()
    nTot = analyzer.DataFrame.Sum("genWeight").GetValue()
    print("nTot = {}".format(nTot))
    if (PASSorFAIL == "PASS"):
       analyzer.Cut("Eff_{}_cut".format(SRorCR),"({0}[0] > {1} && {0}[1] > {1})".format(tagger, wp))
    else:
       analyzer.Cut("Eff_{}_cut".format(SRorCR),"({0}[0] > {1} && {0}[1] < {1}) || ({0}[1] > {1} && {0}[0] < {1})".format(tagger, wp))
    nT = analyzer.DataFrame.Sum("genWeight").GetValue()
    print("nT = {}".format(nT))
    effT = nT/nTot
    analyzer.SetActiveNode(start)
    print('{}: effT = {}%'.format(SRorCR, effT*100.))
    return effT

def getTopEfficiencies(analyzer, tagger, wp, idx, tag):
    print('Obtaining efficiencies for jet at idx {}'.format(idx))
    start = analyzer.GetActiveNode()
    nTot = analyzer.DataFrame.Sum("genWeight").GetValue()
    print("nTot = {}".format(nTot))
    analyzer.Cut("Eff_jet{}_{}_cut".format(idx, tag),"{} > {}".format(tagger, wp))
    nT = analyzer.DataFrame.Sum("genWeight").GetValue()
    print('nT = {}'.format(nT))
    eff = nT/nTot
    print('SR: eff = {}'.format(eff*100.))
    analyzer.SetActiveNode(start)
    return eff

def applyScaleFactors(analyzer, tagger, variation, SRorCR, PASSorFAIL, eff, wp):
    '''
	creates PNetSFHandler object and creates the original and updated tagger categories
	must be called ONLY once, after calling ApplyTopPick() so proper Higgs vect is created
	Therefore, we have to prepend the tagger with 'Higgs_'
    '''
    print('Applying SFs in {0}_{1}'.format(SRorCR, PASSorFAIL))
#DP EDIT
#    tagger = 'Higgs_' + tagger
    # instantiate Scale Factor class: {WPs}, {effs}, "year", variation
#    CompileCpp('PNetXbbSFHandler p_%s = PNetXbbSFHandler({0.8,0.98}, {%f,%f}, "20%s", %i);'%(SRorCR, eff_loose, eff_tight, args.era, variation))
    tagger = 'Diphoton_' + tagger
    CompileCpp('PNetSaaSFHandler p_%s_%s = PNetSaaSFHandler(-0.9, %f, "20%s", %i);'%(SRorCR, PASSorFAIL, eff, args.era, variation))
    # now create the column with original tagger category values (1: fail, 2: pass)
    analyzer.Define("OriginalTagCats","p_{}_{}.createTag({})".format(SRorCR, PASSorFAIL, tagger))
    # now create the column with *new* tagger categories, after applying logic. MUST feed in the original column (created in last step)
#    analyzer.Define("NewTagCats","p_{}.updateTag(OriginalTagCats, Higgs_pt_corr, {})".format(SRorCR, tagger))
    analyzer.Define("NewTagCats","p_{}_{}.updateTag(OriginalTagCats, Diphoton_pt, {})".format(SRorCR, PASSorFAIL, tagger))

def TTselection(args):
    ROOT.ROOT.EnableImplicitMT(args.threads)
    start = time.time()
    signal = False

    print('Opening dijet_nano/{}_{}_snapshot.txt'.format(args.setname,args.era))
#DP EDIT
#    selection = THClass('dijet_nano/{}_{}_snapshot.txt'.format(args.setname,args.era),args.era,1,1)
    selection = TTClass('dijet_nano/{}_{}_snapshot.txt'.format(args.setname,args.era),args.era,1,1)
    selection.OpenForSelection(args.variation)

    # apply HT cut due to improved trigger effs
    before = selection.a.DataFrame.Count()
    selection.a.Cut('HT_cut','HT > {}'.format(args.HT))
    after = selection.a.DataFrame.Count()

    selection.ApplyTrigs(args.trigEff)

    # scale factor application
    if ('StoAA' in args.setname):
	signal = True
	# Determine which SF we are varying 
	if (args.variation == 'PNetTop_up'):
	    TopVar = 1
	    SaaVar = 0
	elif (args.variation == 'PNetTop_down'):
	    TopVar = 2
	    SaaVar = 0
	elif (args.variation == 'PNetSaa_up'):
	    TopVar = 0
	    SaaVar = 1
	elif (args.variation == 'PNetSaa_down'):
	    TopVar = 0
	    SaaVar = 2
	else:	# if doing any other variation, keep Top/Xbb SFs nominal
	    TopVar = 0
	    SaaVar = 0

    kinOnly = selection.a.MakeWeightCols(extraNominal='' if selection.a.isData else 'genWeight*%s'%selection.GetXsecScale())
    out = ROOT.TFile.Open('rootfiles/THselection_HT%s_%s%s_%s%s.root'%(args.HT, args.setname,
                                                                  '' if args.topcut == '' else '_htag'+args.topcut.replace('.','p'),
                                                                  args.era,
                                                                  '' if args.variation == 'None' else '_'+args.variation), 'RECREATE')
    out.cd()

    for t in ['particleNet']:	# add other taggers to this list if studying more than just ParticleNet
#DP EDIT: commented out these two lines
#        if args.topcut != '':
#            selection.cuts[t+'MD_HbbvsQCD'] = float(args.topcut)

            top_tagger = '%s_TvsQCD'%t
            photon_tagger = 'mvaID'

	# SIGNAL
# WE DO NOT NEED THIS....	if signal:
#            print('DOING THE SIGNAL TEST - PRE SF')
#            selection.a.SetActiveNode(kinOnly)
#            passTest = selection.ApplySTagTopTagCheck(photon_tagger, -0.9, top_tagger, 0.8)
#            PreSmassTPmassTest = selection.ApplyPreSmassTPmassCheck(0.0,0.0)
	    print('----------------------- CONTROL REGION --------------------------------------------------------------')
	    # CONTROL REGION - ONE TOP REAL ONE NOT
	    selection.a.SetActiveNode(kinOnly)
#            e0CR = getTopEfficiencies(analyzer=selection.a, tagger='Dijet_'+top_tagger+'[0]', wp=0.8, idx=0, tag='cr1')
#            e1CR = getTopEfficiencies(analyzer=selection.a, tagger='Dijet_'+top_tagger+'[1]', wp=0.8, idx=1, tag='cr2')
            #NEXT DEFINE THE TOPS AND THE PHOTONS
#            selection.ApplyTopPick_Signal(TopTagger='Dijet_'+top_tagger, PhotonTagger='Diphoton_'+photon_tagger, pt='Dijet_pt_corr', TopScoreCut=0.8, PhotonScoreCut=-0.9, eff0=e0CR, eff1=e1CR, year=args.era, TopVariation=TopVar)
#            print('DOING THE MASS TEST')
#            SmassTPmassTest = selection.ApplySmassTPmassCheck(0.0,0.0)
            # CONTROL REGION - ONE TOP REAL ONE NOT; PASS - BOTH REAL PHOTONS
#            eff_CR_PASS = getSaaEfficiencies(selection.a, photon_tagger, 'CR', 'PASS', -0.9)
#            applyScaleFactors(selection.a, photon_tagger, SaaVar, 'CR', 'PASS', eff_CR_PASS, -0.9)
            # CONTROL REGION - ONE TOP REAL ONE NOT; FAIL - ONLY ONE REAL PHOTON
#            eff_CR_FAIL = getSaaEfficiencies(selection.a, photon_tagger, 'CR', 'FAIL', -0.9)
#            applyScaleFactors(selection.a, photon_tagger, SaaVar, 'CR', 'FAIL', eff_CR_FAIL, -0.9)
            passfailCR = selection.ApplySTagTopTag('CR', top_tagger, 0.8, photon_tagger, -0.9)
	    # SIGNAL REGION
            print('----------------------- SIGNAL REGION --------------------------------------------------------------')
            selection.a.SetActiveNode(kinOnly)
#DP EDIT
#            e0SR = getTopEfficiencies(analyzer=selection.a, tagger='Dijet_'+top_tagger+'[0]', wp=0.8, idx=0, tag='sr1')
#            e1SR = getTopEfficiencies(analyzer=selection.a, tagger='Dijet_'+top_tagger+'[1]', wp=0.8, idx=1, tag='sr2')
#            selection.ApplyTopPick_Signal(TopTagger='Dijet_'+top_tagger, XbbTagger='Dijet_'+higgs_tagger, pt='Dijet_pt_corr', TopScoreCut=0.94, eff0=e0SR, eff1=e1SR, year=args.era, TopVariation=TopVar, invert=False)
#            eff_L_SR, eff_T_SR = getXbbEfficiencies(selection.a, higgs_tagger, 'SR', 0.8, 0.98)
#            applyScaleFactors(selection.a, higgs_tagger, XbbVar, 'SR', eff_L_SR, eff_T_SR, 0.8, 0.95)
#            passfailSR = selection.ApplyHiggsTag('SR', tagger=higgs_tagger, signal=signal)
#            e0SR = getTopEfficiencies(analyzer=selection.a, tagger='Dijet_'+top_tagger+'[0]', wp=0.8, idx=0, tag='sr1')
#            e1SR = getTopEfficiencies(analyzer=selection.a, tagger='Dijet_'+top_tagger+'[1]', wp=0.8, idx=1, tag='sr2')
#            selection.ApplyTopPick_Signal(TopTagger='Dijet_'+top_tagger, PhotonTagger='Diphoton_'+photon_tagger, pt='Dijet_pt_corr', TopScoreCut=0.8, PhotonScoreCut=-0.9, eff0=e0SR, eff1=e1SR, year=args.era, TopVariation=TopVar)
#            eff_SR_PASS = getSaaEfficiencies(selection.a, photon_tagger, 'SR', 'PASS', -0.9)
#            applyScaleFactors(selection.a, photon_tagger, SaaVar, 'SR', 'PASS', eff_SR_PASS, -0.9)
#            eff_SR_FAIL = getSaaEfficiencies(selection.a, photon_tagger, 'SR', 'FAIL', -0.9)
#            applyScaleFactors(selection.a, photon_tagger, SaaVar, 'SR', 'FAIL', eff_SR_FAIL, -0.9)
            passfailSR = selection.ApplySTagTopTag('SR', top_tagger, 0.8, photon_tagger, -0.9)

	# rkey: SR/CR, pfkey: pass/loose/fail
 #           print('DOING THE MASS TEST')
#            SmassTPmassTest = selection.ApplySmassTPmassCheck(0.0,0.0)

            print('ABOUT TO PLOT....')
            for rkey,rpair in {"SR":passfailSR,"CR":passfailCR}.items():
              for pfkey,n in rpair.items():
                mod_name = "%s_%s_%s"%('TvsQCD_mvaID',rkey,pfkey)
                print(mod_name)
                mod_title = "%s %s"%(rkey,pfkey)
                print(mod_title)
                selection.a.SetActiveNode(n)
#                SmassHist = ROOT.TH1F('Smass','Smass',40,60,1260)
		# MakeTemplateHistos takes in the template histogram and then the variables which to plot in the form [x, y]
		# in this case, 'Smass' is the x axis (S mass) and 'mth' is the y axis (T' mass = St mass)
		# both of these variables were created/defined during the ApplyTopPick() and ApplyHiggsTag() steps above (see THClass)
                templates = selection.a.MakeTemplateHistos(ROOT.TH2F('MtpvMs_%s'%mod_name,'MtpvMs %s with %s'%(mod_title,'TvsQCD_mvaID'),20,0,800,20,600,2200),['Smass','mth'])
#                templates = selection.a.MakeTemplateHistos(ROOT.TH1F('MthvMs_%s'%mod_name,'MthvMs %s with %s'%(mod_title,t),40,60,1260),['Smass'])
#                templates = selection.a.MakeTemplateHistos(SmassHist,['Smass'])
                templates.Do('Write')
    '''
    # now process cutflow information
    cutflowInfo = OrderedDict([
	('nTop_CR',selection.nTop_CR), 
	('higgsF_CR',selection.higgsF_CR),
	('higgsL_CR',selection.higgsL_CR),
	('higgsP_CR',selection.higgsP_CR),
	('nTop_SR',selection.nTop_SR),
	('higgsF_SR',selection.higgsF_SR),
	('higgsL_SR',selection.higgsL_SR),
	('higgsP_SR',selection.higgsP_SR),
    ])

    nLabels = len(cutflowInfo)
    hCutflow = ROOT.TH1F('cutflow'.format(args.setname, args.era, args.variation), "Number of events after each cut", nLabels, 0.5, nLabels+0.5)
    nBin = 1
    for label, value in cutflowInfo.items():
	hCutflow.GetXaxis().SetBinLabel(nBin, label)
	hCutflow.AddBinContent(nBin, value)
	nBin += 1
    hCutflow.Write()
    '''

    if not selection.a.isData:
        scale = ROOT.TH1F('scale','xsec*lumi/genEventSumw',1,0,1)
        scale.SetBinContent(1,selection.GetXsecScale())
        scale.Write()
#        selection.a.PrintNodeTree('NodeTree_selection.pdf',verbose=True)

    before = before.GetValue()
    after = after.GetValue()
    frac = float(after)/float(before)
    loss = 100.*(1-frac)
    print('------------------------------------------------------------')
    print('Fractional loss of {}% of events after HT cut'.format(loss))
    print('------------------------------------------------------------')
    print ('%s sec'%(time.time()-start))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-s', type=str, dest='setname',
                        action='store', required=True,
                        help='Setname to process.')
    parser.add_argument('-y', type=str, dest='era',
                        action='store', required=True,
                        help='Year of set (16, 16APV, 17, 18).')
    parser.add_argument('-v', type=str, dest='variation',
                        action='store', default='None',
                        help='JES_up, JES_down, JMR_up,...')
    parser.add_argument('--HT', type=str, dest='HT',
                        action='store', default='0',
                        help='Value of HT to cut on')
    parser.add_argument('--topcut', type=str, dest='topcut',
                        action='store', default='',
                        help='Overrides config entry if non-empty')
    args = parser.parse_args()
    args.threads = 2

    # Updated method using the trigger efficiencies parameterized by 2D function
    if ('Data' not in args.setname) and (args.era == '17'): # we are dealing with MC from 2017
        cutoff = 0.11655        # fraction of total JetHT data belonging to 2017B
        TRand = ROOT.TRandom()
        rand = TRand.Uniform(0.0, 1.0)
        if rand < cutoff:       # apply the 2017B trigger efficiency to this MC
            print('Applying 2017B trigger efficiency')
            args.trigEff = Correction("TriggerEff17",'TIMBER/Framework/include/EffLoader_2DfittedHist.h',['out_Eff_2017B.root','Eff_2017B'],corrtype='weight')
        else:
            args.trigEff = Correction("TriggerEff17",'TIMBER/Framework/include/EffLoader_2DfittedHist.h',['out_Eff_2017.root','Eff_2017'],corrtype='weight')
    elif ('16' in args.era):
        args.trigEff = Correction("TriggerEff"+args.era,'TIMBER/Framework/include/EffLoader.h',['THtrigger2D_HT{}_{}.root'.format(args.HT,args.era if 'APV' not in args.era else 16),'Pretag'], corrtype='weight')
    else:
        args.trigEff = Correction("TriggerEff18",'TIMBER/Framework/include/EffLoader_2DfittedHist.h',['out_Eff_2018.root','Eff_2018'],corrtype='weight')

#DP EDIT
#    CompileCpp('THmodules.cc')
    CompileCpp('TTmodules.cc')
    if ('StoAA' in args.setname):
	#CompileCpp('ParticleNet_TopSF.cc')
#DP EDIT
#	CompileCpp('ParticleNet_XbbSF.cc')
        CompileCpp('ParticleNet_SaaSF.cc')
    TTselection(args)
