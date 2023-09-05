
tab_liga = createSection(".tab.La-liga");
var matchContainers_liga = tab_liga.querySelectorAll('.match-container');

getPLData('static/dataframes/next_fixtures_liga.csv','static/dataframes/teams_logos_liga.csv', matchContainers_liga)
