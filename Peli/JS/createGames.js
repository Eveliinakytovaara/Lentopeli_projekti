'use strict';



//Fetches games and displays them on the screen (both continuegame.js and highscore.js uses this function with different url)
//TODO: Make continuing games possible
async function createGames(url, isGameComplete) {
    //Fetch game data
    let games = await FetchFromDatabase(url);
    //Get reference to container
    let container = document.getElementById('score');

    //Loop through every game
    for (let i = 0; i < Object.keys(games).length; i++) {
        //Create html elements (div and p)
        let single_entry = document.createElement('div');
        let txt = document.createElement('a');

        //Add text to p
        txt.innerHTML += 'player: ' + games[i].name + ' <br>';
        txt.innerHTML += 'co2 consumed: ' + games[i].co2_consumed + ' <br>';
        txt.innerHTML += 'travel distance: ' + games[i].travel_distance + ' <br>';
        txt.innerHTML += 'number of flights: ' + games[i].number_of_flights + ' <br>';
        txt.innerHTML += 'small planes used: ' + games[i].s_planes_used + ' <br>';
        txt.innerHTML += 'medium planes used: ' + games[i].m_planes_used + ' <br>';
        txt.innerHTML += 'large planes used: ' + games[i].l_planes_used + ' <br>';

        if (isGameComplete) {
            txt.addEventListener('click', async function () {
            })
        }
        //Append div and p to container to display them
        single_entry.appendChild(txt);
        container.appendChild(single_entry);
    }
}