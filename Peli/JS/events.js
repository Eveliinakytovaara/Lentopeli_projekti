'use strict';

var hostAddress = 'http://127.0.0.1:3000';

function errorInSearch(type) {
    throw new Error(type)
}

//Makes a fetch for data
async function AlterDatabase(search) {
    try {
        await fetch(hostAddress + search);
    }
    catch (error) {
        errorInSearch('Error in connection: ' + error);
    }
}

async function FetchFromDatabase(search) {
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

async function flight_events() {
    const response = await FetchFromDatabase('/events/');
    let dialog = document.getElementById('drink_service');
    let p = document.getElementById('drink_question');
    let img = document.getElementById('drink_pic');
    let ul = document.getElementById('drink_choices');
    p.innerHTML = response.question.text;
    img.src = '../Kuvat/flight-attendant-cart-drink-service-never-order.jpg';
    for (let key in response) {
          let li = document.createElement('li');
              li.innerHTML = response[key].drink
        ul.appendChild(li);
    }
    dialog.appendChild(p);
    dialog.appendChild(img);
    dialog.appendChild(ul);
    dialog.showModal();
}