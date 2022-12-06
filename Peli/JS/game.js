'use strict';

async function selectContinent(data) {

    let container = document.getElementById('game');
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

            ul.appendChild(li);
            li.appendChild(txt);
            li.appendChild(a);
        }

    }

    container.appendChild(youareat);
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

    console.log(currentData);
    return currentData;
}



window.onload = async function () {

    if (sessionStorage.getItem('playerid')) {
        let currentData = await getPlayerCurrentInfo();
        await selectContinent(currentData);
    }
    else {
        console.log('no player');
    }
}