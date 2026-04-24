import ROOT
f = ROOT.TFile.Open('out_Eff_2016.root','read')
# get the histos
h1 = f.Get("Eff_2016")
#h3 = f.Get("histo3")
f1 = ROOT.TFile.Open('out_Eff_2016APV.root','read')
f2 = ROOT.TFile.Open('out_Eff_2017.root','read')
f3 = ROOT.TFile.Open('out_Eff_2018.root','read')
h2 = f1.Get("Eff_2016APV")
h3 = f2.Get("Eff_2017")
h4 = f3.Get("Eff_2018")

# make a canvas
c = ROOT.TCanvas('c','c')
c.Divide(2,2)
#c.cd()
#c.Print('outputSWAN.pdf[')  # this tells the canvas to open file for multi-page printing
#c.Clear()

i=0
# loop over the histos u want to draw
for h in [h1,h2,h3,h4]:
#    c.Clear()   # clear any previous draws from the canvas
    i=i+1
    c.cd(i)
    h.SetStats(0)
    h.SetMaximum(1.0)
    h.SetMinimum(0.0)
    h.Draw("colz")  # draw the histo with colz
#    c.Print("outputSWAN.pdf")  # save it to the pdf
c.Print("outputSWAN.pdf")
#c.Print("outputSWAN.pdf]")  # finished, close the multipage file
