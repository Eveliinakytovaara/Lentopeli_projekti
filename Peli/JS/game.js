'use strict';

async function continentSelection(data) {

    let container = document.getElementById('game');
    container.innerHTML = "";
    let youareat = document.createElement('p');
    let ul = document.createElement('ul');

    youareat.innerHTML = `Hellow ${data.player.name}!<br>You are currently at ${data.airport.name}, ${data.country}`;
    youareat.innerHTML += `<br>Choose which continent to fly next...`;

    let i = 0;
    let arraydata = []
    for (let key in data.continent) {
        if (i > 0) {
            let temp = [data.continent[key].code, data.continent[key].name];
            arraydata.push(temp);
        }
        i++;
    }

    for (let i = 0; i < arraydata.length; i++) {

        if (arraydata[i][1] != "") {
            let li = document.createElement('li');
            let txt = document.createElement('p');
            let a = document.createElement('a');

            txt.innerHTML = arraydata[i][1];
            a.addEventListener('click', function () {
                airportSelection(data, arraydata[i]);
            })

            ul.appendChild(li);
            li.appendChild(a);
            a.appendChild(txt);
        }

    }

    container.appendChild(youareat);
    container.appendChild(ul);
}

async function airportSelection(playerdata, continent) {

    let container = document.getElementById('game');
    container.innerHTML = "";
    let ul = document.createElement('ul');

    let text = document.createElement('p');
    text.innerHTML = `Oh, you want to fly to ${continent[1]}!<br>Here are some flights that I could find:`;

    const randAirport = await FetchFromDatabase(`/randairport/5/${continent[0]}`);

    let arraydata = [];
    for (let key in randAirport) {
        let temp = [];
        temp.push(randAirport[key].name)
        temp.push(randAirport[key].country_name)
        // TODO: weather
        const distance = await FetchFromDatabase(`/getdistance/${playerdata.airport.ident}/${randAirport[key].ident}`)
        temp.push(distance.distance)
        // TODO: planes
        arraydata.push(temp);
    }

    for (let i = 0; i < arraydata.length; i++) {

        let li = document.createElement('li');
        let txt = document.createElement('p');
        let a = document.createElement('a');

        for (let x = 0; x < arraydata[i].length; x++) {
            txt.innerHTML += arraydata[i][x] + '<br>';
        }

        ul.appendChild(li);
        li.appendChild(a);
        a.appendChild(txt);
    }
    container.appendChild(text);
    container.appendChild(ul);
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