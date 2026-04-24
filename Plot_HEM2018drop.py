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
    selection = TTClassLead('dijet_nano/DataC_18_snapshot.txt','18',1,1)

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
#    selection.a.Define('NewWeights','%s'%(HEM_worker.GetCall(evalArgs={"FatJet_eta":"Dijet_eta","FatJet_phi":"Dijet_phi","run":"run"})))
    selection.a.Define('NewWeights','HEM_dropData(Dijet_eta,Dijet_phi,run)')
#    selection.a.Define('NewWeights','HEM_worker.GetCall(Dijet_eta,Dijet_phi,run)')
    selection.a.Cut('HEM_veto_Data','NewWeights[0] > 0')

    nAfter = selection.getNweighted()
    print(nAfter)

    if 'Data' not in proc:
        selection.OpenForSelection('None',runCorrs=True)
        selection.a.MakeWeightCols(
            correctionNames = list(selection.a.GetCorrectionNames()),
            extraNominal = '{selection.GetXsecScale()}'
        )
        hist = selection.a.DataFrame.Histo2D(
            ('MC','MC',70,-3,3,70,-3.14,3.14),
            "Dijet_eta","Dijet_phi",
            "weight__nominal"
        )
    else:
        print('hist')
        hist = selection.a.DataFrame.Histo2D(
            ('Data','Data',70,-3,3,70,-3.14,3.14),
            "Dijet_eta","Dijet_phi"
        )


    # Plot
    c = ROOT.TCanvas(proc,proc,800,800)
    c.cd()
    hist.SetStats(0)
    hist.SetTitle('Data C 2018 after HEM veto')
    hist.GetXaxis().SetTitle('#eta')
    hist.GetYaxis().SetTitle('#phi')
    hist.Draw('colz')
    c.Print('plots/DataC_2018_HEM_veto_X.pdf')

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
