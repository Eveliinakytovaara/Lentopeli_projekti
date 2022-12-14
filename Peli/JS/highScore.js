"use strict";

window.onload = async function () {
    let reset = document.getElementById('hs');
    reset.addEventListener('click', async function(){
        await AlterDatabase('/clear_player_data');
        window.location.replace('../HTML + CSS/Highscore.html')
    })
    createGames("/getGames/>=", true)
}