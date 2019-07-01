// set the dimensions and margins of the graph
var margint = {topt: 40, rightt: 22, bottomt: 110, leftt: 40},
    widtht = 700 - margint.leftt - margint.rightt,
    heightt = 320 - margint.topt - margint.bottomt;



// set the ranges
var x = d3.scaleBand()
          .range([0, widtht])
          .padding(0.1);
var y = d3.scaleLinear()
          .range([heightt, 0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svgtt = d3.select("body").append("svg")
    .attr("width", widtht + margint.leftt + margint.rightt)
    .attr("height", heightt + margint.topt + margint.bottomt)
  .append("g")
    .attr("transform", 
          "translate(" + margint.leftt + "," + margint.topt + ")");

// get the data
d3.json("http://127.0.0.1:5000/getfile?filename=instances.json", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {

    d.instancescount = +d.instancescount;
  });

  // Scale the range of the data in the domains
  x.domain(data.map(function(d) { return d.region; }));
  y.domain([0, d3.max(data, function(d) { return d.instancescount; })]);

  // append the rectangles for the bar chart
  svgtt.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.region); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.instancescount); })
      .attr("height", function(d) { return heightt - y(d.instancescount); });

  // add the x Axis
  svgtt.append("g")
      .attr("transform", "translate(0," + heightt + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  // add the y Axis
  svgtt.append("g")
      .call(d3.axisLeft(y));
  
      svgtt.append("text")
      .attr("x", (widtht / 7))             
      .attr("y", 377 - (margint.bottomt ))
      .attr("text-anchor", "middle")  
      .style("font-size", "16px") 
      .style("text-decoration", "underline")  
      .text("Instances in each region");

       



});
