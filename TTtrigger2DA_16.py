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
        year (str) : 16
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
    fName = 'dijet_nano/SingleMuonData_16_snapshot.txt'
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
    hists.Add('preTagDenominator',selection.a.DataFrame.Histo2D(('preTagDenominator','',16,25,825,30,25,3025),'Smass_trig','mth_trig'))
    hists.Add('preTagDenominatorZoomed', selection.a.DataFrame.Histo2D(('preTagDenominatorZoomed','',8,25,425,12,625,1825),'Smass_trig','mth_trig'))
    hists.Add('preTagDenominatorHT',selection.a.DataFrame.Histo1D(('preTagDenominatorHT','',0,25,3025),'HT'))
#    hists.Add('preTagDenominatorTpt',selection.a.DataFrame.Histo1D(('preTagDenominatorTpt','',0,25,3025),'Dijet_pt[0]')
#    hists.Add('preTagDenominatorApt',selection.a.DataFrame.Histo1D(('preTagDenominatorApt','',0,25,3025),'Diphoton_pt[0]')
    selection.ApplyTrigs()
#    hists.Add('preTagNumerator',selection.a.DataFrame.Histo2D(('preTagNumerator','',16,25,825,24,625,3025),'Smass_trig','mth_trig'))
    hists.Add('preTagNumerator',selection.a.DataFrame.Histo2D(('preTagNumerator','',16,25,825,30,25,3025),'Smass_trig','mth_trig'))
    hists.Add('preTagNumeratorZoomed', selection.a.DataFrame.Histo2D(('preTagNumeratorZoomed','',8,25,425,12,625,1825),'Smass_trig','mth_trig'))
    hists.Add('preTagNumeratorHT',selection.a.DataFrame.Histo1D(('preTagNumeratorHT','',0,25,3025),'HT'))
#    hists.Add('preTagNumeratorTpt',selection.a.DataFrame.Histo1D(('preTagNumeratorTpt','',0,25,3025),'Dijet_pt[0]'))
#    hists.Add('preTagNumeratorApt',selection.a.DataFrame.Histo1D(('preTagNumeratorApt','',0,25,3025),'Diphoton_pt[0]'))
#    hists.Draw("colz")

    # make efficiencies
    effs = {
        "Pretag": ROOT.TEfficiency(hists['preTagNumerator'], hists['preTagDenominator']),
	"PretagZoom": ROOT.TEfficiency(hists['preTagNumeratorZoomed'], hists['preTagDenominatorZoomed']),
    }

    h_efficiency = ROOT.TGraphAsymmErrors()
    h_efficiency.Divide(hists['preTagNumeratorHT'],hists['preTagDenominatorHT'])
#    h_efficiency = ROOT.TGraphAsymmErrors()
#    h_efficiency.Divide(hists['preTagNumeratorTpt'],hists['preTagDenominatorTpt'])
#    h_efficiency = ROOT.TGraphAsymmErrors()
#    h_efficiency.Divide(hists['preTagNumeratorApt'],hists['preTagDenominatorApt'])

    out = ROOT.TFile.Open('THtrigger2D_HT{}_{}.root'.format(HT,year), 'RECREATE')
    out.cd()
    for name,eff in effs.items():
        g = eff.CreateHistogram()
        g.SetName(name+'_hist')
        g.SetTitle(name)
        g.GetXaxis().SetTitle('m_{\gamma \gamma} (GeV)')
        g.GetYaxis().SetTitle('m_{j \gamma \gamma} (GeV)')
        g.GetZaxis().SetTitle('Efficiency')
        g.SetMinimum(0.6)
        g.SetMaximum(1.0)
        f = ROOT.TF2("eff_func","1-[0]/10*exp(-1.3*y/1000)*exp(0.07*x/50)",25,825,25,3025)
#        f = ROOT.TF2("eff_func","1-[0]/10*exp([1]*y/1000)*exp(-[2]*x/50)",25,825,25,3025)
#        f = ROOT.TF2("eff_func","1-exp(-[0]+[1]*y/1000)*exp([2]*x/50)",25,825,25,3025)
#        f = ROOT.TF2("eff_func","1-[0]/10*exp([1]*y/1000)*exp([2]*x/50)",25,825,625,3025)
        #f = ROOT.TF2("eff_func","1-[0]*exp([1]*y/1000)*exp([2]*x/200)",60,260,800,2600)
        f.SetParameter(0,0.01)
        f.SetParameter(1,-0.01)
        f.SetParameter(2,0.01)
        g.Fit(f)
        g.Write()
        eff.SetName(name)
        eff.Write()
    out.Close()

#    out = ROOT.TFile.Open('THtrigger1D_HT{}_{}.root'.format(HT,year), 'RECREATE')
#    out.cd()
#    h_efficiency.Write()
#    out.Close()
#    c1 =  ROOT.TCanvas('c','c')
#    c1.cd()
#    c1.Clear()
#    h.Draw("AP")
#    c1.Print('THtrigger1D_HT0_16.pdf')

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
        for y in ['16']:
            MakeEfficiency(y, args.HT)
#DP EDIT -- only left 16 below...
    files = {
        '16': ROOT.TFile.Open('THtrigger2D_HT{}_16.root'.format(args.HT))
#        '17': ROOT.TFile.Open('THtrigger2D_HT{}_17.root'.format(args.HT)),
#        '18': ROOT.TFile.Open('THtrigger2D_HT{}_18.root'.format(args.HT)),
#	'17B': ROOT.TFile.Open('THtrigger2D_HT{}_17B.root'.format(args.HT)),
#	'17All': ROOT.TFile.Open('THtrigger2D_HT{}_17All.root'.format(args.HT))
    }

#DP EDIT
#    hists = {hname.GetName():[files[y].Get(hname.GetName()) for y in ['16','17','18']] for hname in files['16'].GetListOfKeys() if '_hist' in hname.GetName()}
    hists = {hname.GetName():[files[y].Get(hname.GetName()) for y in ['16']] for hname in files['16'].GetListOfKeys() if '_hist' in hname.GetName()}
    colors = [ROOT.kBlack, ROOT.kGreen+1, ROOT.kOrange-3]
#DP EDIT
#    legendNames = ['2016','2017','2018']
    legendNames = ['2016']
    for hname in hists.keys():
        c = ROOT.TCanvas('c','c',2000,700)
        c.Divide(3,1)
        for i,h in enumerate(hists[hname]):
            c.cd(i+1)
            ROOT.gPad.SetLeftMargin(0.13)
            ROOT.gPad.SetRightMargin(0.16)
            h.GetZaxis().SetTitleOffset(1.7)
            h.SetLineColor(colors[i])
            h.SetTitle(legendNames[i])
            h.Draw('colz')

        c.Print('plots/Trigger2D_{}_HT{}.pdf'.format(hname, args.HT),'pdf')

    print ('%s sec'%(time.time()-start))
