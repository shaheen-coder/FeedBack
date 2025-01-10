var tl = new TimelineMax(),
split404  = new SplitText(".textB", {type:"chars"}),
splitPage = new SplitText(".textA", {type:"chars"}),
splitBack = new SplitText(".textC", {type:"chars"});

split404.split({type:"chars"});
splitPage.split({type:"chars"});
splitBack.split({type:"chars"});

tl.set(".hide", {opacity: 0})
.set(".box", {scale: 0,  transformOrigin: "50% 50%"})
.set(".hide.big-white-circle", {scale: 0,  transformOrigin: "50% 50%"})
.set(".hide.bottom-triangles", {scale: 0, rotation: 720,  transformOrigin: "50% 50%"})

.to(".box", 2, {scale: 1, transformOrigin: "50% 50%", ease: Elastic.easeOut.config(1, 0.5)})

.staggerFrom(split404.chars, 1, {opacity: 0, scaleX: 0, ease: Power4.easeOut}, 0.05, "-=1")
.staggerTo(split404.chars, 1, {opacity: 1, scaleX: 1, ease: Power4.easeOut}, 0.05, "-=1")

.staggerFrom(splitPage.chars, 1, {opacity: 0, scaleX: 0, ease: Power4.easeOut}, 0.05, "-=1")
.staggerTo(splitPage.chars, 1, {opacity: 1, scaleX: 1, ease: Power4.easeOut}, 0.05, "-=1")

.staggerFrom(splitBack.chars, 1, {opacity: 0, scaleX: 0, ease: Power4.easeOut}, 0.05, "-=1.5")
.staggerTo(splitBack.chars, 1, {opacity: 1, scaleX: 1, ease: Power4.easeOut}, 0.05, "-=1.5")
.to(".hide.big-white-circle", 2, {scale: 1, opacity: 1, ease: Elastic.easeOut.config(1, 0.3)}, "-=1.45")
.to(".hide.spin-circles", 2, {opacity: 1}, "-=1.45")
.to(".hide.tri-dots", 1, {opacity: 1}, "-=1.5")
.to(".hide.bottom-triangles", 2, {opacity: 1, scale: 1, rotation: 0}, "-=1.5")
.to(".start-tri", 1, {morphSVG:".end-tri"}, "-=1.5")

// .timeScale();
// .seek();

// create repeating timeline for spinning circles
var tlSpin = new TimelineMax({repeat: -1});
tlSpin.set('.hide.spin-circles', {rotation: 0, transformOrigin: "50% 50%"})
.to('.hide.spin-circles', 3.5, {rotation: 360, ease:Linear.easeNone})