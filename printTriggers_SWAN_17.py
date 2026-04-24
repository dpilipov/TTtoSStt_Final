import ROOT
f = ROOT.TFile.Open('out_Eff_2017.root','read')
# get the histos
h1 = f.Get("Eff_2017")
#h3 = f.Get("histo3")

# make a canvas
c = ROOT.TCanvas('c','c')
c.cd()
c.Print('outputSWAN_17.pdf[')  # this tells the canvas to open file for multi-page printing
c.Clear()

# loop over the histos u want to draw
for h in [h1]:
    c.Clear()   # clear any previous draws from the canvas
    h.SetStats(0)
    h.Draw("colz")  # draw the histo with colz
    c.Print("outputSWAN_17.pdf")  # save it to the pdf

c.Print("outputSWAN_17.pdf]")  # finished, close the multipage file
