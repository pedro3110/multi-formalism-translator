<!DOCTYPE html>
<html lang="es">
<head>
<link rel="stylesheet" href="css/estilos.css"/>
</head>
<body>

<svg width="800" height="800"></svg>
<script src="js/d3.v4.js"></script>

<script type="text/javascript">

var svg = d3.select('svg');
var originX = 200;
var originY = 200;
var innerCircleRadius = 40;
var outerCircleRadius = 60;

var table = svg.selectAll("circle").data([1,2,3,4]).enter().append("circle")
	.attr("cx", originX)
    .attr("cy", originY)
    .attr("r", innerCircleRadius)
    .attr("fill", "white")
    .attr("stroke", "black");

var outerCircle = svg.append("circle")
    .attr("cx", originX)
    .attr("cy", originY)
    .attr("r", outerCircleRadius)
    .attr("fill", "none")
    .attr("stroke", "black");

var chairOriginX = originX + ((outerCircleRadius) * Math.sin(0));
var chairOriginY = originY - ((outerCircleRadius) * Math.cos(0));

var chairWidth = 20;
var chair = svg.append("rect")
    .attr("x", chairOriginX - (chairWidth / 2))
    .attr("y", chairOriginY - (chairWidth / 2))
    .attr("width", chairWidth)
    .attr("opacity", 1)
    .attr("height", 20)
    .attr("fill", "none")
    .attr("stroke", "blue");

chair.attr("transform", "rotate(93, 200, 200)");


</script>
</body>
</html>