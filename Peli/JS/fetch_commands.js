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
