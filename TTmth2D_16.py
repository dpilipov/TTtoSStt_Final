import sys, time, ROOT
from collections import OrderedDict

from TIMBER.Analyzer import HistGroup
from TIMBER.Tools.Common import CompileCpp
#DP EDIT
#from THClass import THClass
from TTClassREF_0 import TTClassREF_0

def MakePlot(year, HT=0):
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
    fName = 'dijet_nano/StoAA1000x100_16_snapshot.txt'
#        fName = 'dijet_nano/SingleMuonData_{}_snapshot.txt'.format(year)
#DP EDIT
#    selection = TTClassSIG(fName,year if 'B' not in year else '17',1,1)
    selection = TTClassREF_0(fName,year,1,1)
    print(selection.year)
    selection.OpenForSelection('None')

    # cut on HT to improve efficiency
    before = selection.a.DataFrame.Count()
    selection.a.Cut('HT_cut', 'HT > {}'.format(HT))
    after = selection.a.DataFrame.Count()
    print(after)

    c = ROOT.TCanvas('c','c')
    graph = ROOT.TGraph(1000, ROOT.array('d',mth_trig), ROOT.array('d', mthsig_trig))
    graph.Draw("AP")
    c.Print('mth2d.pdf')

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
            MakePlot(y, args.HT)
#    c = ROOT.TCanvas('c','c')
#    graph = ROOT.TGraph(len(mth), ROOT.array('d', mth), ROOT.array('d', mthsig))
#    graph.Draw("AP")
#    c.Print('mth2d.pdf')
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

        c.Print('plots/Tmth2D_{}_HT{}.pdf'.format(hname, args.HT),'pdf')

    print ('%s sec'%(time.time()-start))
