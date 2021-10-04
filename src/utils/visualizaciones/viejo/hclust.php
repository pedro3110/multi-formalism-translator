
<script src="d3.v4.js"></script>
<script src="jquery-1.11.2.min.js"></script>
<script src="./datasets.js" type="text/javascript"></script>

<body>
  <svg id="origin_coupled" height="1200" width="1200"></svg>
</body>

<script>

// TODO : setear bien los tamanios de los circulos, dependiendo de la cantidad de atomicos / acoplados que contenga adentro
var makeSVG = function(root_svg, dataset, init_radius) {

  var n_coupled = dataset['datasets'].length;

  if(n_coupled > 0) {
    var coupled_nodes = dataset['datasets_nodes'];
    var coupled_links = dataset['datasets_links'];

    makeGroup(root_svg+'_coupled', coupled_nodes, coupled_links, init_radius * Math.log(n_coupled), 'coupled');

    for(var i=0; i < dataset['datasets'].length; i++) {
      atomic_name = dataset['datasets'][i];
      atomic_dataset = dataset[atomic_name];

      makeSVG(atomic_name, atomic_dataset, init_radius * Math.log(n_coupled) / (n_coupled + 1));
    }

  } else {
    var nodes = dataset['nodes'];
    var n_nodes = nodes.length;
    var links = dataset['links'];
    
    //console.log(root_svg);
    makeGroup(root_svg+'_coupled', nodes, links, init_radius / n_nodes, 'atomic');
  }
}

var makeGroup = function(idSelector, data_nodes, data_links, radius, type_) {

  console.log(idSelector);
  // TODO
  var width = radius;
  var height = radius;

  // Create somewhere to put the force directed graph
  var svg = d3.select("#"+idSelector);
  //console.log(idSelector);

  var rectWidth = width / 5;
  var rectHeight = height / 5;
  var minDistance = Math.sqrt(rectWidth*rectWidth + rectHeight*rectHeight);
  var node_radius = rectWidth / 2;

  // Set up the simulation and add forces
  var simulation = d3.forceSimulation()
  	.nodes(data_nodes);

  var link_force =  d3.forceLink(data_links)
  	.id(function(d) { return d.id; })
    .distance(minDistance)
    .strength(1);

  var charge_force = d3.forceManyBody()
      .strength(-1500);

  var center_force = d3.forceCenter(width / 2, height / 2);

  simulation
      .force("charge_force", charge_force)
      .force("center_force", center_force)
      .force("links",link_force)
      .force('y', d3.forceY(height / 2).strength(0.10));


  // Add tick instructions:
  simulation.on("tick", tickActions );

  // Add encompassing group for the zoom
  var move_x = 0, move_y = 0;
  if(type_ == 'coupled') {move_x = -160; move_y = -160;}
  var g = svg.append("g")
    .attr("id", idSelector +'_child')
    .attr("transform", "translate(" + move_x + "," + move_y + ")");

  var div = g.select("body").append("div")
      .attr("class", "tooltip");

  // Arrow-heads
  g.append("defs").selectAll("marker")
        .data(['arrowhead'])
      .enter().append("marker")
        .attr("id", function(d) { return d; })
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 10)
        .attr("refY", 0)
        .attr("marker-units", "stroke-width")
        .attr("markerWidth", 0.004*radius)
        .attr("markerHeight", 0.004*radius)
        .attr("orient", "auto")
      .append("path")
        .attr("d", "M0,-5L10,0L0,5");

  // Draw lines for the links
  var link = g.append("g")
  	.attr("class", "links")
  		.selectAll("line").data(data_links)
  		  .enter()
  		.append("path")
        .attr("class", "link")
  			.attr("stroke-width", 1.5)
  			  .style("stroke", "#000")
        .attr('marker-end', "url(#arrowhead)");//linkColour

  // Draw rects and texts for the nodes
  var nodes = g.append("g")
  	.attr("class", "nodes");

  var node = nodes.selectAll("node")
  	.data(data_nodes)
  	.enter()
  		.append("g").attr("id", function(d) {return d.name + '_' + d.level;});

  node
  	.on("mouseover", function(d) {
  		d3.select(this).select("rect").style("fill", "red");
  		div.transition().duration(200);
  		div.html("asdasd")
  			.style("left", (d3.event.pageX) + "px")
  			.style("top", (d3.event.pageY - 28) + "px");
      d3.select(this).classed("fixed", d.fixed = true);
  	})
  	.on("mouseout", function(d) {
  		d3.select(this).select("rect").style("fill", rectColour);
  		div.transition().duration(500);
      d3.select(this).classed("fixed", d.fixed = true);
  	});


  var rect = node.append("circle").attr("id", function(d) {return d.name + '_' + d.level + '_circle'; })
  		.attr("cx", 0)
  		.attr("cy", 0)
  		//.attr("width", rectWidth)
  		//.attr("height", rectHeight)
  		.attr("r", node_radius)
      .attr("fill", function(d,i) {
        return d.color;
      })
      .attr("stroke", "black")
      .style("fill-opacity", function(d,i) {
        if(d.level == 'coupled') {
          return 0;
        }
        return 1;
      });

  var textName = node.append("text")
  		.text(function (d) { return d.name; })
  		.attr("y", 0)
  		.style("text-anchor", "middle")
      .style("font-size", 10)
      .attr("transform", "translate(0," + -node_radius + ")");

  /*var textOwned = node.append("text")
  		.text(function (d) { return d.id; })
  		.attr("y", 15)
  		.style("text-anchor", "middle");*/

  /*node.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")"
  });*/

  // Add drag capabilities
  var drag_handler = d3.drag()
  	.on("start", drag_start)
  	.on("drag", drag_drag)
  	.on("end", drag_end);

  drag_handler(node);

  // Add zoom capabilities
  var zoom_handler = d3.zoom()
      .on("zoom", zoom_actions);

  zoom_handler(svg);

  /** Functions **/

  function rectColour(d, i){
    var color = d3.scaleOrdinal(d3.schemeCategory10);
  	return color(i);
  }

  // Function to choose the line colour and thickness
  function linkColour(d){
  	return "black";
  }

  // Drag functions
  function drag_start(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
    d3.select(this).classed("fixed", d.fixed = true);
  }

  // Make sure you can't drag the rect outside the box
  function drag_drag(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
    d3.select(this).classed("fixed", d.fixed = true);
  }

  function drag_end(d) {
    if (!d3.event.active) simulation.alphaTarget(0);

    // TODO : comentar/descomentar para que los nodos se queden quietos despues de moverlos
    //d.fx = null;
    //d.fy = null;
    d3.select(this).classed("fixed", d.fixed = true);
  }

  // Zoom functions
  function zoom_actions(){
      g.attr("transform", d3.event.transform)
  }

  function tickActions() {
    // update node positions each tick of the simulation
  	// TODO : bound to circle's parent limit. https://bl.ocks.org/mbostock/1129492
    node.attr("transform", function(d) {
      //console.log(d); 
      var dx = d.x;
      var dy = d.y;
      return "translate(" + dx + "," + dy + ")"
  	});
    

    // update link positions
    link.attr( "d", function(d) {
      // Muevo los limites del path para que conecte los BORDES de los nodos
      diffX = d.target.x - d.source.x;
      diffY = d.target.y - d.source.y;

      // Length of path from center of source node to center of target node
      pathLength = Math.sqrt((diffX * diffX) + (diffY * diffY));
      var node_dst_radius = node_radius;

      // x and y distances from center to outside edge of target node
      offsetX_dst = (diffX * node_dst_radius) / pathLength;
      offsetY_dst = (diffY * node_dst_radius) / pathLength;

      offsetX_src = offsetX_dst;
      offsetY_src = offsetY_dst;

      return "M" + (d.source.x + offsetX_src) + "," + (d.source.y + offsetY_src) + "L" + (d.target.x - offsetX_dst) + "," + (d.target.y - offsetY_dst);
      /*return "M" + d.source.x + "," + d.source.y + ", " + d.target.x + "," + d.target.y;*/
    });
  }
}

makeSVG("origin", dataset3, 1200);
</script>