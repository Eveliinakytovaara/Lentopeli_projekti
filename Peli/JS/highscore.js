'use strict';


async function createHighscores() {
    let highscores = await FetchFromDatabase('/gethighscores');
    let container = document.getElementById('score');
    for (let i = 0; i < Object.keys(highscores).length; i++) {
        let single_entry = document.createElement('div');
        let txt = document.createElement('p');

        txt.innerHTML += highscores[i].name + ' <br>';
        txt.innerHTML += highscores[i].co2_consumed + ' <br>';
        txt.innerHTML += highscores[i].travel_distance + ' <br>';
        txt.innerHTML += highscores[i].number_of_flights + ' <br>';
        txt.innerHTML += highscores[i].s_planes_used + ' <br>';
        txt.innerHTML += highscores[i].m_planes_used + ' <br>';
        txt.innerHTML += highscores[i].l_planes_used + ' <br>';

        container.appendChild(single_entry);
        single_entry.appendChild(txt);
        console.log(highscores[i]);
    }
}

window.onload = async function () {
    createHighscores();
}