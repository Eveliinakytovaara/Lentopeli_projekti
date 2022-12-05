'use strict';

var hostAddress = 'http://127.0.0.1:5000';

function errorInSearch(type) {
    throw new Error(type)
}

//Makes a fetch for data
async function makeAFetch(search) {
    try {
        await fetch(hostAddress + search);
    }
    catch (error) {
        errorInSearch('Error in connection: ' + error);
    }
}

async function makeAFetchForData(search){
    try {
        const response = await fetch(hostAddress + search);
        if (response.ok) {
            const data = await response.json();
            return data;
        }
        else {
            errorInSearch('Error in fetch request');
            return null;
        }
    }
    catch (error) {
        errorInSearch('Error in connection: ' + error);
        return null;
    }
}

async function getRandomAirports(count, playerData){
    let airports = {}
    for(i = 0; i < count; i++){
    }
}

async function createAirportChoices(count, playerdata){
    let airports = getRandomAirports(count, playerdata)

    const container = document.getElementById('airports');
    for(i = 0; i < count; i++){
        let listelement = document.createElement('li');
        
        let linkbutton = document.createElement('a');

    }
}


// document.getElementById('continent').addEventListener('click', async function () {
//     makeAFetch('/getcontinent/efhk');
// })

// document.getElementById('airport').addEventListener('click', async function () {
//     makeAFetch('/getairport/efhk');
// })

// document.getElementById('random').addEventListener('click', async function () {
//     makeAFetch('/randairport/5');
// })

// document.getElementById('country').addEventListener('click', async function () {
//     makeAFetch('/getcountry/efhk');
// })


document.getElementById('newgamemenu').addEventListener('submit', async function (evt) {
    evt.preventDefault();
    let sname = document.querySelector('input[name=screen_name]').value;
    if (sname != "" && starting_airport != "") {
        const playerData = makeAFetchForData('/newplayer/' + sname + '/' + starting_airport);
        let starting_airport = 'efhk';
        localStorage.currentplayer = playerData.id
    }
    else{
        console.log('no name');
    }
});

document.getElementById('continuegame')


