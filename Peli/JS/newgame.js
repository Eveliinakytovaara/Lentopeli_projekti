'use strict';

var buttons=[];

//Fetch random airports to start with and display them in html
async function createAirportChoices(count) {
    //Fetch
    let airports = await FetchFromDatabase('/getfirstairports/' + count);

    //Get container
    let container = document.getElementById('airports');
    //Loop through airports
    for (let i = 0; i < count; i++) {

        //Create li
        let listelement = document.createElement('li');
        listelement.classList.add('airportwindow');

        //Create a
        let linkbutton = document.createElement('a');
        linkbutton.classList.add('linkki');
        buttons.push(linkbutton)

        //On click, save this airport in session storage
        linkbutton.addEventListener('click', async function(){
            sessionStorage.setItem('airport', airports[i].ident);
            for(let x = 0; x < buttons.length; x++){
                buttons[x].style.background='#1D3240'
            }
            linkbutton.style.background ='#658DA6'
        })

        //Display airport name and country
        linkbutton.innerHTML += airports[i].name;
        linkbutton.innerHTML += ', '
        linkbutton.innerHTML += airports[i].country_name;

        //Append
        container.appendChild(listelement);
        listelement.appendChild(linkbutton);
    }
}

//On start load and display airports. Also clear possible old session storage
window.onload = function() {
    sessionStorage.removeItem('airport');
    sessionStorage.removeItem('playerid');
    createAirportChoices(5);

}
//Sumbit button starts the game
document.getElementById('newgamemenu').addEventListener('submit', async function (evt) {
    evt.preventDefault();

    //Get input value (player name)
    let sname = document.querySelector('input[name=screen_name]').value;
    //Get session storage airport (starting airport)
    let starting_airport = sessionStorage.getItem('airport')

    //If both name and starting airport exists, create a player and start game in game.hmtl
    if (sname != "" && starting_airport) {
        const playerData = await FetchFromDatabase('/newplayer/' + sname + '/' + starting_airport);
        sessionStorage.setItem('playerid', playerData.id);
        window.location.replace('../HTML + CSS/game.html');
    }
    else {
        //TODO: update html so that it shows why the game didn't start (name or starting airport missing)

    }
});
