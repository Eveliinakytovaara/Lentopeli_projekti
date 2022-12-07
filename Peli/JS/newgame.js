'use strict';

async function getRandomAirports(count) {
    let airports = await FetchFromDatabase('/randairport/' + count);
    return airports;
}

async function createAirportChoices(count) {
    let airports = await getRandomAirports(count);

    let container = document.getElementById('airports');
    for (let i = 0; i < count; i++) {

        let listelement = document.createElement('li');
        listelement.classList.add('airportwindow')

        let linkbutton = document.createElement('a');
        linkbutton.addEventListener('click', async function(){
            sessionStorage.setItem('airport', airports[i].ident)
            console.log(localStorage.currentairport);
        })
        
        let text = document.createElement('p');
        text.innerHTML += airports[i].name;
        text.innerHTML += ', '
        text.innerHTML += airports[i].country_name;

        container.appendChild(listelement);
        listelement.appendChild(linkbutton);
        linkbutton.appendChild(text);
    }
}

window.onload = function() {
    sessionStorage.removeItem('airport');
    sessionStorage.removeItem('playerid');
    createAirportChoices(5);

}
document.getElementById('newgamemenu').addEventListener('submit', async function (evt) {
    evt.preventDefault();

    let sname = document.querySelector('input[name=screen_name]').value;
    let starting_airport = sessionStorage.getItem('airport')

    if (sname != "" && starting_airport) {
        const playerData = await FetchFromDatabase('/newplayer/' + sname + '/' + starting_airport);
        sessionStorage.setItem('playerid', playerData.id);
        window.location.replace('../HTML + CSS/game.html');
    }
    else {
        console.log('no name');
    }
});