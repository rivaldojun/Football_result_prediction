tab_ligue1 = createSection(".tab.Ligue-1 ");
var matchContainers_ligue1 = tab_ligue1.querySelectorAll('.match-container');

getPLData('static/dataframes/next_fixtures_ligue1.csv','static/dataframes/teams_logos_ligue1.csv', matchContainers_ligue1)