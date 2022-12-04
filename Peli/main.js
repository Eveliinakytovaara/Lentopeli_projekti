'use strict';

var hostAddress = 'http://127.0.0.1:3000';

function errorInSearch(type){
    console.log(type);
}

//Makes a fetch for data
async function makeAFetch(search) {

    let searchS = '';
    for(let i = 0; i < search.length; i++){
        searchS += search[i];
        searchS += '/';
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/' + searchS);
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

function createPlayer(screen_name, starting_airport){

    if(screen_name != '' && starting_airport != ''){
        
    }
}

