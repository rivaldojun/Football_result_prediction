const links = [...document.querySelectorAll('.navbar .link')];
const tabs = [...document.querySelectorAll('.tabs .tab')];
const headerImg = document.querySelector('.header img');
const headerTitle = document.querySelector('.header h1');
const root = document.documentElement;

const colors = {
    'Premier League': '242, 5, 92',
    'La Liga': '68, 88, 155',
    'Bundesliga': '210,	6, 22',
    'Serie A': '18, 87, 64',
    'Ligue 1': '238, 153, 0'
  };

  let activeHeaderImg = headerImg.src;
  let activeHeaderTitle = headerTitle.textContent;

//   localStorage.setItem('activeHeaderImg',  headerImg.src);
//   localStorage.setItem('activeHeaderTitle', headerTitle.textContent);
  

links.forEach((link, idx) =>{
    link.addEventListener('click', () =>{
        selectTab(idx);
        const imgName = link.getAttribute('data-img');
        const title = link.getAttribute('data-title');

        headerImg.src = `static/img/${imgName}`;
        headerTitle.textContent = title; 
        changeHeaderBackground(colors[title]);

        // Store the active header image and title
        activeHeaderImg = headerImg.src;
        activeHeaderTitle = headerTitle.textContent;

        localStorage.setItem('activeHeaderImg', activeHeaderImg);
        localStorage.setItem('activeHeaderTitle', activeHeaderTitle);
        
        
    })

});


if (window.location.href.indexOf("result") > -1){
    headerImg.src = localStorage.getItem('activeHeaderImg');
	headerTitle.textContent = localStorage.getItem('activeHeaderTitle');
	changeHeaderBackground(colors[localStorage.getItem('activeHeaderTitle')]);
}else{
    headerImg.src = activeHeaderImg;
    headerTitle.textContent = activeHeaderTitle;
    changeHeaderBackground(colors[activeHeaderTitle]);
}



function selectTab(idx){
    links.forEach((link, index) =>{
        if(index === idx){
            link.classList.add('active');
            tabs[index].classList.remove('hide');
        }else{
            link.classList.remove('active');
            tabs[index].classList.add('hide');
        }
    })
}

function changeHeaderBackground(color) {
    root.style.setProperty('--main-bg-color', color);
}


const states = document.querySelectorAll('.state');

states.forEach((state) => {
  state.addEventListener('click', () => {
    const matchContainer = state.closest('.match-container');
    const homeTeam = matchContainer.querySelector('.home-team .name').textContent;
    const awayTeam = matchContainer.querySelector('.away-team .name').textContent;
    const homeTeamLogo = matchContainer.querySelector('img[alt="Manchester City"]').src;
    const awayTeamLogo = matchContainer.querySelector('img[alt="Arsenal"]').src;
    const league = headerTitle.textContent;
    

    fetch('/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}&league=${encodeURIComponent(league)}&homelogo=${encodeURIComponent(homeTeamLogo)}&awaylogo=${encodeURIComponent(awayTeamLogo)}`
      })
      
      .then(response => {response.text(),window.location.href='/result'})
      .then(result => { });
      
  });
});
