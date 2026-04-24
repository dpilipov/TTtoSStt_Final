'''
Script to plot the full 2018 dataset before and after applying the HEM correction
'''
from collections import OrderedDict
from TTClassLead import TTClassLead
from TIMBER.Analyzer import Correction, CutGroup, ModuleWorker, analyzer
from argparse import ArgumentParser
import ROOT
from TIMBER.Tools.Common import CompileCpp


def plot(proc):
    print('Running over')
    print(proc)
    print('2018 dataset....')
    selection = TTClassLead('dijet_nano/ttbar-allhad_18_snapshot.txt','18',1,1)
#    selection.OpenForSelection('None')

    nBefore = selection.getNweighted()
    print(nBefore)
#    nBnum = nBefore.GetValue()
#    print(nBnum)

    HEM_worker = ModuleWorker('HEM_drop','TIMBER/Framework/include/HEM_drop.h',[proc])
#    if 'Data' in proc:
#        selection.a.Cut('HEM_veto_Data','%s == 0.0'%(HEM_worker.GetCall(evalArgs={"FatJet_eta":"Dijet_eta[0]","FatJet_phi":"Dijet_phi[0]","run":"run"})))
#    else:
#        selection.a.Cut('HEM_veto_MC','%s == 0.0'%(HEM_worker.GetCall(evalArgs={"FatJet_eta":"Dijet_eta","FatJet_phi":"Dijet_phi","run":"run"})))
    selection.a.Define('Dijeteta0','Dijet_eta[0]')
    selection.a.Define('Dijetphi0','Dijet_phi[0]')

#    selection.a.Define('NewWeights',HEM_worker.GetCall(evalArgs={"FatJet_eta":"Dijeteta0","FatJet_phi":"Dijetphi0","run":"run"}))
#    selection.a.Define('NewWeights','%s'%(HEM_worker.GetCall(evalArgs={"FatJet_eta":"Dijet_eta","FatJet_phi":"Dijet_phi"})))
    selection.a.Define('NewWeights','HEM_dropMC(Dijet_eta,Dijet_phi)')
    selection.a.Cut('HEM_veto_MC','NewWeights[0]>0.0')
#    selection.a.Cut('HEM_veto_MC','NewWeights[1]>0.0')

    nAfter = selection.getNweighted()
    print(nAfter)

#    lumi = self.config['lumi{}'.format(self.year if 'APV' not in self.year else 16)]
#    xsec = self.config['XSECS'][self.setname]
#        if self.a.genEventSumw == 0:
#            raise ValueError('%s %s: genEventSumw is 0'%(self.setname, self.year))
#        return lumi*xsec/self.a.genEventSumw
    
    selection.a.Define('lumi','59692.687741')
    selection.a.Define('xsec','378.93') 
    selection.a.Define('nAft','120811213.271')
    selection.a.Define('extN','lumi*xsec/nAft') 
    selection.a.MakeWeightCols(
            correctionNames = list(selection.a.GetCorrectionNames()),
            extraNominal = 'extN'
        )
    hist = selection.a.DataFrame.Histo2D(
            ('MC','MC',70,-3,3,70,-3.14,3.14),
            "Dijet_eta","Dijet_phi",
            "weight__nominal"
        )
#    else:
#        hist = selection.a.DataFrame.Histo2D(
#            ('ttbar-allhad','ttbar-allhad',70,-3,3,70,-3.14,3.14),
#            "Dijet_eta","Dijet_phi"
#        )


    # Plot
    c = ROOT.TCanvas(proc,proc,800,800)
    c.cd()
    hist.SetStats(0)
    hist.SetTitle('ttbar-allhad 2018 after HEM veto')
    hist.GetXaxis().SetTitle('#eta')
    hist.GetYaxis().SetTitle('#phi')
    hist.Draw('colz')
    c.Print('plots/MC_2018_HEM_veto.pdf')

#    ratio = nAfter.GetValue()/nBefore.GetValue()
    ratio = nAfter/nBefore
    leftover = 1.0 - ratio
    print('Loss of events after HEM veto',leftover)

parser = ArgumentParser()
parser.add_argument('-s', type=str, dest='setname',
                    action='store', required=True,
                    help='Setname to process.')
args = parser.parse_args()

proc = args.setname

CompileCpp('TTmodules.cc')
plot(proc)
