import ROOT
f = ROOT.TFile.Open('rootfiles/THselection_HT0_VJets_16.root','read')
# get the histos
h1 = f.Get("MtpvMs_TvsQCD_cutBased_SR_pass__nominal")
h2 = f.Get("MtpvMs_TvsQCD_cutBased_SR_fail__nominal")
h3 = f.Get("MtpvMs_TvsQCD_cutBased_CR_pass__nominal")
h4 = f.Get("MtpvMs_TvsQCD_cutBased_CR_fail__nominal")
h5 = f.Get("MtpvMs_TvsQCD_cutBased_SR_failfail__nominal")
h6 = f.Get("MtpvMs_TvsQCD_cutBased_CR_failfail__nominal")

# make a canvas
c = ROOT.TCanvas('c','c')
c.cd()
c.Print('outputSelectionVJets.pdf[')  # this tells the canvas to open file for multi-page printing
c.Clear()

# loop over the histos u want to draw
for h in [h1, h2, h5, h3, h4, h6]:
    c.Clear()   # clear any previous draws from the canvas
    h.SetStats(0)
    zl=h.GetMaximum()
    print(zl)
#    if (zl<3.00):
#       h.SetMaximum(3.00)
#       print('3.00')
    h.Draw("colz")  # draw the histo with colz
    c.Print("outputSelectionVJets.pdf")  # save it to the pdf

#c.Clear()   # clear any previous draws from the canvas
#h5.SetStats(0)
#h5.SetMaximum(3.00)
#h5.Draw("colz")  # draw the histo with colz
#c.Print("outputSelectionVJets.pdf")  # save it to the pdf
#h4.SetStats(0)
#h4.SetMaximum(3.00)
#h4.Draw("colz")  # draw the histo with colz
#c.Print("outputSelectionVJets.pdf")  # save it to the pdf
c.Print("outputSelectionVJets.pdf]")  # finished, close the multipage file
