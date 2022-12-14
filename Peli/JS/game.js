'use strict';

function resetContainer(){
    let container = document.getElementById('game');
    container.innerHTML = "";
    return container;
}

//Fetches continent choices based on player data and then displays them
async function continentSelection(playerData) {

    //Get reference to container and clear old html
    let container = resetContainer();

    //Create ul for continent choices
    let ul = document.createElement('ul');
    ul.classList.add('maanosat')

    //Create p with flavour text
    let youareat = document.createElement('p');
    youareat.classList.add('sijainti');
    youareat.innerHTML = `Hellow <b>${playerData.player.name}</b>! <br>You are currently at <b>${playerData.airport.name}, ${playerData.country}</b><br>`;
    youareat.innerHTML += `You have visited the following continents: <br><b>`;

    //Fetch continents visited based on players id
    const continents_visited = await FetchFromDatabase(`/getcontinentsvisited/${sessionStorage.getItem('playerid')}`);
    //Display continents that the player has visited
    for (let key in continents_visited) {
        youareat.innerHTML += continents_visited[key].name + ', '
    }
    youareat.innerHTML += `</b><br>Choose a continent to fly to next...`;

    //Display continent choices ignoring first entry or null values
    //TODO: edit python so you don't need to ignore first entry
    let i = 0;
    for (let key in playerData.continent) {
        if (i > 0 && playerData.continent[key].name != "") {

            //Create li and a
            let li = document.createElement('li');
            let a = document.createElement('a');

            //Add function to 'a' so that it opens airports from this continent
            a.innerHTML += playerData.continent[key].name
            a.addEventListener('click', function () {
                airportSelection(playerData.airport.ident, playerData.continent[key].code, playerData.continent[key].name);
            })

            //Append to ul
            ul.appendChild(li);
            li.appendChild(a);
        }
        i++;
    }
    //Append flavour text and ul
    container.appendChild(youareat);
    container.appendChild(ul);
}


//Fetch airport data based on continent and display it in html
async function airportSelection(playerIdent, continent_code, continent_name) {

    //Get container reference and clear old html
    let container = resetContainer();

    //Create ul and p
    let ul = document.createElement('ul');
    let text = document.createElement('p');
    text.innerHTML = `Oh, you want to fly to ${continent_name}!<br>Here are some flights that I could find:`;
    container.appendChild(text);

    //Fetch random airports
    const randAirport = await FetchFromDatabase(`/randairport/5/${continent_code}`);

    //loop through airports
    for (let key in randAirport) {

        //Create list element and link
        let li = document.createElement('li');
        let a = document.createElement('a');

        //Fetch distance from current location and this airport
        const distance = await FetchFromDatabase(`/getdistance/${playerIdent}/${randAirport[key].ident}`);

        //loop thorugh temporary list and display inner html
        //TODO: temporary list in unnessesary. Innerhtml can be added straight
        a.innerHTML+= 'Airport name: ' + randAirport[key].name + '<br>';
        a.innerHTML+= 'Country: ' + randAirport[key].country_name + '<br>';
        a.innerHTML+= 'Distance: ' + distance.distance + ' km' + '<br>';
        a.innerHTML+= 'Plane size: ' + distance.plane +'<br>';
        a.innerHTML+= 'Weather: ' + randAirport[key].weather[0] + '<br>';

        setMarker([randAirport[key].lat, randAirport[key].lon], a.innerHTML, "hue-rotate(120deg)");

        //add function to 'a' so that it makes the flight when clicked 
        a.addEventListener('click', async function () {
            makeFlight(playerIdent, randAirport[key].ident, randAirport[key].weather[0]);
        })

        //Append to ul
        ul.appendChild(li);
        li.appendChild(a);
    }

    //Append to container
    container.appendChild(ul);
    zoomToMarkers();
}

//Calculates nessesary flight info, updates player data and then opens continent choices
async function makeFlight(current_airport, new_airport, weather) {

    //Fetch flight details
    //TODO: calculate consumption properly
    const flight = await FetchFromDatabase(`/make_flight/${current_airport}/${new_airport}/${weather}`);

    //Animate flying and on finnish show next location
    animateFlying(flight);
    resetContainer();
}

async function finnishFlight(flight){

    flight_events();
    //Update player data
    //TODO: make a flight and updating can be done in python
    await AlterDatabase(`/updateplayer/${sessionStorage.getItem('playerid')}
    /${flight.co2_consumed}/${flight.distance}/${flight.plane}/${flight.continent}/${flight.ending_location.ident}`);

    //Get continents visited
    const continents_visited = await FetchFromDatabase(`/getcontinentsvisited/${sessionStorage.getItem('playerid')}`);
    //Check if the game is completed
    if (Object.keys(continents_visited).length >= 7) {
        endGame();
    }
    else {
        const playerdata = await getPlayerCurrentInfo();
        continentSelection(playerdata);
    }
}

//Display end game stats
//TODO: make pretty
async function endGame() {
    let container = document.getElementById('game');
    container.innerHTML = 'winner winner, chicken dinner!'
    let p = document.createElement('p');
    p.classList.add('endscreen');
    AlterDatabase(`/endgame/${sessionStorage.getItem('playerid')}`);
    const playerdata = await FetchFromDatabase('/endgame/' + sessionStorage.getItem('playerid'));
    p.innerHTML += 'name: ' + playerdata.name + '<br>';
    p.innerHTML += 'co2 consumed: ' + playerdata.co2_consumed + '<br>';
    p.innerHTML += 'travel distance: ' + playerdata.travel_distance + ' km' + '<br>';
    p.innerHTML += 'current location: ' + playerdata.last_location + '<br>';
    p.innerHTML += 'starting location: ' + playerdata.starting_location + '<br>';
    p.innerHTML += 'number of flights: ' + playerdata.number_of_flights + '<br>';
    p.innerHTML += 'small planes used: ' + playerdata.s_planes_used + '<br>';
    p.innerHTML += 'medium planes used: ' + playerdata.m_planes_used + '<br>';
    p.innerHTML += 'large planes used: ' + playerdata.l_planes_used + '<br>';
    p.innerHTML += 'thank you for travelling with us!' + '<br>';
    container.appendChild(p);
}


//Get players current info and return it
async function getPlayerCurrentInfo() {

    const playerdata = await FetchFromDatabase('/getplayer/' + sessionStorage.getItem('playerid'));
    const airportdata = await FetchFromDatabase('/getairport/' + playerdata.location);
    const countryname = await FetchFromDatabase('/getcountry/' + playerdata.location);
    const continentdata = await FetchFromDatabase('/getcontinent/' + playerdata.location);

    const currentData = {
        'player': playerdata,
        'airport': airportdata,
        'country': countryname.name,
        'continent': continentdata
    };
    return currentData;
}

//Start game with sessionstorage playerid 
window.onload = async function () {

    if (sessionStorage.getItem('playerid')) {
        let currentData = await getPlayerCurrentInfo();
        await continentSelection(currentData);
        setStartingPoint([currentData.airport.lat, currentData.airport.lon]);
    }
    else {
        console.log('no player');
    }
}