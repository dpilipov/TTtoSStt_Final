import ROOT
f = ROOT.TFile.Open('rootfiles/THselection_HT0_StoAA1000x100_16APV.root','read')
f1 = ROOT.TFile.Open('rootfiles/THselection_HT0_StoAA1000x200_16APV.root','read')
f2  = ROOT.TFile.Open('rootfiles/THselection_HT0_StoAA1000x300_16APV.root','read')
# get the histos
h1 = f.Get("MtpvMs_TvsQCD_cutBased_SR_pass__nominal")
#h2 = f.Get("MtpvMs_TvsQCD_cutBased_SR_fail__nominal")
h3 = f.Get("MtpvMs_TvsQCD_cutBased_CR_pass__nominal")
h4 = f.Get("MtpvMs_TvsQCD_cutBased_CR_fail__nominal")
h1.SetTitle("1000-100: SR pass")
h3.SetTitle("1000-100: CR pass")
h4.SetTitle("1000-100: CR fail") 
h11 = f1.Get("MtpvMs_TvsQCD_cutBased_SR_pass__nominal")
h13 = f1.Get("MtpvMs_TvsQCD_cutBased_CR_pass__nominal")
h14 = f1.Get("MtpvMs_TvsQCD_cutBased_CR_fail__nominal")
h11.SetTitle("1000-200: SR pass")
h13.SetTitle("1000-200: CR pass")
h14.SetTitle("1000-200: CR fail")
h21 = f2.Get("MtpvMs_TvsQCD_cutBased_SR_pass__nominal")
h23 = f2.Get("MtpvMs_TvsQCD_cutBased_CR_pass__nominal")
h24 = f2.Get("MtpvMs_TvsQCD_cutBased_CR_fail__nominal")
h21.SetTitle("1000-300: SR pass")
h23.SetTitle("1000-300: CR pass")
h24.SetTitle("1000-300: CR fail")

#h5 = f.Get("MtpvMs_TvsQCD_cutBased_SR_failfail__nominal")
#h6 = f.Get("MtpvMs_TvsQCD_cutBased_CR_failfail__nominal")

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(3,3)
#c.cd()
#c.Print('outputSelection.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [h1, h3, h4, h11, h13, h14, h21, h23, h24]:
#    c.Clear()   # clear any previous draws from the canvas
    i = i+1
    c.cd(i)
    h.SetStats(0)
    zl=h.GetMaximum()
    print(zl)
    if (zl<1.0):
       h.SetMaximum(1.0)
       print('1.0')
    h.Draw("colz")  # draw the histo with colz
#    c.Print("outputSelection.pdf")  # save it to the pdf
#c.Clear()   # clear any previous draws from the canvas
#h5.SetStats(0)
#h5.SetMaximum(3.00)
#h5.Draw("colz")  # draw the histo with colz
c.Print("outputSelection1000M_16APV.pdf")  # save it to the pdf
#c.Print("outputSelection.pdf]")  # finished, close the multipage file
