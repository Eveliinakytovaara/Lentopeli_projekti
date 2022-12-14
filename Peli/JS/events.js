'use strict';


async function flight_events() {
    const response = await FetchFromDatabase('/events/');
    let dialog = document.getElementById('drink_service');
    let div = document.getElementById('drink');
    div.innerHTML = ''
    let p = document.createElement('p');
    p.id = 'drink_question'
    let img = document.createElement('img');
    img.id = 'drink_pic'
    let ul = document.createElement('ul');
    p.innerHTML = response.question.txt;
    img.src = response.question.url;
    for (let key in response) {
        let li = document.createElement('li');
        let link = document.createElement('a');
        link.innerHTML = response[key].drink;
        link.addEventListener('click', function () {
            dialog.close();
            console.log('moi')
        })
        li.appendChild(link)
        ul.appendChild(li);
    }
    div.appendChild(img);
    div.appendChild(p);
    div.appendChild(ul);
    dialog.showModal();
}