var canvas = document.getElementById('rain');
var ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var rainDrops = [];

for (var i = 0; i < 50; i++) {
    rainDrops.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        l: Math.random() * 1,
        xs: -4 + Math.random() * 4 + 2,
        ys: Math.random() * 10 + 10
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'rgba(0,0,0,0.5)';
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';

    for (var i = 0; i < rainDrops.length; i++) {
        var r = rainDrops[i];
        ctx.beginPath();
        ctx.moveTo(r.x, r.y);
        ctx.lineTo(r.x + r.l * r.xs, r.y + r.l * r.ys);
        ctx.stroke();
    }
    move();
}

function move() {
    for (var i = 0; i < rainDrops.length; i++) {
        var r = rainDrops[i];
        r.x += r.xs;
        r.y += r.ys;
        if (r.x > canvas.width || r.y > canvas.height) {
            r.x = Math.random() * canvas.width;
            r.y = -20;
        }
    }
}

setInterval(draw, 30);

window.addEventListener('resize', function() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
