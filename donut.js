// margin
var margin = {top: 20, right: 20, bottom: 20, left: 20},
    width = 350 - margin.right - margin.left,
    height = 350 - margin.top - margin.bottom,
    radius = width/2;

// color range

      
var color = d3.scaleOrdinal()
    .range(["#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5", "#2196F3", "#1E88E5", "#1976D2"]);

// donut chart arc
var arc2 = d3.arc()
    .outerRadius(radius - 10)
    .innerRadius(radius - 70);

// arc for the labels position
var labelArc = d3.arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);

// generate pie chart and donut chart
var pie = d3.pie()
    .sort(null)
    .value(function(d) { return d.count; });


// define the svg donut chart
var svg4 = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");




// import data 
d3.json("http://127.0.0.1:5000/getfile?filename=bucketencryptiondetails.json", function(error, data) {

    data.forEach(function(d) {
        d.type = d.type;
        d.buckets = +d.count;
    });


   // "g element is a container used to group other SVG elements"
   var g4 = svg4.selectAll(".arc2")
   .data(pie(data))
 .enter().append("g")
   .attr("class", "arc2");

// append path 
g4.append("path")
   .attr("d", arc2)
   .style("fill", function(d) { return color(d.data.type); })
 .transition()
   .ease(d3.easeLinear)
   .duration(2000)
   .attrTween("d", tweenDonut);
     
// append text
g4.append("text")
 .transition()
   .ease(d3.easeLinear)
   .duration(2000)
 .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
   .attr("dy", ".35em")
   .text(function(d) { return d.data.type; });

   g4.append("text")
   .attr("x", (width / 2))             
   .attr("y", 0 - (margin.top ))
   .attr("text-anchor", "middle")  
   .style("font-size", "16px") 
   .style("text-decoration", "underline")  
   .text("Number of buckets encrypted and unencrypted");
 
});



function tweenDonut(b) {
b.innerRadius = 0;
var i = d3.interpolate({startAngle: 0, endAngle: 0}, b);
return function(t) { return arc2(i(t)); };
}
