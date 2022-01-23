from re import T
import ROOT


def setUpHistrogram(Name,XTitle,YTitle,LineColor,ttree,branch,Nbins,min,max,LineWidth=2,Title='',HistName='',cond="",intHis="hist"):
	if HistName=='':
		ttree.Draw(branch+">>"+intHis+"("+str(Nbins)+","+str(min)+","+str(max)+")",cond)
		Name = ROOT.gDirectory.Get(intHis).Clone()
	else:
		Name = ROOT.TH1F(HistName,HistName,Nbins,min,max)
	Name.SetLineColor(LineColor)
	Name.SetLineWidth(LineWidth)
	Name.SetTitle(Title)
	Name.GetXaxis().SetTitle(XTitle)
	Name.GetYaxis().SetTitle(YTitle)
	return Name


def setUpCanvas(Name):
	Name = ROOT.TCanvas(Name,Name)
	Name.SetTopMargin(0.1)
	Name.SetFrameLineWidth(1)
	#HiggsMass.SetBottomMargin(0.27)
	Name.SetRightMargin(0.15)
	Name.SetBottomMargin(0.08)
	#Name.SetGrid()
	return Name



def setUpLegend():
	legend = ROOT.TLegend(0.65, 0.87, 0.75, 0.77, "", "brNDC") # Understand the numbers - that is the second pair 
	legend.SetFillStyle(1001)
	legend.SetLineWidth(0)
	legend.SetLineStyle(1)
	legend.SetFillColor(0)
	legend.SetBorderSize(0)
	legend.SetTextSize(0.03)
	return legend


def setUpCmsLatex(year):
	cmsLatex = ROOT.TLatex()
	cmsLatex.SetTextSize(0.06)
	cmsLatex.SetNDC(True)
	cmsLatex.SetTextFont(61)
	cmsLatex.SetTextAlign(11)
	#cmsLatex.DrawLatex(0.1,0.92,"CMS")
	cmsLatex.DrawLatex(0.1,0.91,"CMS")
	cmsLatex.SetTextFont(52)
	#cmsLatex.DrawLatex(0.1+0.08,0.95,"Preliminary")
	cmsLatex.DrawLatex(0.12+0.08,0.91,"Preliminary")
	if year==2016:
		lumiText = '16.81 fb^{-1}, 13 TeV'
	cmsLatex.SetTextFont(42)
	cmsLatex.SetTextSize(0.045)
	cmsLatex.DrawLatex(0.55,0.91,lumiText)
	return cmsLatex