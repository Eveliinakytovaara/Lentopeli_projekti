'use strict';

let thing = document.getElementById('clickMe');

thing.addEventListener('click',
    async function() {
        makeAFetch();
    });

function errorInSearch(message)
{
    console.log(message);
}

async function makeAFetch() {
    try {
        const response = await fetch('http://127.0.0.1:3000/Kok/joo');
        if (response.ok) {
            console.log('osui');
            const data = await response.json();
            console.log(data);
        }
        else {
            errorInSearch('Error in fetch request');
            console.log('ei osu');
        }
    }
    catch (error) {
        errorInSearch('Error in connection: ' + error);
    }
}
