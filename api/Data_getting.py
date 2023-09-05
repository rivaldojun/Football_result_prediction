from Data_scrapping import *


premleague=read_data_path("premierleague","E0")
ligue1=read_data_path("ligue1","F1")
laliga=read_data_path("laliga","SP1")
bundesliga=read_data_path("bundesligua","D1")
serieA=read_data_path("serieA","I1")



teamPL=get_team(premleague)
teamL1=get_team(ligue1)
teamLL=get_team(laliga)
teamBL=get_team(bundesliga)
teamSA=get_team(serieA)


dataprepocessing(premleague,teamPL,"PL")
dataprepocessing(ligue1,teamL1,"L1")
dataprepocessing(laliga,teamLL,"LL")
dataprepocessing(bundesliga,teamBL,"BL")
dataprepocessing(serieA,teamSA,"SA")