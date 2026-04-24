import ROOT, time
ROOT.gROOT.SetBatch(True)
from TIMBER.Tools.Common import CompileCpp
from TIMBER.Analyzer import analyzer, HistGroup, VarGroup, CutGroup
from argparse import ArgumentParser
#DP EDIT
#from THClass import THClass
from TTClassdR18 import TTClassdR18

parser = ArgumentParser()
parser.add_argument('-s', type=str, dest='setname',
                    action='store', required=True,
                    help='Setname to process.')
parser.add_argument('-y', type=str, dest='era',
                    action='store', required=True,
                    help='Year of set (16, 17, 18).')
parser.add_argument('-j', type=int, dest='ijob',
                    action='store', default=1,
                    help='Job number')
parser.add_argument('-n', type=int, dest='njobs',
                    action='store', default=1,
                    help='Number of jobs')
args = parser.parse_args()

start = time.time()

#DP EDIT
#CompileCpp('THmodules.cc')
CompileCpp('TTmodules.cc')
#selection = THClass('raw_nano/%s_%s.txt'%(args.setname,args.era),args.era,args.ijob,args.njobs)
selection = TTClassdR18('raw_nano/%s_%s.txt'%(args.setname,args.era),args.era,args.ijob,args.njobs)

flags = [
    'Flag_goodVertices',
    'Flag_globalSuperTightHalo2016Filter',
    'Flag_HBHENoiseFilter',
    'Flag_HBHENoiseIsoFilter',
    'Flag_EcalDeadCellTriggerPrimitiveFilter',
    'Flag_BadPFMuonFilter',
    'Flag_BadPFMuonDzFilter',
    'Flag_eeBadScFilter'
]

# Recommended selection 
MET_filters = selection.a.GetFlagString(flags)
selection.a.Cut('flags', MET_filters)
#selection.a.Cut('jetId', 'Jet_jetId[0] > 1 && Jet_jetId[1] > 1')
selection.a.Cut('nFatJet','nFatJet > 1')# at least 2 AK8 jets
selection.a.Cut('nPhoton', 'nPhoton > 1')
selection.a.Define('DijetIdxs','PickDijets(FatJet_pt,FatJet_eta,FatJet_phi,FatJet_msoftdrop)')
#selection.a.Define('DiphotonIdxs','PickDiphotonsLeadingOrdered(Photon_pt,Photon_eta,Photon_phi,Photon_mass)')
selection.a.Cut('dijetsExist','DijetIdxs[0] > -1 && DijetIdxs[1] > -1')
#selection.a.Define('DiphotonIdxs','PickDiphotons(Photon_pt,Photon_eta,Photon_phi,Photon_mass,Photon_cutBased)')
selection.a.Define('DiphotonIdxs2','PickDiphotons2(Photon_pt,Photon_eta,Photon_phi,Photon_mass,Photon_mvaID)')
#selection.a.Cut('diphotonsExist','DiphotonIdxs[0] > -1 && DiphotonIdxs[1] > -1')
selection.a.Cut('diphotonsExist','DiphotonIdxs2[0] > -1 && DiphotonIdxs2[1] > -1')
selection.a.SubCollection('Dijet','FatJet','DijetIdxs',useTake=True)
#selection.a.SubCollection('Diphoton','Photon','DiphotonIdxs',useTake=True)
selection.a.SubCollection('Diphoton2','Photon','DiphotonIdxs2',useTake=True)
selection.a.Cut('absEta','abs(Dijet_eta[0]) < 2.4 && abs(Dijet_eta[1]) < 2.4')
selection.a.Cut('deltaEta','abs(Dijet_eta[0]-Dijet_eta[1]) < 1.6')
selection.a.Cut('pt','Dijet_pt[0] > 350 && Dijet_pt[1] > 350')
selection.a.Cut('topTag','Dijet_particleNet_TvsQCD[0] > 0.8 && Dijet_particleNet_TvsQCD[1] > 0.8')
#selection.a.Cut('photonBaccept','(Diphoton_isScEtaEB[0] || Diphoton_isScEtaEE[0]) && (Diphoton_isScEtaEB[1] || Diphoton_isScEtaEE[1])')
selection.a.Cut('photonBaccept','(Diphoton2_isScEtaEB[0] || Diphoton2_isScEtaEE[0]) && (Diphoton2_isScEtaEB[1] || Diphoton2_isScEtaEE[1])')
selection.a.Cut('HT','Dijet_pt[0] + Dijet_pt[1] > 900')
#selection.a.Cut('photonNotElec','Diphoton_electronVeto[0]  && Diphoton_electronVeto[1]')
selection.a.Cut('photonNotElec','Diphoton2_electronVeto[0]  && Diphoton2_electronVeto[1]')
#selection.a.Cut('photonMvaID','Diphoton2_mvaID[0] > 0.8 && Diphoton2_mvaID[1] > 0.8')
#selection.a.Cut('photonWP80','Diphoton_mvaID_WP80[0] && Diphoton_mvaID_WP80[1]')
#selection.a.Cut('photonCutBased','Diphoton_cutBased[0] > -1 && Diphoton_cutBased[1] > -1')
selection.a.Cut('mtop_cut','Dijet_msoftdrop[0] > 50 && Dijet_msoftdrop[1] > 50')
selection.a.Cut('dphPt','Diphoton2_pt[0] > 25 && Diphoton2_pt[1] > 25.0')
norm = selection.GetXsecScale()
#norm = 1.0
selection.a.Define('norm',str(norm))

# VarGroup to store info about jets and photons
jets = VarGroup('Dijets')
jets.Add('lead_vect',"hardware::TLvector(Dijet_pt[0], Dijet_eta[0], Dijet_phi[0], Dijet_msoftdrop[0])")
jets.Add('sublead_vect','hardware::TLvector(Dijet_pt[1], Dijet_eta[1], Dijet_phi[1], Dijet_msoftdrop[1])')
#jets.Add('deltaEta', 'Dijet_eta[0]')
#jets.Add('deltaEta', 'abs(lead_vect.Eta() - sublead_vect.Eta())')
#jets.Add('mtphi','hardware::InvariantMass({lead_vect,sublead_vect})')
#jets.Add('topTag','Dijet_deepTag_TvsQCD[0]')
#jets.Add('TvsQCD1','Dijet_deepTag_TvsQCD[1]')
# VarGroup to store info about photons
#photons = VarGroup('Diphotons')
#jets.Add('Alead_vect',"hardware::TLvector(Diphoton_pt[0], Diphoton_eta[0], Diphoton_phi[0], Diphoton_mass[0])")
#jets.Add('Asublead_vect','hardware::TLvector(Diphoton_pt[1], Diphoton_eta[1], Diphoton_phi[1], Diphoton_mass[1])')
jets.Add('Alead2_vect',"hardware::TLvector(Diphoton2_pt[0], Diphoton2_eta[0], Diphoton2_phi[0], Diphoton2_mass[0])")
jets.Add('Asublead2_vect','hardware::TLvector(Diphoton2_pt[1], Diphoton2_eta[1], Diphoton2_phi[1], Diphoton2_mass[1])')
#photons.Add('AdeltaEta', 'abs(Alead_vect.Eta() - Asublead_vect.Eta())')
#photons.Add('Amass','hardware::InvariantMass({Alead_vect,Asublead_vect})')
#photons.Add('AdeltaR','hardware::DeltaR({Alead_vect,Asublead_vect})')

jets.Add('Photon1_vect','hardware::TLvector(Diphoton2_pt[0],Diphoton2_eta[0], Diphoton2_phi[0], Diphoton2_mass[0])')
jets.Add('Photon2_vect','hardware::TLvector(Diphoton2_pt[1],Diphoton2_eta[1], Diphoton2_phi[1], Diphoton2_mass[1])')
jets.Add('Top1_vect','hardware::TLvector(Dijet_pt[0], Dijet_eta[0], Dijet_phi[0], Dijet_msoftdrop[0])')
jets.Add('Top2_vect','hardware::TLvector(Dijet_pt[1], Dijet_eta[1], Dijet_phi[1], Dijet_msoftdrop[1])')
jets.Add('Smass','hardware::InvariantMass({Photon1_vect,Photon2_vect})')
#jets.Add('mth1','hardware::InvariantMass({Top1_vect,Photon1_vect,Photon2_vect})')
#jets.Add('mth2','hardware::InvariantMass({Top2_vect,Photon1_vect,Photon2_vect})')
#jets.Add('StoAAid0','FindID0StoAA(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)')
#jets.Add('topID','FindIDtopWithS(StoAAid0,nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)')
#jets.Add('gen_vect',"hardware::TLvector(GenPart_pt[topID], GenPart_eta[topID], GenPart_phi[topID], GenPart_mass[topID])")
#jets.Add('Sgen_vect',"hardware::TLvector(GenPart_pt[StoAAid0], GenPart_eta[StoAAid0], GenPart_phi[StoAAid0], GenPart_mass[StoAAid0])")
#jets.Add('dRgen','hardware::DeltaR(gen_vect,Sgen_vect)')
jets.Add('Svec','Photon1_vect+Photon2_vect')
jets.Add('dRj0','hardware::DeltaR(Top1_vect,Svec)')
jets.Add('dRj1','hardware::DeltaR(Top2_vect,Svec)')
#jets.Add('dtopRj0','hardware::DeltaR(Top1_vect,gen_vect)')
#jets.Add('dtopRj1','hardware::DeltaR(Top2_vect,gen_vect)')
jets.Add('topchoice','int(dRj0 > 0.8)*int(dRj0>dRj1)')
jets.Add('seldR','topchoice*dRj0 + (1.0-topchoice)*dRj1')
jets.Add('aliasdR','topchoice*dRj1 + (1.0-topchoice)*dRj0')
#jets.Add('topGENchoice','int(dtopRj0>dtopRj1)')
#jets.Add('iphot','int(nPhoton==2)')
#jets.Add('topGENchoice','iphot*int(dtopRj0<dtopRj1)+(1-iphot)*int(dtopRj0>dtopRj1)')
#jets.Add('topGENchoice','int(abs(dRj0-dRgen)<abs(dRj1-dRgen))')

# Plotting variables
plotting_vars = VarGroup('plotting_vars')
#plotting_vars.Add('icorrect','int(topchoice==topGENchoice)')
#plotting_vars.Add('iincorrect','int(!(topchoice==topGENchoice))')
#DP EDIT
#plotting_vars.Add('dRgen','hardware::DeltaR(gen_vect,Sgen_vect)')
plotting_vars.Add('dR0','dRj0')
plotting_vars.Add('dR1','dRj1')
plotting_vars.Add('SeldR','seldR')
plotting_vars.Add('AliasdR','aliasdR')
#jets.Add('diff0a','abs(dRj0-1.8)')
#jets.Add('diff0b','abs(dRj0-2.5)')
#jets.Add('ichoice1','int(diff0a<diff0b)')
#jets.Add('diff0c','ichoice1*diff0a+(1-ichoice1)*diff0b')
#jets.Add('diff0d','abs(dRj0-3.2)')
#jets.Add('jchoice1','int(diff0c<diff0d)')
#jets.Add('diff0','jchoice1*diff0c+(1-jchoice1)*diff0c')
#jets.Add('diff1a','abs(dRj1-1.8)')
#jets.Add('diff1b','abs(dRj1-2.5)')
#jets.Add('ichoice2','int(diff1a<diff1b)')
#jets.Add('diff1c','ichoice2*diff1a+(1-ichoice2)*diff1b')
#jets.Add('diff1d','abs(dRj1-3.2)')
#jets.Add('jchoice2','int(diff1c<diff1d)')
#jets.Add('diff1','jchoice2*diff1c+(1-jchoice2)*diff1c')
#jets.Add('diff0','abs(dRj0-2.6)')
#jets.Add('diff1','abs(dRj1-2.2)')
#jets.Add('ichoiceX','int(diff0<diff1)')
#jets.Add('ichoice','int((dRj1 < 1.2) || (dRj0 > 0.8))')
#jets.Add('ichoice','int((dRj1 < 2.0) || (dRj0 > dRj1))')
#jets.Add('ichoice','int(dRj0 > 0.8)*(int(dRj1<2.0)+int(dRj1>2.0)*int(dRj0 > dRj1))')
#jets.Add('ichoice','int(dRj0 > 0.8)*int(dRj0 > dRj1)')
#plotting_vars.Add('dRselection1','ichoice*dRj0+(1-ichoice)*dRj1')
#plotting_vars.Add('dRselection2','ichoiceX*dRj0+(1-ichoiceX)*dRj1')
#jets.Add('ichoicegentop','int(dtopRj0<dtopRj1)')
#plotting_vars.Add('dRsignal','ichoicegentop*dRj0+(1-ichoicegentop)*dRj1')
#plotting_vars.Add('dRreflection','ichoicegentop*dRj1+(1-ichoicegentop)*dRj0')
#plotting_vars.Add('dRselsig','int(ichoice==ichoicegentop)*(ichoice*dRj0+(1-ichoice)*dRj1)')
#plotting_vars.Add('dtopR','ichoicegentop*dtopRj0+(1-ichoicegentop)*dtopRj1')
#jets.Add('mth1','hardware::InvariantMass({Top1_vect,Photon1_vect,Photon2_vect})')
#jets.Add('mth2','hardware::InvariantMass({Top2_vect,Photon1_vect,Photon2_vect})')
#plotting_vars.Add('mthsel1','ichoice*mth1+(1-ichoice)*mth2')
#plotting_vars.Add('mthsel2','ichoiceX*mth1+(1-ichoiceX)*mth2')
#plotting_vars.Add('mthsig','ichoicegentop*mth1+(1-ichoicegentop)*mth2')
#plotting_vars.Add('mthref','ichoicegentop*mth2+(1-ichoicegentop)*mth1')
#plotting_vars.Add('mth1x','mth1')
#plotting_vars.Add('mth2x','mth2')
#plotting_vars.Add('mtop','Dijet_msoftdrop[0]')
#plotting_vars.Add('mtop1','Dijet_msoftdrop[1]')
#plotting_vars.Add('Apt','Diphoton_pt[0]')
#plotting_vars.Add('AptCutBased','Diphoton_pt[0]')
#plotting_vars.Add('AptMvaID','Diphoton2_pt[0]')
#plotting_vars.Add('Apt1','Diphoton_pt[1]')
#plotting_vars.Add('AdeltaEta','AdeltaEta')
#plotting_vars.Add('deltaEta','abs(Dijet_eta[0]-Dijet_eta[1])')
#plotting_vars.Add('pt','Dijet_pt[0]')
#plotting_vars.Add('pt0','Dijet_pt[0]')
#plotting_vars.Add('pt1','Dijet_pt[1]')
#plotting_vars.Add('Amass','Amass')
#plotting_vars.Add('topTag','Dijet_particleNet_TvsQCD[0]')
#plotting_vars.Add('topTag0','TvsQCD0')
#plotting_vars.Add('topTag1','TvsQCD1')
#plotting_vars.Add('AdR','AdeltaR')
#plotting_vars.Add('SmassCutBased','hardware::InvariantMass({Alead_vect,Asublead_vect})')
#plotting_vars.Add('TPmassCutBased','hardware::InvariantMass({lead_vect,Alead_vect,Asublead_vect})')
#plotting_vars.Add('SmassMvaID','hardware::InvariantMass({Alead2_vect,Asublead2_vect})')
#plotting_vars.Add('TPmassMvaID','hardware::InvariantMass({lead_vect,Alead2_vect,Asublead2_vect})')
#plotting_vars.Add('tmass','hardware::InvariantMass({lead_vect,sublead_vect})')
#plotting_vars.Add('deltaR','hardware::DeltaR(Alead_vect,Asublead_vect)')
#plotting_vars.Add('photonCutBased','Diphoton_cutBased[0]')
#plotting_vars.Add('photonMvaID','Diphoton2_mvaID[0]')
#plotting_vars.Add('dPhi','abs(Dijet_phi[0]-Dijet_phi[1])')
#plotting_vars.Add('AdPhi','abs(Diphoton_phi[0]-Diphoton_phi[1])')
#plotting_vars.Add('METpt','MET_pt')
#plotting_vars.Add('METsumEt','MET_sumEt')

# N-1 cuts to make
NCuts = CutGroup('NCuts')
#NCuts.Add('icorrect','icorrect > 0')
#NCuts.Add('iincorrect','iincorrect > 0')
#NCuts.Add('dRgen','dRgen > -1.0')
NCuts.Add('dR0','dR0 > -1.0')
NCuts.Add('dR1','dR1 > -1.0')
#NCuts.Add('dRselection1','dRselection1 > -1.0')
#NCuts.Add('dRselection2','dRselection2 > -1.0')
NCuts.Add('SeldR','SeldR > -1.0')
NCuts.Add('AliasdR','AliasdR > -1.0')
#NCuts.Add('dRreflection','dRreflection > -1.0')
#NCuts.Add('dtopR','dtopR < 6.4')
#NCuts.Add('mthsel1','mthsel1 > 0.0')
#NCuts.Add('mthsel2','mthsel2 > 0.0')
#NCuts.Add('mthsig','mthsig > 0.0')
#NCuts.Add('mthref','mthref > 0.0')
#NCuts.Add('mth1x','mth1x > 0.0')
#NCuts.Add('mth2x','mth2x > 0.0')
#NCuts.Add('mth1','mth1 > 0.0 && mth1 < 3000.0')
#NCuts.Add('mth2','mth2 > 0.0 && mth2 < 3000.0')
#NCuts.Add('deltaEta_cut','deltaEta < 1.6')
#NCuts.Add('pt_cut','Dijet_pt[0] > 350 && Dijet_pt[1] > 350')
#NCuts.Add('absEta_cut','abs(Dijet_eta[0]) < 2.4 && abs(Dijet_eta[1]) < 2.4')
#NCuts.Add('mtop_cut','Dijet_msoftdrop[0] > 50 && Dijet_msoftdrop[1] > 50')
#NCuts.Add('topTag_cut','(Dijet_particleNet_TvsQCD[0] > 0.8 && Dijet_particleNet_TvsQCD[1] < 0.8) || (Dijet_particleNet_TvsQCD[0] < 0.8 && Dijet_particleNet_TvsQCD[1] > 0.8)')
#NCuts.Add('topTag_cut','Dijet_particleNet_TvsQCD[0] > 0.8 && Dijet_particleNet_TvsQCD[1] > 0.8')
# dummy cuts so we can plot values of interest
#NCuts.Add('AptCutBased_cut','Diphoton_pt[0] > 25 && Diphoton_pt[1] > 25')
#NCuts.Add('AptMvaID_cut','Diphoton2_pt[0] > 25 && Diphoton2_pt[1] > 25')
#NCuts.Add('deltaR_cut','deltaR < 6.0')
#NCuts.Add('Smass_cut','Smass>5')
#NCuts.Add('tmass_cut','tmass>5')
#NCuts.Add('Amass','Amass < 400')
#NCuts.Add('photonTag_cut','(Diphoton_cutBased[0] > 1 && Diphoton_cutBased[1] < 2) || (Diphoton_cutBased[0] < 2 && Diphoton_cutBased[1] > 1)')
#NCuts.Add('photonCutBased_cut','Diphoton_cutBased[0] > -1 && Diphoton_cutBased[1] > -1')
#NCuts.Add('photonMvaID_cut','(Diphoton_mvaID[0] > -0.91 && Diphoton_mvaID[1] < -0.91) || (Diphoton_mvaID[0] < -0.91 && Diphoton_mvaID[1] > -0.91)')
#NCuts.Add('photonMvaID_cut','Diphoton2_mvaID[0] > -1.01 && Diphoton2_mvaID[1] > -1.01')
#NCuts.Add('photonNOTelecTag_cut','Diphoton_electronVeto[0] && Diphoton_electronVeto[1]')
#NCuts.Add('dPhi_cut','abs(Dijet_phi[0]-Dijet_phi[1])>1.5')
#NCuts.Add('AdPhi_cut','abs(Diphoton_phi[0]-Diphoton_phi[1])<6.4')
#NCuts.Add('TPmassCutBased_cut','TPmassCutBased > 0.0')
#NCuts.Add('SmassCutBased_cut','SmassCutBased>0.0')
#NCuts.Add('TPmassMvaID_cut','TPmassMvaID > 0.0')
#NCuts.Add('SmassMvaID_cut','SmassMvaID>0.0')
#NCuts.Add('METpt_cut','METpt>0.0')
#NCuts.Add('METsumEt_cut','METsumEt>0.0')

nodeToPlot = selection.a.Apply([jets,plotting_vars])
#nodeToPlot = selection.a.Apply([photons,plotting_vars])
nminus1Nodes = selection.a.Nminus1(NCuts, node=nodeToPlot)
nminus1Hists = HistGroup('nminus1Hists')

oFile = ROOT.TFile.Open('rootfiles/NMinus1_dRselFIN_{}_{}_{}of{}.root'.format(args.setname, args.era, args.ijob, args.njobs),'RECREATE')
oFile.cd()
binning = {
#    'mth1':[25,200,3025],
#    'mth2':[25,200,3025],
#    'mthsel1':[40,200,3025],
#    'mthsel2':[40,200,3025],
#    'mthsig':[40,200,3025],
#    'mthref':[40,200,3025],
#    'mth1x':[40,200,3025],
#    'mth2x':[40,200,3025],
#    'dRgen':[40,0,4.5],
    'dR0':[40,0,4.5],
    'dR1':[40,0,4.5],
#    'dRselection1':[40,0,4.5],
#    'dRselection2':[40,0,4.5],
    'SeldR':[40,0,4.5],
#    'dRsignal':[40,0,4.5],
    'AliasdR':[40,0,4.5]
#    'dtopR':[40,0,4.5],
#    'mtop':[25,0,300],
#    'mtphi':[25,800,2200],
#    'mphi':[25,50,270],
#    'pt':[25,200,1600],
#    'AptMvaID':[25,0,1200],
#    'AptCutBased':[25,0,1200],
#    'pt0':[25,200,2200],
#    'pt1':[25,200,2200],
#    'deltaEta':[20,0,3.5],
#    'topTag':[20,0,1.0],
#    'photonCutBased':[5,0,4],
#    'photonMvaID':[40,-1.0,1.0],
#    'photonNOTelecTag':[2,False,True],
#    'SmassCutBased':[25,0,1200],
#    'TPmassCutBased':[25,200,3200],
#    'SmassMvaID':[25,0,1200],
#    'TPmassMvaID':[25,200,3200],
#    'METpt':[25,0,1200],
#    'METsumEt':[25,0,1200]
#    'tmass':[25,200,3200],
#    'deltaR':[20,0,6.0],
#    'dPhi':[20,0.0,6.0],
#    'AdPhi':[20,0.0,6.0]
#    'topTag0':[20,0,1.0],
#    'topTag1':[20,0,1.0]
#    'icorrect':[2,0,1],
#    'iincorrect':[2,0,1]
}

print('Plotting')
print(nminus1Nodes)
for nkey in nminus1Nodes.keys():
    print('1')
    if nkey=='full': continue
    print('\t{}'.format(nkey))
#    if ('mtop' not in nkey) and ('pt0' not in nkey) and ('pt1' not in nkey) and ('deltaEta' not in nkey) and ('topTag0' not in nkey) and ('topTag1' not in nkey):
    if ('SeldR'  not in nkey) and  ('AliasdR'  not in nkey) and ('mth'  not in nkey) and ('dRselection1'  not in nkey) and ('dRgen'  not in nkey) and ('dR0'  not in nkey) and ('dR1'  not in nkey) and ('dRsignal' not in nkey) and ('dRreflection' not in nkey) and ('dtopR' not in nkey) and ('dRselsig' not in nkey) and ('mthsel1' not in nkey) and ('mthsig' not in nkey) and ('mthref' not in nkey) and ('mth1x' not in nkey) and ('mth2x' not in nkey) and ('dRselection2' not in nkey) and ('deltaR' not in nkey) and ('mthsel2' not in nkey) and ('mtop' not in nkey) and ('pt' not in nkey) and ('deltaEta' not in nkey) and ('topTag' not in nkey):
	continue
    print('2')	
    var = nkey.replace('_cut','').replace('minus_','')
    print('3')
    hist_tuple = (var,var,binning[var][0],binning[var][1],binning[var][2])
    print('4')
    hist = nminus1Nodes[nkey].DataFrame.Histo1D(hist_tuple,var,'norm')
    print('5')
    hist.GetValue()
    print('6')
    nminus1Hists.Add(var,hist)

print('X1')
nminus1Hists.Do('Write')
print('X2')
oFile.Close()

print ('%s sec'%(time.time()-start))
