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

function gdcoord(v) {
    return new vec2(v.x*1.85, -1.85*v.y+832);
}

function gdcoordc(v) {
    return new vec2(v.x*1.85-camera.x, -1.85*v.y+832-camera.y);
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
let bgImage = new Image()
let groundImage = new Image();
bgImage.src = "assets/textures/backgrounds/back-fade2.png";
groundImage.src = "assets/textures/grounds/floor-fade2.png";

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

function line(x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.closePath();
    ctx.stroke();
}

function line(v1, v2) {
    ctx.beginPath();
    ctx.moveTo(v1.x, v1.y);
    ctx.lineTo(v2.x, v2.y);
    ctx.closePath();
    ctx.stroke();
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

function drawGrid() {
    ctx.strokeStyle = "rgba(0,0,0,0.25)";
    for (let i = gdcoord(new vec2(-1500)).x; i < width*10; i += 30) {
        line(gdcoordc(new vec2(i,-1500)), gdcoordc(new vec2(i,height)));
    }

    for (let i = -1515; i < height; i += 30) {
        line(gdcoordc(new vec2(-1500,i)), gdcoordc(new vec2(width*10,i)));
    }
}
let t = 0;
let ox, oy, ocx, ocy;
let mouseX, mouseY;

function draw() {
    ctx.fillStyle = "#0068FF";
    for (let a = 0; a < 10; a++) {
        rect(2400*a, 0, width, height);
        image(bgImage, -0.2*camera.x+2400*a, -0.2*camera.y, 2400, 1800);
    }
    

    drawGrid();
    drawLevel();
    ctx.fillStyle = "#0048AF";
    for (let i = 0; i < 10; i++) {
        rect(gdcoord(new vec2(15,-15)).x-camera.x+i*960, gdcoord(new vec2(15,-15)).y-camera.y, 960, 240);
        image(groundImage, gdcoord(new vec2(15,-15)).x-camera.x+i*960, gdcoord(new vec2(15,-15)).y-camera.y, 960, 240);
    }

    ctx.fillStyle = "black";
    rect(gdcoord(new vec2(15,-15)).x-camera.x, gdcoord(new vec2(15,-15)).y-camera.y+240, 9600, 2400);

    ctx.fillStyle = "white";
    text("FPS: "+FPS, 10, height-100);

    window.document.body.addEventListener("mousedown", () => mouseDown = true);
    window.document.body.addEventListener("mouseup", () => mouseDown = false);


    if (mouseDown) {
        window.document.body.addEventListener("mousemove", (e) => {
            if (!mouseDown) return null;
            mouseX = -e.clientX - width/2;
            mouseY = -e.clientY - height/2;
            if (t < 1) {
                ox = mouseX;
                oy = mouseY;
                ocx = camera.x;
                ocy = camera.y;
                console.log(t);
            }
            camera.x = ocx + (mouseX - ox);
            camera.y = ocy + (mouseY - oy);
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