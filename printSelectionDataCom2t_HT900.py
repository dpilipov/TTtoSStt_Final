import ROOT
f = ROOT.TFile.Open('/uscms/home/dpilipov/nobackup/TwoDAlphabet/CMSSW_10_6_14/src/rootfiles/THselection_mvaID_HT900_Data.root','read')
f1 = ROOT.TFile.Open('/uscms/home/dpilipov/nobackup/TwoDAlphabet/CMSSW_10_6_14/src/rootfiles/THselection_mvaID_HT900_ttbar.root','read')
f2 = ROOT.TFile.Open('/uscms/home/dpilipov/nobackup/TwoDAlphabet/CMSSW_10_6_14/src/rootfiles/THselection_mvaID_HT900_VJets.root','read')

# get the histos
h1 = f.Get("MtpvMs_TvsQCD_mvaID_SR_pass__nominal")
h2 = f.Get("MtpvMs_TvsQCD_mvaID_CR_pass__nominal")
h3 = f.Get("MtpvMs_TvsQCD_mvaID_CR_fail__nominal")
h4 = f.Get("MtpvMs_TvsQCD_mvaID_SR1_pass__nominal")
h5 = f.Get("MtpvMs_TvsQCD_mvaID_CR1_pass__nominal")
h6 = f.Get("MtpvMs_TvsQCD_mvaID_CR1_fail__nominal")
h11 = f1.Get("MtpvMs_TvsQCD_mvaID_SR_pass__nominal")
h12 = f1.Get("MtpvMs_TvsQCD_mvaID_CR_pass__nominal")
h13 = f1.Get("MtpvMs_TvsQCD_mvaID_CR_fail__nominal")
h14 = f1.Get("MtpvMs_TvsQCD_mvaID_SR1_pass__nominal")
h15 = f1.Get("MtpvMs_TvsQCD_mvaID_CR1_pass__nominal")
h16 = f1.Get("MtpvMs_TvsQCD_mvaID_CR1_fail__nominal")
h21 = f2.Get("MtpvMs_TvsQCD_mvaID_SR_pass__nominal")
h22 = f2.Get("MtpvMs_TvsQCD_mvaID_CR_pass__nominal")
h23 = f2.Get("MtpvMs_TvsQCD_mvaID_CR_fail__nominal")
h24 = f2.Get("MtpvMs_TvsQCD_mvaID_SR1_pass__nominal")
h25 = f2.Get("MtpvMs_TvsQCD_mvaID_CR1_pass__nominal")
h26 = f2.Get("MtpvMs_TvsQCD_mvaID_CR1_fail__nominal")

h1.SetTitle("Data 2t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h2.SetTitle("Data 2t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h3.SetTitle("Data 2t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h4.SetTitle("Data 1t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h5.SetTitle("Data 1t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h6.SetTitle("Data 1t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")

h11.SetTitle("t#bar{t} 2t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h12.SetTitle("t#bar{t} 2t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h13.SetTitle("t#bar{t} 2t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h14.SetTitle("t#bar{t} 1t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h15.SetTitle("t#bar{t} 1t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h16.SetTitle("t#bar{t} 1t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")

h21.SetTitle("VJets 2t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h22.SetTitle("VJets 2t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h23.SetTitle("VJets 2t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h24.SetTitle("VJets 1t-2a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h25.SetTitle("VJets 1t-1a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
h26.SetTitle("VJets 1t-0a; M_{\gamma\gamma}; M_{t\gamma\gamma}")
# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(3,3)
#c.cd()
#c.Print('outputSelection.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [h1, h2, h3, h11, h12, h13,h21, h22, h23]:
#h4, h5, h6]:
#    c.Clear()   # clear any previous draws from the canvas
    i = i+1
    c.cd(i)
    h.SetStats(0)
    zl=h.GetMaximum()
    print(zl)
    if (zl<1.0):
       h.SetMaximum(1.0)
    if (i>1):
       h.Draw("colz")  # draw the histo with colz
#    c.Print("outputSelection.pdf")  # save it to the pdf
#c.Clear()   # clear any previous draws from the canvas
#h5.SetStats(0)
#h5.SetMaximum(3.00)
#h5.Draw("colz")  # draw the histo with colz
c.Print("outputSelectionDataComp2t_HT900.pdf")  # save it to the pdf
#c.Print("outputSelection.pdf]")  # finished, close the multipage file
