
function connect() {

    let game_id = '{{game_id}}'
    let team_name = '{{team_name}}'
    let url = `ws://${window.location.host}/ws/waiting/${game_id}/`

    const waitSocket = new WebSocket(url)

    waitSocket.onopen = function open() {
        console.log("WebSockets connection created.");
        waitSocket.send(JSON.stringify({
            "event": "START",
            "team_name": team_name
        }))
    };

    waitSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    waitSocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        console.log('Data:', data)

        console.log('WTF?')
        let message = data['message']
        let team_name = data['team_name']
        let event = data['event']

        if(event === 'NEWTEAM'){
            alert("test");
            let teams_div = document.getElementById('teams')

            teams_div.insertAdjacentHTML('beforeend', `<div> 
                <p>${team_name}</p>
            </div>`)
        }
    }
}

