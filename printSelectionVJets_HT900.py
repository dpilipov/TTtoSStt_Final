import ROOT
f = ROOT.TFile.Open('/uscms/home/dpilipov/nobackup/TwoDAlphabet/CMSSW_10_6_14/src/rootfiles/THselection_mvaID_HT900_VJets.root','read')
# get the histos
h1 = f.Get("MtpvMs_TvsQCD_mvaID_SR_pass__nominal")
h2 = f.Get("MtpvMs_TvsQCD_mvaID_CR_pass__nominal")
h3 = f.Get("MtpvMs_TvsQCD_mvaID_CR_fail__nominal")
h4 = f.Get("MtpvMs_TvsQCD_mvaID_SR1_pass__nominal")
h5 = f.Get("MtpvMs_TvsQCD_mvaID_CR1_pass__nominal")
h6 = f.Get("MtpvMs_TvsQCD_mvaID_CR1_fail__nominal")
h1.SetTitle("VJets 2t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h2.SetTitle("VJets 2t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h3.SetTitle("VJets 2t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h4.SetTitle("VJets 1t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h5.SetTitle("VJets 1t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h6.SetTitle("VJets 1t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(3,2)
#c.cd()
#c.Print('outputSelection.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [h1, h2, h3, h4, h5, h6]:
#    c.Clear()   # clear any previous draws from the canvas
    i = i+1
    c.cd(i)
    h.SetStats(0)
    sum1=h.GetSum()
    print(sum1)
    zl=h.GetMaximum()
    print(zl)
    if (zl<1.0):
       h.SetMaximum(1.0)
    h.Draw("colz")  # draw the histo with colz
#    c.Print("outputSelection.pdf")  # save it to the pdf
#c.Clear()   # clear any previous draws from the canvas
#h5.SetStats(0)
#h5.SetMaximum(3.00)
#h5.Draw("colz")  # draw the histo with colz
c.Print("outputSelectionVJets_HT900.pdf")  # save it to the pdf
#c.Print("outputSelection.pdf]")  # finished, close the multipage file
