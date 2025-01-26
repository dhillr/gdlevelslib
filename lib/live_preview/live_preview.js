/**
    * @name LivePreview 
**/

window.ctx = document.getElementById('canvas').getContext('2d');
ctx.canvas.width = window.outerWidth;
ctx.canvas.height = window.outerHeight;
const MAX_FPS = 120;
let frames = 0;
let time = Date.now();
let FPS = 0;
let width = window.outerWidth;
let height = window.outerHeight;
let images = [];
let frameCount = 0;
images.push(new Image());
images[0].src = "assets/textures/1.png";

fetch("assets/level/level.json")
.then(response => response.json())
.then(data => levelParse(data));

let level = [];

function levelParse(data) {
    for (let l of data) {
        level.push([l.id, l.x, l.y, l.dir]);
    }
}

function rect(x, y, w, h) {
    ctx.beginPath();
    ctx.rect(x, y, w, h);
    ctx.closePath();
    ctx.fill();
}

function image(img, x, y, w, h) {
    ctx.drawImage(img, x, y, w, h);
}

function text(txt, x, y) {
    ctx.font = "30px Minecraft";
    ctx.fillText(txt, x, y);
}

function drawLevel() {
    for (let i = 0; i < level.length; i++) {
        ctx.fillStyle = "black";
        image(images[level[i][0]-1], level[i][1]*1.85, -1.85*level[i][2]+450, 56, 56);
    }
}

function draw() {
    ctx.fillStyle = "lightblue";
    rect(0, 0, width, height);
    // image(images[0], Math.sin(0.02*frameCount)*50, frameCount, 100, 100);
    drawLevel();
    ctx.fillStyle = "black";
    text("FPS: "+FPS, 10, height-100);
}

setInterval(() => {
    draw();
    frameCount++;
    frames++;
    if (time > 999 && time < 1000000000) {
        FPS = frames;
        time = Date.now();
        frames = 0;
    }
    time = Date.now() - time;
}, 1000 / MAX_FPS);