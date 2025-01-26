/**
    * @name LivePreview
    * @description Live preview for a GeometryDashLevel.
    * @version 1.0
    
    Note the this isn't live yet, but it will be soon.
    If there are any issues with my code, feel free to create an issue on the GitHub repository.
**/

class vec2 {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

window.ctx = document.getElementById('canvas').getContext('2d');
ctx.canvas.width = window.outerWidth;
ctx.canvas.height = window.outerHeight;
const MAX_FPS = 1000;
let frames = 0;
let time = Date.now();
let FPS = 0;
let width = window.outerWidth;
let height = window.outerHeight;
let images = [];
let frameCount = 0;
let mouseDown = false;

let camera = new vec2(0, 0);

// load images
images.push(new Image());
images[0].src = "assets/textures/objects/1.png";

// fetch level.json
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
        image(images[level[i][0]-1], level[i][1]*1.85-camera.x, -1.85*level[i][2]+832-camera.y, 56, 56);
    }
}
let t = 0;
let ox, oy;
let mouseX, mouseY;

function draw() {
    ctx.fillStyle = "lightblue";
    rect(0, 0, width, height);
    drawLevel();
    ctx.fillStyle = "black";
    text("FPS: "+FPS, 10, height-100);

    window.document.body.addEventListener("mousedown", (e) => mouseDown = true);
    window.document.body.addEventListener("mouseup", (e) => mouseDown = false);


    if (mouseDown) {
        window.document.body.addEventListener("mousemove", (e) => {
            if (!mouseDown) return null;
            mouseX = e.clientX - width/2;
            mouseY = e.clientY - height/2;
            if (t < 1) {
                ox = mouseX;
                oy = mouseY;
                console.log(t);
            }
            camera.x = mouseX + ox;
            camera.y = mouseY + oy;
            t++;
        });
    } else {
        t = 0;
    }
}

setInterval(() => {
    draw();
    frameCount++;
    frames++;
    if ((time > 999 && time < 1000000000) || frames >= MAX_FPS) {
        FPS = frames;
        time = Date.now();
        frames = 0;
    }
    time = Date.now() - time;
}, 1000 / MAX_FPS);