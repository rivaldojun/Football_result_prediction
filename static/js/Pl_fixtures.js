// https://v3.football.api-sports.io/fixtures?live=all
// https://v3.football.api-sports.io/fixtures/rounds?season=2021&league=60 39  104e39294fda5cdc3a51f77c0624221a 

// var matchContainers = document.querySelectorAll('.match-container');
// var homeTeamLogo = matchContainers[1].querySelector('img[alt="Manchester City"]');
// var awayTeamLogo = matchContainers[1].querySelector('img[alt="Arsenal"]');
// var homeTeamName = matchContainers[1].querySelector('.home-team .name');
// var awayTeamName = matchContainers[1].querySelector('.away-team .name');
// var matchday = matchContainers[1].querySelector('h4');



// function getPLData(){

//     fetch("https://v3.football.api-sports.io/fixtures?league=39&season=2022",{
//         "method" : "GET",
//         "headers" :{
//             "x-rapidapi-host" : "v3.football.api-sports.io",
//             "x-rapidapi-key" : "104e39294fda5cdc3a51f77c0624221a"
//         }
//     })
//     .then(response => response.json().then(data => {

//         var matcheslist = data['response'];
//         //var fixture = matcheslist[0]['fixture'];
//         //var goals = matcheslist[0]['goals'];
//         var teams = matcheslist[0]['teams'];

//         matchday.textContent = matcheslist[0]['league']['round'].replace(/Regular Season - (\d+)/, 'Journée $1');
//         homeTeamLogo.setAttribute('src', teams['home']['logo']);

//         console.log(matcheslist)

//     }))
//     .catch(err => {
//         console.log(err);
//     });


// }

// getPLData();
tab_Pl= createSection(".tab.Premier-league");
//var tabPremierLeague = document.querySelector('.tab.Premier-league');
var matchContainers = tab_Pl.querySelectorAll('.match-container');
async function getPLData(link_data, link_logo, matchContainers){
    const response = await fetch(link_data);
    const data = await response.text();
    const parsedData = Papa.parse(data, { header: true }).data;
    const selectedMatches = selectRandomMatches(parsedData, 7);
    
    selectedMatches.forEach(async (match, index) => {
        const container = matchContainers[index];
        const homeTeamLogo = container.querySelector('img[alt="Manchester City"]');
        const awayTeamLogo = container.querySelector('img[alt="Arsenal"]');
        const homeTeamName = container.querySelector('.home-team .name');
        const awayTeamName = container.querySelector('.away-team .name');
        const matchday = container.querySelector('h4');
        const homeTeam = match['Home'];
        const awayTeam = match['Away'];
        const week = parseInt(match['Wk']);
        matchday.textContent = "Journée " + week;
        homeTeamName.textContent = homeTeam;
        awayTeamName.textContent = awayTeam;

        const [homeLogo, awayLogo] = await findlogo(homeTeam, awayTeam, link_logo);

        homeTeamLogo.setAttribute('src', homeLogo);
        awayTeamLogo.setAttribute('src', awayLogo);
    });
}

async function findlogo(homeTeam, awayTeam, link2){
    const response = await fetch(link2);
    const data = await response.text();
    const parsedLogos = Papa.parse(data, { header: true }).data;
    let homeLogo, awayLogo;
    for (let i = 0; i < parsedLogos.length; i++) {
        if (parsedLogos[i].team === homeTeam) {
          homeLogo = parsedLogos[i].logo;
        }
        if (parsedLogos[i].team === awayTeam) {
          awayLogo = parsedLogos[i].logo;
        }
    }
    

    return [homeLogo, awayLogo];
}

function selectRandomMatches(parsedData, count) {
    const shuffled = parsedData.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

getPLData('static/dataframes/next_fixtures.csv','static/dataframes/teams_logos.csv', matchContainers);
