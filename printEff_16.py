import ROOT
f = ROOT.TFile.Open('THtrigger2D_HT900_16.root','read')
# get the histos
h1 = f.Get("PretagZoom_hist")
h2 = f.Get("Pretag_hist")
h3eff = f.Get("Pretag")
he=h1.Clone()
Nx = h2.GetNbinsX()
Ny = he.GetNbinsY()
for i in range(1,Nx):
 for j in range(1,Ny):
   err = f.Get("Pretag").GetAsymmetryErrorLow(i,j)
   print(err)

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(2,2)
#c.cd()
#c.Print('output.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

# loop over the histos u want to draw
i=0
for h in [h1, h2,h4]:
#    c.Clear()   # clear any previous draws from the canvas
    i=i+1
    c.cd(i)
    h.Draw("colz")  # draw the histo with colz
#    c.Print("output.pdf")  # save it to the pdf
c.Print("Trig_output_16.pdf")
#c.Print("output.pdf]")  # finished, close the multipage file
