/* eslint-disable no-undef */
import {formatCLP} from './formats.js';


const makeArea = (svg, data) => {
  // https://bl.ocks.org/d3noob/119a138ef9bd1d8f0a8d57ea72355252
  console.log("Data area chart", data);

  svg.selectAll('g').remove();
  svg.selectAll('path').remove();
  svg.selectAll('area').remove();
  svg.selectAll('dot').remove();

  // parse the date / time
  var parseTime = d3.timeParse("%Y-%m-%d");

  // format the data
  data.forEach(function(d) {
      d.valued_at = parseTime(d.valued_at);
  });

  const minDate = d3.min(data, (d) => d.valued_at);
  const maxDate = d3.max(data, (d) => d.valued_at);

  var margin = {top: 20, right: 20, bottom: 30, left: 75},
    width = 1300 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;


  // set the ranges
  var x = d3.scaleTime()
            .range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);

  // define the area
  var area = d3.area()
      .x(function(d) { return x(d.valued_at); })
      .y0(height)
      .y1(function(d) { return y(d.value); })


  // define the line
  var valueline = d3.line()
      .x(function(d) { return x(d.valued_at); })
      .y(function(d) { return y(d.value); });

  svg
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + (margin.left) + "," + (margin.top) + ")");

  // scale the range of the data
  x.domain(d3.extent(data, function(d) { return d.valued_at; }));
  y.domain([170500000, d3.max(data, function(d) { return d.value; })]);

  // add the X Axis
  svg.append("g")
      .attr("transform", "translate(" + (margin.left) + "," + (height + margin.top) + ")")
      .call(d3.axisBottom(x));

  // add the Y Axis
  svg.append("g")
      .attr("transform", "translate(" + (margin.left) + "," + (margin.top) + ")")
      .call(d3.axisLeft(y));

  // add the valueline path.
  svg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("stroke", "#69b3a2")
      .attr("stroke-width", 1.5)
      .attr("transform",
            "translate(" + (margin.left) + "," + (margin.top) + ")")
      .attr("d", valueline);

  // add the area
  svg.append("path")
     .data([data])
     .attr("fill", "#cce5df")
     .attr("class", "area")
     .attr("transform",
           "translate(" + (margin.left + 1) + "," + (margin.top) + ")")
     .attr("d", area);

  // Add the data points
  svg.selectAll("dot")
     .data(data)
     .enter()
     .append("circle")
     .attr("fill", "#69b3a2")
     .attr("stroke", "black")
     .attr("r", 3.5)
     .attr("cx", function(d) { return x(d.valued_at); })
     .attr("cy", function(d) { return y(d.value); })
     .attr("transform",
           "translate(" + (margin.left) + "," + (margin.top) + ")")
     .append("svg:title")
       .text(function(d) { return formatCLP(d.value); })
}

export {
  makeArea,
}
