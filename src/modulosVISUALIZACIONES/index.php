<!DOCTYPE html>
<html lang="es">
<head>
<link rel="stylesheet" href="css/estilos.css"/>
</head>
<body>

<svg width="800" height="800"></svg>
<script src="js/d3.v4.js"></script>

<script type="text/javascript">
// Requiere la variable 'data', guardada en data/data.json
d3.json('data/pulse2.json', function(data) {
  console.log(data);

  var svg = d3.select("svg"),
  margin = 20,
  diameter = +svg.attr("width"),
  g = svg.append("g").attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

  svg.append('svg:defs').append('svg:marker')
    .attr('id', 'head')
    .attr('orient', 'auto')
    .attr('markerWidth', '2')
    .attr('markerHeight', '4')
    .attr('refX', '0.1')
    .attr('refY', '2')
    .append('marker:polygon').attr('points', '0,0 0,4 2,2').attr('fill', 'red');

  var color = d3.scaleLinear()
    .domain([-1, 5])
    .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
    .interpolate(d3.interpolateHcl);

  var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(2);

  data = d3.hierarchy(data)
    .sum(function(d) {
      return d.size;
    })
    .sort(function(a, b) {
      return b.value - a.value;
    });

  var focus = data,
    nodes = pack(data).descendants(),
    view;

  // Circle center
  var origin_circle = g.selectAll("circle")
    .data(nodes).enter();

  // Inner circle
  var circle = origin_circle.append("circle")
    .attr("class", function(d) {
      return d.parent ? d.children ? "node" : "node node--leaf" : "node node--data";
    })
    .style("fill", function(d) {
      return d.children ? color(d.depth) : "white";
    })
    .style("z-index", function(d) {
      return d.children ? 10 : 1;
    })
    .on("click", function(d) {
      if (focus !== d) zoom(d), d3.event.stopPropagation();
    });
  
  // Outer circle
  var circle2 = origin_circle.append("circle")
    .attr("class", "outer")
    .attr("stroke", "white")
    .attr("stroke-opacity", 0)
    .attr("fill", "none");

  // Ports (por ahora un puerto por circulo)
  var ports = origin_circle.append("rect")
    .attr("fill", "none")
    .attr("stroke", "blue");


  ////////////////////////////////////////////
  // Text for each circle
  var text = g.selectAll("text")
    .data(nodes)
    .enter().append("text")
    .attr("class", "label")
    .style("fill-opacity", function(d) {
      return d.parent === data ? 1 : 0.1;
    })
    .style("display", function(d) {
      return d.parent === data ? "inline" : "none";
    })
    .text(function(d) {
      return d.data.name;
    });

  var node = g.selectAll("circle,text");

  svg
    .style("background", color(-1))
    .on("click", function() {
      zoom(data);
    });

  zoomTo([data.x, data.y, data.r * 2 + margin]);
  var activeNode = data;

  function zoom(d) {
    var focus0 = focus;
    focus = d;
    activeNode = d;
    var transition = d3.transition()
      .duration(d3.event.altKey ? 7500 : 750)
      .tween("zoom", function(d) {
        var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
        return function(t) {
          zoomTo(i(t));
        };
      });

    transition.selectAll("text")
      .filter(function(d) {
        return d.parent === focus || this.style.display === "inline";
      })
      .style("fill-opacity", function(d) {
        return d.parent === focus ? 1 : 0;
      })
      .on("start", function(d) {
        if (d.parent === focus) this.style.display = "inline";
      })
      .on("end", function(d) {
        if (d.parent !== focus) this.style.display = "none";
      });
  }

  function zoomTo(v) {
    var k = diameter / v[2];
    view = v;
    
    // Update node properties
    node.attr("transform", function(d) {
      return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")";
    });

    /*var side_square = 5;
    g.selectAll("rect")
      .attr("transform", function(d) {
        return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1] - d.r - side_square/2) * k + ")";
      })
      .attr("fill", "blue")
      .attr("width", side_square)
      .attr("height", side_square)
      .attr("opacity", 1);
    */
    // Inner circle
    circle.attr("r", function(d) {
      return d.r * k;
    });
    // Outer circle
    circle2.attr("r", function(d) {
      return d.r * k + 5;
    });

    // Action on node attributes
    if (activeNode) {
      // TODO : activar puertos de E/S (que se agranden)
      /*g.selectAll("path").remove();
      g.selectAll("path").data(activeNode.children).enter().append("svg:path")
        .attr('d', function(d) {
          // TODO: 
          var x = (d.x - v[0]) * k;
          var y = (d.y - v[1]) * k;
          var fX = (activeNode.x - v[0]) * k;
          var fY = (activeNode.y - activeNode.r - v[1]) * k;
          return 'M ' + fX + ' ' + -fY + ' Q ' + (parseInt(fX) + 20) + ' ' + y / 2 + ' ' + x + ' ' + y
        })
        .attr("style", function(d) {
          return "stroke:#4169E1;stroke-width:4;fill:none;";
        }).attr('marker-end', 'url(#head)');*/
    }
  }
});
</script>
</body>
</html>