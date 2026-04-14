const grid = document.getElementById("grid");
const scoreText = document.getElementById("score");

function draw(data){
    grid.innerHTML = "";

    scoreText.innerText =
        "Player: " + data.player_score +
        " | AI: " + data.agent_score +
        " | Moves: " + data.moves;

    for(let i=0;i<6;i++){
        for(let j=0;j<6;j++){
            let c = document.createElement("div");
            c.classList.add("cell");

            if(data.goal[0]==i && data.goal[1]==j)
                c.style.background="green";

            if(data.agent[0]==i && data.agent[1]==j)
                c.style.background="red";

            if(data.player[0]==i && data.player[1]==j)
                c.style.background="blue";

            grid.appendChild(c);
        }
    }
}

function move(d){
    fetch(`http://127.0.0.1:5000/step/${d}`)
    .then(r=>r.json())
    .then(draw);
}

function reset(){
    fetch("http://127.0.0.1:5000/reset")
    .then(r=>r.json())
    .then(draw);
}

function setMode(m){
    fetch(`http://127.0.0.1:5000/mode/${m}`)
    .then(()=> reset()); // 🔥 reset on mode change
}

reset();