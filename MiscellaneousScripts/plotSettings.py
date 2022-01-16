from re import T
import ROOT


def setUpHistrogram(Name,XTitle,YTitle,LineColor,ttree,branch,Nbins,min,max,LineWidth=2,Title='',HistName=''):
	if HistName=='':
		ttree.Draw(branch+">>"+branch+"("+str(Nbins)+","+str(min)+","+str(max)+")")
		Name = ROOT.gDirectory.Get(branch).Clone()
	else:
		Name = ROOT.TH1F(Name,Name,Nbins,min,max)
	Name.SetLineColor(LineColor)
	Name.SetLineWidth(LineWidth)
	Name.SetTitle(Title)
	Name.GetXaxis().SetTitle(XTitle)
	Name.GetYaxis().SetTitle(YTitle)
	return Name
