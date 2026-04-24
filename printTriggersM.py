import ROOT
f = ROOT.TFile.Open('THtrigger2D_HT0_16.root','read')
# get the histos
h1 = f.Get("PretagZoom_hist")
h2 = f.Get("Pretag_hist")
#h3 = f.Get("histo3")

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(2,1)
#c.cd()
#c.Print('output.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [h1, h2]:
#    c.Clear()   # clear any previous draws from the canvas
    i=i+1
    c.cd(i)
    h.Draw("colz")  # draw the histo with colz
#    c.Print("output.pdf")  # save it to the pdf
c.Print("outputM.pdf")
#c.Print("output.pdf]")  # finished, close the multipage file
