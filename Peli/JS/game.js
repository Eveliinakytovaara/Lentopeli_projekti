'use strict';

async function continentSelection(playerData) {

    let container = document.getElementById('game');
    container.innerHTML = "";
    let youareat = document.createElement('p');
    youareat.classList.add('sijainti');

    let ul = document.createElement('ul');
    ul.classList.add('maanosat')

    const continents_visited = await FetchFromDatabase(`/getcontinentsvisited/${sessionStorage.getItem('playerid')}`);
    youareat.innerHTML = `Hellow <b>${playerData.player.name}</b>! <br>You are currently at <b>${playerData.airport.name}, ${playerData.country}</b><br>`;
    youareat.innerHTML += `You have visited the following continents: <br><b>`;
    for (let key in continents_visited) {
        youareat.innerHTML += continents_visited[key].name + ', '
    }
    youareat.innerHTML += `</b><br>Choose a continent to fly to next...`;

    let i = 0;
    for (let key in playerData.continent) {
        if (i > 0 && playerData.continent[key].name != "") {

            let li = document.createElement('li');
            let a = document.createElement('a');

            a.innerHTML += playerData.continent[key].name
            a.addEventListener('click', function () {
                airportSelection(playerData, playerData.continent[key].code, playerData.continent[key].name);
            })

            ul.appendChild(li);
            li.appendChild(a);
        }
        i++;
    }
    container.appendChild(youareat);
    container.appendChild(ul);
}

async function airportSelection(playerdata, continent_code, continent_name) {

    let container = document.getElementById('game');
    container.innerHTML = "";
    let ul = document.createElement('ul');

    let text = document.createElement('p');
    text.innerHTML = `Oh, you want to fly to ${continent_name}!<br>Here are some flights that I could find:`;

    const randAirport = await FetchFromDatabase(`/randairport/5/${continent_code}`);

    for (let key in randAirport) {

        let li = document.createElement('li');
        let a = document.createElement('a');

        let temp = [];
        temp.push(randAirport[key].name);
        temp.push(randAirport[key].country_name);
        // TODO: weather
        const distance = await FetchFromDatabase(`/getdistance/${playerdata.airport.ident}/${randAirport[key].ident}`);
        temp.push(distance.distance);
        temp.push(distance.plane);
        // TODO: planes
        for (let x = 0; x < temp.length; x++) {
            a.innerHTML += temp[x] + '<br>';
        }

        a.addEventListener('click', async function () {
            makeFlight(playerdata.player.location, randAirport[key].ident);
        })

        ul.appendChild(li);
        li.appendChild(a);
    }

    container.appendChild(text);
    container.appendChild(ul);
}


async function makeFlight(current_airport, new_airport) {
    //TODO: calculate consumption properly
    const flight = await FetchFromDatabase(`/make_flight/${current_airport}/${new_airport}`);
    await AlterDatabase(`/updateplayer/${sessionStorage.getItem('playerid')}
    /${flight.co2_consumed}/${flight.distance}/${flight.plane}/${flight.continent}/${new_airport}`);

    const continents_visited = await FetchFromDatabase(`/getcontinentsvisited/${sessionStorage.getItem('playerid')}`);

    if (Object.keys(continents_visited).length >= 7) {
        endGame();
    }
    else {
        const playerdata = await getPlayerCurrentInfo();
        continentSelection(playerdata);
    }
}

async function endGame() {
    let container = document.getElementById('game');
    container.innerHTML = 'winner winner, chicken dinner!'
    AlterDatabase(`/endgame/${sessionStorage.getItem('playerid')}`);
    const playerdata = await FetchFromDatabase('/getplayer/' + sessionStorage.getItem('playerid'));
    for(let key in playerdata){
        container.innerHTML += '<br>' + playerdata[key];
    }
}

// relevant info:
// airport, country, continent, continents visited
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

window.onload = async function () {

    if (sessionStorage.getItem('playerid')) {
        let currentData = await getPlayerCurrentInfo();
        await continentSelection(currentData);
    }
    else {
        console.log('no player');
    }
}