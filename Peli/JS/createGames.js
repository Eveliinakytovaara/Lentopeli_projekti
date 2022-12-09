'use strict';


async function createGames(url) {
    let highscores = await FetchFromDatabase(url);
    let container = document.getElementById('score');
    console.log(highscores);
    for (let i = 0; i < Object.keys(highscores).length; i++) {
        let single_entry = document.createElement('div');
        let txt = document.createElement('p');


        txt.innerHTML += 'player: ' +  highscores[i].name + ' <br>';
        txt.innerHTML += 'co2 consumed: ' + highscores[i].co2_consumed + ' <br>';
        txt.innerHTML += 'travel distance: ' + highscores[i].travel_distance + ' <br>';
        txt.innerHTML += 'number of flights: ' + highscores[i].number_of_flights + ' <br>';
        txt.innerHTML += 'small planes used: ' + highscores[i].s_planes_used + ' <br>';
        txt.innerHTML += 'medium planes used: ' + highscores[i].m_planes_used + ' <br>';
        txt.innerHTML += 'large planes used: ' + highscores[i].l_planes_used + ' <br>';

        single_entry.appendChild(txt);
        container.appendChild(single_entry);
    }
}