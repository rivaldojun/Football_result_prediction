tab_serieA= createSection(".tab.Serie-A ");

var matchContainers_serieA = tab_serieA.querySelectorAll('.match-container');

getPLData('static/dataframes/next_fixtures_serieA.csv','static/dataframes/teams_logos_serieA.csv', matchContainers_serieA)