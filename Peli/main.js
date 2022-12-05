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

async function makeAFetchForData(search) {
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

async function getRandomAirports(count) {
    let airports = await makeAFetchForData('/randairport/' + count);
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
            localStorage.currentairport = airports[i].ident
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

window.onload = function() {
    createAirportChoices(5);
}
document.getElementById('newgamemenu').addEventListener('submit', async function (evt) {
    evt.preventDefault();
    let sname = document.querySelector('input[name=screen_name]').value;
    let starting_airport = localStorage.currentairport;
    if (sname != "" && starting_airport != "") {
        const playerData = await makeAFetchForData('/newplayer/' + sname + '/' + starting_airport);
        localStorage.currentplayer = playerData.id
    }
    else {
        console.log('no name');
    }
});