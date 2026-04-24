import ROOT
f = ROOT.TFile.Open('rootfiles/THselection_mvaID_HT850_ttbar-gJets.root','read')
# get the histos
h1 = f.Get("MtpvMs_TvsQCD_mvaID_SR_pass__nominal")
#h2 = f.Get("MtpvMs_TvsQCD_mvaID_SR_fail__nominal")
h3 = f.Get("MtpvMs_TvsQCD_mvaID_CR_pass__nominal")
h4 = f.Get("MtpvMs_TvsQCD_mvaID_CR_fail__nominal")
h1.SetTitle("ttbar-gJets: 2t2a")
h3.SetTitle("ttbar-gJets: 2t1a")
h4.SetTitle("ttbar-gJets: 2t0a") 
h11 = f.Get("MtpvMs_TvsQCD_mvaID_SR1_pass__nominal")
h13 = f.Get("MtpvMs_TvsQCD_mvaID_CR1_pass__nominal")
h14 = f.Get("MtpvMs_TvsQCD_mvaID_CR1_fail__nominal")
h11.SetTitle("ttbar-gJets: 1t2a")
h13.SetTitle("ttbar-gJets: 1t1a")
h14.SetTitle("ttbar-gJets: 1t0a")

#h5 = f.Get("MtpvMs_TvsQCD_mvaID_SR_failfail__nominal")
#h6 = f.Get("MtpvMs_TvsQCD_mvaID_CR_failfail__nominal")

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(3,2)
#c.cd()
#c.Print('outputSelection.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [h1, h3, h4, h11, h13, h14]:
#    c.Clear()   # clear any previous draws from the canvas
    i = i+1
    c.cd(i)
    h.SetStats(0)
    zl=h.GetMaximum()
    print(zl)
    if (zl<1.0):
       h.SetMaximum(1.0)
       print('1.0')
    if (i>0):
       h.Draw("colz")  # draw the histo with colz
#    c.Print("outputSelection.pdf")  # save it to the pdf
#c.Clear()   # clear any previous draws from the canvas
#h5.SetStats(0)
#h5.SetMaximum(3.00)
#h5.Draw("colz")  # draw the histo with colz
c.Print("outputSelectionttgJets_AR.pdf")  # save it to the pdf
#c.Print("outputSelection.pdf]")  # finished, close the multipage file
