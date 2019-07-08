// set the dimensions and margins of the graph
var margintt = {toptt: 50, righttt: 22, bottomtt: 110, lefttt: 40},
    widthttt = 560 - margintt.lefttt - margintt.righttt,
    heighttt = 310 - margintt.toptt - margintt.bottomtt;



// set the ranges
var x = d3.scaleBand()
          .range([0, widthttt])
          .padding(0.1);
var y = d3.scaleLinear()
          .range([heighttt, 0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svgttt = d3.select("body").append("svg")
    .attr("width", widthttt + margintt.lefttt + margintt.righttt)
    .attr("height", heighttt + margintt.toptt + margintt.bottomtt)
  .append("g")
    .attr("transform", 
          "translate(" + margintt.lefttt + "," + margintt.toptt + ")");

// get the data
d3.json("http://127.0.0.1:5000/getfile?filename=instancestate.json", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {

    d.count = +d.count;
  });

  // Scale the range of the data in the domains
  x.domain(data.map(function(d) { return d.type; }));
  y.domain([0, d3.max(data, function(d) { return d.count; })]);

  // append the rectangles for the bar chart
  svgttt.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.type); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return heighttt - y(d.count); });

  // add the x Axis
  svgttt.append("g")
      .attr("transform", "translate(0," + heighttt + ")")
      .call(d3.axisBottom(x));

  // add the y Axiss
  svgttt.append("g")
      .call(d3.axisLeft(y));
  
      svgttt.append("text")
      .attr("x", (widthttt / 2))             
      .attr("y", 330 - (margintt.bottomtt ))
      .attr("text-anchor", "middle")  
      .style("font-size", "16px") 
      .style("text-decoration", "underline")  
      .text("Size of buckets in KB");

 

});
