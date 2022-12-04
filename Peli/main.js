'use strict';

var hostAddress = 'http://127.0.0.1:5000';

function errorInSearch(type) {
    console.log(type);
}

//Makes a fetch for data
async function makeAFetch(search) {
    try {
        const response = await fetch(hostAddress + search);
        if (response.ok) {
            const data = await response.json();
            console.log(data);
        }
        else {
            errorInSearch('Error in fetch request');
        }
    }
    catch (error) {
        errorInSearch('Error in connection: ' + error);
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
    let starting_airport = 'efhk';
    if (sname != "" && starting_airport != "") {
        console.log(hostAddress + '/newplayer/' + sname + '/' + starting_airport);
        makeAFetch('/newplayer/' + sname + '/' + starting_airport);
    }
    else{
        console.log('no name');
    }
});