import ROOT
f = ROOT.TFile.Open('rootfiles/THselection_HT0_Data.root','read')
# get the histos
h1 = f.Get("MtpvMs_TvsQCD_cutBased_SR_pass__nominal")
#h2 = f.Get("MtpvMs_TvsQCD_cutBased_SR_fail__nominal")
h3 = f.Get("MtpvMs_TvsQCD_cutBased_CR_pass__nominal")
h4 = f.Get("MtpvMs_TvsQCD_cutBased_CR_fail__nominal")
h1.SetTitle("Data: 2t2a")
h3.SetTitle("Data: 2t1a")
h4.SetTitle("Data: 2t0a") 
h11 = f.Get("MtpvMs_TvsQCD_cutBased_SR1_pass__nominal")
h13 = f.Get("MtpvMs_TvsQCD_cutBased_CR1_pass__nominal")
h14 = f.Get("MtpvMs_TvsQCD_cutBased_CR1_fail__nominal")
h11.SetTitle("ttbar MC: 1t2a")
h13.SetTitle("ttbar MC: 1t1a")
h14.SetTitle("ttbar MC: 1t0a")
hd11 = h11.Clone()
hd11.Divide(h14)
hd11.SetTitle("Data Ratio: 1t2a/1t0a")
hd13 = h13.Clone()
hd13.Divide(h14)
hd13.SetTitle("Data Ratio: 1t1a/1t0a")
hd3 = h3.Clone()
hd3.Divide(h4)
hd3.SetTitle("Data Ratio: 2t1a/2t0a")

#h5 = f.Get("MtpvMs_TvsQCD_cutBased_SR_failfail__nominal")
#h6 = f.Get("MtpvMs_TvsQCD_cutBased_CR_failfail__nominal")

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(3,1)
#c.cd()
#c.Print('outputSelection.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [hd11,hd13,hd3]:
#    c.Clear()   # clear any previous draws from the canvas
    i = i+1
    c.cd(i)
    h.SetStats(0)
    zl=h.GetMaximum()
    print(zl)
    h.Draw("colz")  # draw the histo with colz
#    c.Print("outputSelection.pdf")  # save it to the pdf
#c.Clear()   # clear any previous draws from the canvas
#h5.SetStats(0)
#h5.SetMaximum(3.00)
#h5.Draw("colz")  # draw the histo with colz
c.Print("outputRatioDataM.pdf")  # save it to the pdf
#c.Print("outputSelection.pdf]")  # finished, close the multipage file
