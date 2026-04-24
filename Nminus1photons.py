import ROOT, time
ROOT.gROOT.SetBatch(True)
from TIMBER.Tools.Common import CompileCpp
from TIMBER.Analyzer import analyzer, HistGroup, VarGroup, CutGroup
from argparse import ArgumentParser
#DP EDIT
#from THClass import THClass
from TTClass import TTClass

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
selection = TTClass('raw_nano/%s_%s.txt'%(args.setname,args.era),args.era,args.ijob,args.njobs)

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
selection.a.Cut('jetId', 'Jet_jetId[0] > 1 && Jet_jetId[1] > 1')
selection.a.Cut('nPhoton', 'nPhoton > 1')
selection.a.Define('DijetIdxs','PickDijets(FatJet_pt,FatJet_eta,FatJet_phi,FatJet_mass)')
selection.a.Define('DiphotonIdxs','PickDiphotonsLeadingOrdered(Photon_pt,Photon_eta,Photon_phi,Photon_mass)')
selection.a.Cut('dijetsExist','DijetIdxs[0] > -1 && DijetIdxs[1] > -1')
selection.a.Cut('diphotonsExist','DiphotonIdxs[0] > -1 && DiphotonIdxs[1] > -1')
#selection.a.Cut('absEta','abs(Dijet_eta[0]) < 2.4 && abs(Dijet_eta[1]) < 2.4')
#selection.a.SubCollection('Dijet','FatJet','DijetIdxs',useTake=True)
selection.a.SubCollection('Diphoton','Photon','DiphotonIdxs',useTake=True)

norm = selection.GetXsecScale()
selection.a.Define('norm',str(norm))

# VarGroup to store info about jets
#jets = VarGroup('Dijets')
#jets.Add('lead_vect',"hardware::TLvector(Dijet_pt[0], Dijet_eta[0], Dijet_phi[0], Dijet_msoftdrop[0])")
#jets.Add('sublead_vect','hardware::TLvector(Dijet_pt[1], Dijet_eta[1], Dijet_phi[1], Dijet_msoftdrop[1])')
#jets.Add('deltaEta', 'abs(lead_vect.Eta() - sublead_vect.Eta())')
#jets.Add('mtphi','hardware::InvariantMass({lead_vect,sublead_vect})')
#jets.Add('TvsQCD0','Dijet_deepTag_TvsQCD[0]')
#jets.Add('TvsQCD1','Dijet_deepTag_TvsQCD[1]')
# VarGroup to store info about photons
photons = VarGroup('Diphotons')
photons.Add('lead_vect',"hardware::TLvector(Diphoton_pt[0], Diphoton_eta[0], Diphoton_phi[0], Diphoton_mass[0])")
photons.Add('sublead_vect','hardware::TLvector(Diphoton_pt[1], Diphoton_eta[1], Diphoton_phi[1], Diphoton_mass[1])')
#photons.Add('deltaEta', 'abs(lead_vect.Eta() -sublead_vect.Eta())')
#photons.Add('Smass','hardware::InvariantMass({lead_vect,sublead_vect})')
#photons.Add('deltaR','hardware::DeltaR(lead_vect,sublead_vect)')

# Plotting variables
plotting_vars = VarGroup('plotting_vars')
#DP EDIT
#plotting_vars.Add('mtop','Dijet_msoftdrop[0]')
#plotting_vars.Add('mtop1','Dijet_msoftdrop[1]')
plotting_vars.Add('pt','Diphoton_pt[0]')
#plotting_vars.Add('pt1','Diphoton_pt[1]')
plotting_vars.Add('deltaEta','abs(Diphoton_eta[0]-Diphoton_eta[1])')
#plotting_vars.Add('deltaEta','deltaEta')
#plotting_vars.Add('pt','Dijet_pt[0]')
plotting_vars.Add('Smass','hardware::InvariantMass({lead_vect,sublead_vect})')
#plotting_vars.Add('topTag0','TvsQCD0')
#plotting_vars.Add('topTag1','TvsQCD1')
plotting_vars.Add('deltaR','hardware::DeltaR(lead_vect,sublead_vect)')

# N-1 cuts to make
NCuts = CutGroup('NCuts')
#NCuts.Add('deltaEta_cut','deltaEta < 1.6')
#NCuts.Add('pt_cut','Dijet_pt[0] > 350 && Dijet_pt[1] > 350')
#NCuts.Add('absEta_cut','abs(Dijet_eta[0]) < 2.4 && abs(Dijet_eta[1]) < 2.4')
#NCuts.Add('mtop_cut','Dijet_msoftdrop[0] > 50 && Dijet_msoftdrop[1] > 50')
# dummy cuts so we can plot values of interest
NCuts.Add('pt_cut','Diphoton_pt[0]>50 && Diphoton_pt[1]>50')
#NCuts.Add('pt1_cut','Diphoton_pt[0]>50 && Diphoton_pt[1]>50')
NCuts.Add('deltaEta_cut','deltaEta < 2.4')
#NCuts.Add('mass_cut','Smass < 500')
NCuts.Add('Smass_cut','Smass > 15')
NCuts.Add('deltaR_cut','deltaR < 4.0')

nodeToPlot = selection.a.Apply([photons,plotting_vars])
#nodeToPlot = selection.a.Apply([photons,plotting_vars])
nminus1Nodes = selection.a.Nminus1(NCuts, node=nodeToPlot)
nminus1Hists = HistGroup('nminus1Hists')

oFile = ROOT.TFile.Open('rootfiles/NMinus1_photons_{}_{}_{}of{}.root'.format(args.setname, args.era, args.ijob, args.njobs),'RECREATE')
oFile.cd()
binning = {
#    'pt0':[25,0,1200],
#    'pt1':[25,0,1200],
#    'mtphi':[25,800,2200],
#    'mphi':[25,50,270],
    'pt':[25,200,2200],
    'deltaEta':[20,0,3.5],
    'Smass':[25,0,1200],
    'deltaR':[20,0,6.0]
}

print('Plotting')
print(nminus1Nodes)
for nkey in nminus1Nodes.keys():
    print('1')
    if nkey=='full': continue
    print('\t{}'.format(nkey))
#    if ('pt0' not in nkey) and ('pt1' not in nkey) and ('deltaEta' not in nkey) and ('mass' not in nkey) and ('dR' not in nkey):
    if ('pt' not in nkey) and ('deltaEta' not in nkey) and ('Smass' not in nkey) and ('deltaR' not in nkey):
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
