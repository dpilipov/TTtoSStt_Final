import ROOT, time
from collections import OrderedDict
from TIMBER.Analyzer import HistGroup, Correction
from TIMBER.Tools.Common import CompileCpp
ROOT.gROOT.SetBatch(True)

#DP EDIT
from TTClassSubleadVR18 import TTClassSubleadVR18

def getSaaEfficiencies(analyzer, SRorCR, Toptagger, ToptaggerWP, Stagger, StaggerWP):
    ''' 
	call this function after ApplyTopPick() has been called
	Therefore, we have to prepend the tagger with 'Higgs_'
    '''
    print('Obtaining efficiencies in {}'.format(SRorCR))
#DP EDIT
    start = analyzer.GetActiveNode()
    nTot = analyzer.DataFrame.Sum("genWeight").GetValue()
    print("nTot = {}".format(nTot))
    if (SRorCR == 'SR'):
       analyzer.Cut("Eff_{}_cut".format(SRorCR),"(Dijet_{0}[0] > {1}) && (Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP))
       nTSR = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTSR = {}".format(nTSR))
       analyzer.Cut("Eff_{}_PASS_cut".format(SRorCR),"(Diphoton_{2}[0] >= {3}) && (Diphoton_{2}[1] >= {3}) && (Dijet_{0}[0] > {1}) && (Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTPASS = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTPASS= {}".format(nTPASS))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAIL_cut".format(SRorCR),"((Diphoton_{2}[0] >= {3} && Diphoton_{2}[1] < {3}) || (Diphoton_{2}[1] >= {3} && Diphoton_{2}[0] < {3})) && (Dijet_{0}[0] > {1} && Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAIL= {}".format(nTFAIL))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAILFAIL_cut".format(SRorCR),"(Diphoton_{2}[0] < {3} && Diphoton_{2}[1] < {3}) && (Dijet_{0}[0] > {1} && Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAILFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAILFAIL= {}".format(nTFAILFAIL))
    else:
       analyzer.Cut("Eff_{}_cut".format(SRorCR),"((Dijet_{0}[0] > {1}) && (Dijet_{0}[1] < {1})) || ((Dijet_{0}[1] > {1}) && (Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP))
       nTSR = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTCR = {}".format(nTSR))
       analyzer.Cut("Eff_{}_PASS_cut".format(SRorCR),"(Diphoton_{2}[0] >= {3} && Diphoton_{2}[1] >= {3}) && ((Dijet_{0}[0] > {1} && Dijet_{0}[1] < {1}) || (Dijet_{0}[1] > {1} && Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTPASS = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTPASS= {}".format(nTPASS))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAIL_cut".format(SRorCR),"((Diphoton_{2}[0] >= {3} && Diphoton_{2}[1] < {3}) || (Diphoton_{2}[1] >= {3} && Diphoton_{2}[0] < {3})) && ((Dijet_{0}[0] > {1} && Dijet_{0}[1] < {1}) || (Dijet_{0}[1] > {1} && Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAIL= {}".format(nTFAIL))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAILFAIL_cut".format(SRorCR),"(Diphoton_{2}[0] < {3} && Diphoton_{2}[1] < {3}) && ((Dijet_{0}[0] > {1} && Dijet_{0}[1] < {1}) || (Dijet_{0}[1] > {1} && Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAILFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAILFAIL= {}".format(nTFAILFAIL))
    effPASS = nTPASS/nTot
    effFAIL = nTFAIL/nTot
    effFAILFAIL = nTFAILFAIL/nTot
    analyzer.SetActiveNode(start)
    print('{}: effPASS = {}%'.format(SRorCR, effPASS*100.))
    print('{}: effFAIL = {}%'.format(SRorCR, effFAIL*100.))
    print('{}: effFAILFAIL = {}%'.format(SRorCR, effFAILFAIL*100.))
    return effPASS, effFAIL, effFAILFAIL

def getSaaEfficienciesTag(analyzer, SRorCR, Toptagger, ToptaggerWP, Stagger, StaggerWP):
    ''' 
        call this function after ApplyTopPick() has been called
        Therefore, we have to prepend the tagger with 'Higgs_'
    '''
    print('Obtaining efficiencies in {}'.format(SRorCR))
#DP EDIT
    start = analyzer.GetActiveNode()
    nTot = analyzer.DataFrame.Sum("genWeight").GetValue()
    print("nTot = {}".format(nTot))
    if (SRorCR == 'SR'):
       analyzer.Cut("Eff_{}_cut".format(SRorCR),"(Dijet_{0}[0] > {1}) && (Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP))
       nTSR = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTSR = {}".format(nTSR))
       analyzer.Cut("Eff_{}_PASS_cut".format(SRorCR),"(Diphoton_{2}[0] >= {3}) && (Diphoton_{2}[1] >= {3}) && (Dijet_{0}[0] > {1}) && (Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTPASS = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTPASS= {}".format(nTPASS))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAIL_cut".format(SRorCR),"((Diphoton_{2}[0] >= {3} && Diphoton_{2}[1] < {3}) || (Diphoton_{2}[1] >= {3} && Diphoton_{2}[0] < {3})) && (Dijet_{0}[0] > {1} && Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAIL= {}".format(nTFAIL))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAILFAIL_cut".format(SRorCR),"(Diphoton_{2}[0] < {3} && Diphoton_{2}[1] < {3}) && (Dijet_{0}[0] > {1} && Dijet_{0}[1] > {1})".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAILFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAILFAIL= {}".format(nTFAILFAIL))
    else:
       analyzer.Cut("Eff_{}_cut".format(SRorCR),"((Dijet_{0}[0] > {1}) && (Dijet_{0}[1] < {1})) || ((Dijet_{0}[1] > {1}) && (Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP))
       nTSR = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTCR = {}".format(nTSR))
       analyzer.Cut("Eff_{}_PASS_cut".format(SRorCR),"(Diphoton_{2}[0] >= {3} && Diphoton_{2}[1] >= {3}) && ((Dijet_{0}[0] > {1} && Dijet_{0}[1] < {1}) || (Dijet_{0}[1] > {1} && Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTPASS = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTPASS= {}".format(nTPASS))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAIL_cut".format(SRorCR),"((Diphoton_{2}[0] >= {3} && Diphoton_{2}[1] < {3}) || (Diphoton_{2}[1] >= {3} && Diphoton_{2}[0] < {3})) && ((Dijet_{0}[0] > {1} && Dijet_{0}[1] < {1}) || (Dijet_{0}[1] > {1} && Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAIL= {}".format(nTFAIL))
       analyzer.SetActiveNode(start)
       analyzer.Cut("Eff_{}_FAILFAIL_cut".format(SRorCR),"(Diphoton_{2}[0] < {3} && Diphoton_{2}[1] < {3}) && ((Dijet_{0}[0] > {1} && Dijet_{0}[1] < {1}) || (Dijet_{0}[1] > {1} && Dijet_{0}[0] < {1}))".format(Toptagger, ToptaggerWP, Stagger, StaggerWP))
       nTFAILFAIL = analyzer.DataFrame.Sum("genWeight").GetValue()
       print("nTFAILFAIL= {}".format(nTFAILFAIL))
    effPASS = nTPASS/nTot
    effFAIL = nTFAIL/nTot
    effFAILFAIL = nTFAILFAIL/nTot
    analyzer.SetActiveNode(start)
    print('{}: effPASS = {}%'.format(SRorCR, effPASS*100.))
    print('{}: effFAIL = {}%'.format(SRorCR, effFAIL*100.))
    print('{}: effFAILFAIL = {}%'.format(SRorCR, effFAILFAIL*100.))
    return effPASS, effFAIL, effFAILFAIL

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

def getPhotonEfficiencies(analyzer, tagger, wp, idx, tag):
    print('Obtaining efficiencies for photon at idx {}'.format(idx))
    start = analyzer.GetActiveNode()
    nTot = analyzer.DataFrame.Sum("genWeight").GetValue()
    print("nTot = {}".format(nTot))
    analyzer.Cut("Eff_photon{}_{}_cut".format(idx, tag),"{} >= {}".format(tagger, wp))
    nT = analyzer.DataFrame.Sum("genWeight").GetValue()
    print('nT = {}'.format(nT))
    eff = nT/nTot
    print('Photon: eff = {}'.format(eff*100.))
    analyzer.SetActiveNode(start)
    return eff

def TTselection(args):
    ROOT.ROOT.EnableImplicitMT(args.threads)
    start = time.time()
    signal = False

    print('Opening dijet_nano/{}_{}_snapshot.txt'.format(args.setname,args.era))
#DP EDIT
#    selection = THClass('dijet_nano/{}_{}_snapshot.txt'.format(args.setname,args.era),args.era,1,1)
    selection = TTClassSubleadVR18('dijet_nano/{}_{}_snapshot.txt'.format(args.setname,args.era),args.era,1,1)
    selection.OpenForSelection(args.variation)

    # apply HT cut due to improved trigger effs
    before = selection.a.DataFrame.Count()
    selection.a.Cut('HT_cut','HT > {}'.format(args.HT))
    after = selection.a.DataFrame.Count()
    # apply top tagger cut for orthogonal selection
    beforeT = selection.a.DataFrame.Count()
    if ('16APV' in args.era):
#        selection.a.Cut('topVRcut','Dijet_particleNet_TvsQCD[0] < 0.74 or Dijet_particleNet_TvsQCD[1] < 0.74')
       selection.a.Cut('top1_cut','Dijet_particleNet_TvsQCD[0] < 0.74')
       selection.a.Cut('top2_cut','Dijet_particleNet_TvsQCD[1] < 0.74')
    elif ('17' in args.era):
#        selection.a.Cut('topVRcut','Dijet_particleNet_TvsQCD[0] < 0.8 or Dijet_particleNet_TvsQCD[1] < 0.8')
       selection.a.Cut('top1_cut','Dijet_particleNet_TvsQCD[0] < 0.8')
       selection.a.Cut('top2_cut','Dijet_particleNet_TvsQCD[1] < 0.8')
    elif ('18' in args.era):
#        selection.a.Cut('topVRcut','Dijet_particleNet_TvsQCD[0] < 0.8 or Dijet_particleNet_TvsQCD[1] < 0.8')
       selection.a.Cut('top1_cut','Dijet_particleNet_TvsQCD[0] < 0.8')
       selection.a.Cut('top2_cut','Dijet_particleNet_TvsQCD[1] < 0.8')
    else:
#        selection.a.Cut('topVRcut','Dijet_particleNet_TvsQCD[0] < 0.73 or Dijet_particleNet_TvsQCD[1] < 0.73')
       selection.a.Cut('top1_cut','Dijet_particleNet_TvsQCD[0] < 0.73')
       selection.a.Cut('top2_cut','Dijet_particleNet_TvsQCD[1] < 0.73')
    afterT = selection.a.DataFrame.Count()

#    selection.ApplyTrigs(args.trigEff)
#    args.trigEff = Correction("TriggerEff%s"%args.era,'EffLoader_2DfittedHist.cc',['out_Eff_20%s.root'%args.era,'Eff_20%s'%args.era],corrtype='weight')
    selection.ApplyTrigs(args.trigEff)
    # scale factor application
    TopVar = 0
    print(args.variation)
    if ('StoAA' in args.setname):
	signal = True
	# Determine which SF we are varying 
	if (args.variation == 'PNetTop_up'):
	    TopVar = 1
	elif (args.variation == 'PNetTop_down'):
	    TopVar = 2

    print('VARIATIONS')
    print(TopVar)
    kinOnly = selection.a.MakeWeightCols(extraNominal='' if selection.a.isData else 'genWeight*%s'%selection.GetXsecScale())
    out = ROOT.TFile.Open('rootfilesMCsubleadVR/THselection_mvaID_subleadVR_HT%s_%s%s_%s%s.root'%(args.HT, args.setname,
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

	    print('----------------------- CONTROL REGION --------------------------------------------------------------')
	    # CONTROL REGION - ONE TOP REAL ONE NOT; APPLY TOP wp=0.73/0.74/0.8/0.8 for 2016/2016APV/2017/2018
	    selection.a.SetActiveNode(kinOnly)
            if ('16APV' in args.era):
                eff_CR_PASS, eff_CR_FAIL, eff_CR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'CR', top_tagger, 0.49, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatCRSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2016APV",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_CR_PASS, eff_CR_FAIL))
                passfailCR_SF = selection.ApplySTagTopTagSF('CR', top_tagger, 0.49, photon_tagger, 0.8)
            elif ('17' in args.era):
                eff_CR_PASS, eff_CR_FAIL, eff_CR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'CR', top_tagger, 0.58, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatCRSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2017",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_CR_PASS, eff_CR_FAIL))
                passfailCR_SF = selection.ApplySTagTopTagSF('CR', top_tagger, 0.58, photon_tagger, 0.8)
            elif ('18' in args.era):
                eff_CR_PASS, eff_CR_FAIL, eff_CR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'CR', top_tagger, 0.58, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatCRSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2018",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_CR_PASS, eff_CR_FAIL))
                passfailCR_SF = selection.ApplySTagTopTagSF('CR', top_tagger, 0.58, photon_tagger, 0.8)
            else:
                eff_CR_PASS, eff_CR_FAIL, eff_CR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'CR', top_tagger, 0.50, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatCRSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2016",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_CR_PASS, eff_CR_FAIL))
                passfailCR_SF = selection.ApplySTagTopTagSF('CR', top_tagger, 0.50, photon_tagger, 0.8)


	    # SIGNAL REGION
            print('----------------------- SIGNAL REGION --------------------------------------------------------------')
            selection.a.SetActiveNode(kinOnly)
#DP EDIT
            if ('16APV' in args.era):
                eff_SR_PASS, eff_SR_FAIL, eff_SR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'SR', top_tagger, 0.49, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2016APV",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_SR_PASS, eff_SR_FAIL))
                passfailSR_SF = selection.ApplySTagTopTagSF('SR', top_tagger, 0.49, photon_tagger, 0.8)
            elif ('17' in args.era):
                eff_SR_PASS, eff_SR_FAIL, eff_SR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'SR', top_tagger, 0.58, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2017",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_SR_PASS, eff_SR_FAIL))
                passfailSR_SF = selection.ApplySTagTopTagSF('SR', top_tagger, 0.58, photon_tagger, 0.8)
            elif ('18' in args.era):
                eff_SR_PASS, eff_SR_FAIL, eff_SR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'SR', top_tagger, 0.58, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2018",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_SR_PASS, eff_SR_FAIL))
                passfailSR_SF = selection.ApplySTagTopTagSF('SR', top_tagger, 0.58, photon_tagger, 0.8)
            else:
                eff_SR_PASS, eff_SR_FAIL, eff_SR_FAILFAIL = getSaaEfficienciesTag(selection.a, 'SR', top_tagger, 0.50, photon_tagger, 0.8)
                selection.a.Define('DiPhotonCatSF','updatePhotonTag(1,DiPhotonCat,Diphoton_pt,Diphoton_eta,Diphoton_mvaID,0.8,{0},{1},"2016",Diphoton_r9,Diphoton_isScEtaEE,Diphoton_isScEtaEB)'.format(eff_SR_PASS, eff_SR_FAIL))
                passfailSR_SF = selection.ApplySTagTopTagSF('SR', top_tagger, 0.50, photon_tagger, 0.8)


	# rkey: SR/CR, pfkey: pass/loose/fail

            print('ABOUT TO PLOT....')
            for rkey,rpair in {"SR":passfailSR_SF,"SR1":passfailCR_SF}.items():
              for pfkey,n in rpair.items():
                print(rkey)
                print(pfkey)
                if (rkey=='SR'):
                  if (pfkey=='fail'):
                    mod_name = "%s_%s_%s"%('TvsQCD_mvaID',"CR","pass")
                    mod_title = "%s %s"%("CR","pass")
                  elif (pfkey=='failfail'):
                    mod_name = "%s_%s_%s"%('TvsQCD_mvaID',"CR","fail")
                    mod_title = "%s %s"%("CR","fail")
                  else:
                    mod_name = "%s_%s_%s"%('TvsQCD_mvaID',rkey,pfkey)
                    mod_title = "%s %s"%(rkey,pfkey)
                else:
                  if (pfkey=='fail'):
                    mod_name = "%s_%s_%s"%('TvsQCD_mvaID',"CR1","pass")
                    mod_title = "%s %s"%("CR1","pass")
                  elif (pfkey=='failfail'):
                    mod_name = "%s_%s_%s"%('TvsQCD_mvaID',"CR1","fail")
                    mod_title = "%s %s"%("CR1","fail")
                  else:
                    mod_name = "%s_%s_%s"%('TvsQCD_mvaID',"SR1","pass")
                    mod_title = "%s %s"%("SR1","pass")
                print(mod_name)
                print(mod_title)
                selection.a.SetActiveNode(n)
                templates = selection.a.MakeTemplateHistos(ROOT.TH2F('MtpvMs_%s'%mod_name,'MtpvMs %s with %s'%(mod_title,'TvsQCD_mvaID'),16,25,825,26,425,3025),['Smass','mth'])
                templates.Do('Write')

#    '''
    # now process cutflow information
    cutflowInfo = OrderedDict([
#	('nTop_CR',selection.nTop_CR),
        ('Tot_CR',selection.higgs_CR_SF), 
	('P_CR',selection.higgsP_CR_SF),
	('F_CR',selection.higgsF_CR_SF),
	('FF_CR',selection.higgsFF_CR_SF),
#	('nTop_SR',selection.nTop_SR),
        ('Tot_SR',selection.higgs_SR_SF),
	('P_SR',selection.higgsP_SR_SF),
	('F_SR',selection.higgsF_SR_SF),
	('FF_SR',selection.higgsFF_SR_SF)
    ])

    nLabels = len(cutflowInfo)
    hCutflow = ROOT.TH1F('cutflow'.format(args.setname, args.era, args.variation), "Number of events after each cut", nLabels, 0.5, nLabels+0.5)
    nBin = 1
    for label, value in cutflowInfo.items():
	hCutflow.GetXaxis().SetBinLabel(nBin, label)
	hCutflow.AddBinContent(nBin, value)
	nBin += 1
    hCutflow.Write()
#    '''

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
#    if ('Data' not in args.setname) and (args.era == '17'): # we are dealing with MC from 2017
    if ('16APV' in args.era):
#        args.trigEff = Correction("TriggerEff16APV",'EffLoader_2DfittedHist.cc',['out_Eff_2016APV.root','Eff_2016APV'],corrtype='weight')
       args.trigEff = Correction("TriggerEff16APV",'TIMBER/Framework/include/EffLoader.h',['THtrigger2D_HT{}_16APV.root'.format(args.HT),'Pretag'], corrtype='weight')
    elif ('17' in args.era):
       cutoff = 0.059053
       TRand = ROOT.TRandom()
       rand = TRand.Uniform(0.0, 1.0)
       if rand < cutoff:       # apply the 2017B trigger efficiency to this MC
            print('Applying 2017B trigger efficiency')
            args.trigEff = Correction("TriggerEff17",'TIMBER/Framework/include/EffLoader.h',['THtrigger2D_HT{}_17B.root'.format(args.HT),'Pretag'], corrtype='weight')
       else:
            args.trigEff = Correction("TriggerEff17",'TIMBER/Framework/include/EffLoader.h',['THtrigger2D_HT{}_17XB.root'.format(args.HT),'Pretag'], corrtype='weight')
#        args.trigEff = Correction("TriggerEff17",'EffLoader_2DfittedHist.cc',['out_Eff_2017.root','Eff_2017'],corrtype='weight')
    elif ('18' in args.era):
#        args.trigEff = Correction("TriggerEff18",'EffLoader_2DfittedHist.cc',['out_Eff_2018.root','Eff_2018'],corrtype='weight')
       args.trigEff = Correction("TriggerEff18",'TIMBER/Framework/include/EffLoader.h',['THtrigger2D_HT{}_18.root'.format(args.HT),'Pretag'], corrtype='weight')
    else:
#        args.trigEff = Correction("TriggerEff16",'EffLoader_2DfittedHist.cc',['out_Eff_2016.root','Eff_2016'],corrtype='weight')
       args.trigEff = Correction("TriggerEff16",'TIMBER/Framework/include/EffLoader.h',['THtrigger2D_HT{}_16.root'.format(args.HT),'Pretag'], corrtype='weight')

#DP EDIT
    CompileCpp('TTmodules.cc')
    TTselection(args)
