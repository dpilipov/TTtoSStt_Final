import ROOT
f = ROOT.TFile.Open('egammaEffi.txt_EGM2D_Pho_Loose_UL16.root','read')
# get the histos
h1 = f.Get("EGamma_SF2D")
#h3 = f.Get("histo3")

# make a canvas
c = ROOT.TCanvas('c','c')
c.cd()
c.Print('outputEGamma.pdf[')  # this tells the canvas to open file for multi-page printing
c.Clear()

# loop over the histos u want to draw
for h in [h1]:
    c.Clear()   # clear any previous draws from the canvas
    h.Draw("colz")  # draw the histo with colz
    c.Print("outputEGamma.pdf")  # save it to the pdf

c.Print("outputEGamma.pdf]")  # finished, close the multipage file
