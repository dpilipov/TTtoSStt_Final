import sys, time, ROOT
from collections import OrderedDict

from TIMBER.Analyzer import HistGroup
from TIMBER.Tools.Common import CompileCpp
#DP EDIT
#from THClass import THClass
from TTClass import TTClass

def MakeEfficiency(year, HT=0):
#DP EDIT
#    '''
#        year (str) : 16, 17, 17B, 17All, 18
#         year (str): 16, 16APV, 17, 18
#    year (str) : 16
#        HT   (int) : value of HT to cut on
#    '''
    '''
        year (str) : 18
    '''

    # For measuring trigger efficiencies, we use the data from the orthogonal SingleMuon dataset
    # For 2017, we need to ensure that the 2017B dataset is evaluated separately and its own efficiency is generated
    # so that it may be applied to a fraction of the 2017 MC corresponding to the contribution of 2017B to the total
    # 2017 dataset.
    # We must also evaluate the 2017C, 2017D, 2017E and 2017F datasets combined together, since they share triggers which
    # result in higher efficiencies than with the inclusion of the 2017B dataset.
#DP EDIT
#    if year == '17B':
#	fName = 'dijet_nano/SingleMuonDataB_17_snapshot.txt'
#    elif year == '17All':
#        fName = 'dijet_nano/SingleMuonDataWithB_17_snapshot.txt'
#    else:
#    fName = 'dijet_nano/SingleMuonData_18_snapshot.txt'
    fName = 'dijet_nano/ttbar-allhad_18_snapshot.txt'
#        fName = 'dijet_nano/SingleMuonData_{}_snapshot.txt'.format(year)
#DP EDIT
#    selection = TTClass(fName,year if 'B' not in year else '17',1,1)
    selection = TTClass(fName,year,1,1)
    print(selection.year)
    selection.OpenForSelection('None')
    hists = HistGroup('out')

    # cut on HT to improve efficiency
    before = selection.a.DataFrame.Count()
    selection.a.Cut('HT_cut', 'HT > {}'.format(HT))
    after = selection.a.DataFrame.Count()

    noTag = selection.a.Cut('pretrig','HLT_Mu50==1')

    # Baseline - no tagging
#    hists.Add('preTagDenominator',selection.a.DataFrame.Histo2D(('preTagDenominator','',16,25,825,24,625,3025),'Smass_trig','mth_trig'))
#    hists.Add('preTagDenominator',selection.a.DataFrame.Histo2D(('preTagDenominator','',16,25,825,30,25,3025),'Smass_trig','mth_trig'))
#    hists.Add('preTagDenominatorZoomed', selection.a.DataFrame.Histo2D(('preTagDenominatorZoomed','',8,25,425,12,625,1825),'Smass_trig','mth_trig'))
    hists.Add('preTagDenominatorHT',selection.a.DataFrame.Histo1D(('preTagDenominatorHT','',30,325,3025),'HT'))
    histDenHT = hists['preTagDenominatorHT']
    hists.Add('preTagDenominatorTpt',selection.a.DataFrame.Histo1D(('preTagDenominatorTpt','',30,325,3025),'pt0'))
    histDenTpt = hists['preTagDenominatorTpt']
    hists.Add('preTagDenominatorApt',selection.a.DataFrame.Histo1D(('preTagDenominatorApt','',30,25,3025),'Apt0'))
    histDenApt = hists['preTagDenominatorApt']
#    selection.ApplyTrigs()
#    yesTag = selection.a.Cut('posttrig','((HLT_PFHT500_PFMET100_PFMHT100_IDTight==1) || (HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4==1) || (HLT_AK8PFJet60==1) || (HLT_AK8PFJet80==1) || (HLT_PFHT1050==1) || (HLT_AK8PFHT800_TrimMass50==1) || (HLT_AK8PFJet500==1) || (HLT_AK8PFJet400_TrimMass30==1) || (HLT_AK8PFHT750_TrimMass50==1))')
# || (HLT_DoublePhoton85==1))')
#    hists.Add('preTagNumerator',selection.a.DataFrame.Histo2D(('preTagNumerator','',16,25,825,24,625,3025),'Smass_trig','mth_trig'))
    yesTag = selection.a.Cut('posttrig','(HLT_AK8PFJet60==1) || (HLT_AK8PFJet80==1) || (HLT_PFHT1050==1) || (HLT_AK8PFHT800_TrimMass50==1) || (HLT_AK8PFJet420_TrimMass30==1) || (HLT_AK8PFJet320==1) || (HLT_AK8PFJet450==1) || (HLT_AK8PFJet550==1) || (HLT_AK8PFJet500==1) || (HLT_AK8PFJet400_TrimMass30==1) || (HLT_AK8PFHT750_TrimMass50==1) || (HLT_PFHT500_PFMET100_PFMHT100_IDTight==1) || (HLT_DoublePhoton70==1) || (HLT_DoublePhoton85==1)')

    hists.Add('preTagNumerator',selection.a.DataFrame.Histo2D(('preTagNumerator','',16,25,825,30,25,3025),'Smass_trig','mth_trig'))
    hists.Add('preTagNumeratorZoomed', selection.a.DataFrame.Histo2D(('preTagNumeratorZoomed','',8,25,425,12,625,1825),'Smass_trig','mth_trig'))
    hists.Add('preTagNumeratorHT',selection.a.DataFrame.Histo1D(('preTagNumeratorHT','',30,325,3025),'HT'))
#    hists.Draw("colz")
    histNumHT = hists['preTagNumeratorHT']
    hists.Add('preTagNumeratorTpt',selection.a.DataFrame.Histo1D(('preTagNumeratorTpt','',30,325,3025),'pt0'))
    histNumTpt = hists['preTagNumeratorTpt']
    hists.Add('preTagNumeratorApt',selection.a.DataFrame.Histo1D(('preTagNumeratorApt','',30,25,3025),'Apt0'))
    histNumApt = hists['preTagNumeratorApt']

    # make efficiencies
    h_efficiency = ROOT.TGraphAsymmErrors()
#    h_efficiency.Divide(hists['preTagNumeratorHT'],hists['preTagDenominatorHT'])
    h_efficiency.Divide(histNumHT,histDenHT,"cl=0.68 b(1,1) mode")

    out = ROOT.TFile.Open('THtrigger1D_HT{}_{}.root'.format(HT,year), 'RECREATE')
    out.cd()
    histNumHT.Write()
    histDenHT.Write()
    histNumTpt.Write()
    histDenTpt.Write()
    histNumApt.Write()
    histDenApt.Write()
    h_efficiency.Write()
    out.Close()

#    out = ROOT.TFile.Open('THtrigger1D_HT{}_{}.root'.format(HT,year), 'RECREATE')
#    out.cd()
#    h_efficiency.Write()
#    out.Close()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--HT', type=str, dest='HT',
                        action='store', default='0',
                         help='Value of HT to cut on')
    parser.add_argument('--recycle', dest='recycle',
                        action='store_true', default=False,
                        help='Recycle existing files and just plot.')
    args = parser.parse_args()
    start = time.time()
    CompileCpp('TTmodules.cc')
    if not args.recycle:
# DP EDIT only do 16
#        for y in ['16','17','17B','18']:
        for y in ['18']:
            MakeEfficiency(y, args.HT)
#DP EDIT -- only left 16 below...
    files = {
        '18': ROOT.TFile.Open('THtrigger1D_HT{}_18.root'.format(args.HT))
#        '17': ROOT.TFile.Open('THtrigger1D_HT{}_17.root'.format(args.HT)),
#        '18': ROOT.TFile.Open('THtrigger1D_HT{}_18.root'.format(args.HT)),
#	'17B': ROOT.TFile.Open('THtrigger1D_HT{}_17B.root'.format(args.HT)),
#	'17All': ROOT.TFile.Open('THtrigger1D_HT{}_17All.root'.format(args.HT))
    }

#DP EDIT
#    hists = {hname.GetName():[files[y].Get(hname.GetName()) for y in ['16','17','18']] for hname in files['16'].GetListOfKeys() if '_hist' in hname.GetName()}
    hists = {hname.GetName():[files[y].Get(hname.GetName()) for y in ['18']] for hname in files['18'].GetListOfKeys() if '_hist' in hname.GetName()}
#    colors = [ROOT.kBlack, ROOT.kGreen+1, ROOT.kOrange-3]
#DP EDIT
#    legendNames = ['2016','2017','2018']
    legendNames = ['2018']
#    for hname in hists.keys():
#        c = ROOT.TCanvas('c','c',2000,700)
#        c.Divide(3,1)
#        for i,h in enumerate(hists[hname]):
#            c.cd(i+1)
#            ROOT.gPad.SetLeftMargin(0.13)
#            ROOT.gPad.SetRightMargin(0.16)
#            h.GetZaxis().SetTitleOffset(1.7)
#            h.SetLineColor(colors[i])
#            h.SetTitle(legendNames[i])
#            h.Draw('colz')
#
#        c.Print('plots/Trigger2D_{}_HT{}.pdf'.format(hname, args.HT),'pdf')

    print ('%s sec'%(time.time()-start))
