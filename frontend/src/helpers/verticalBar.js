/* eslint-disable no-undef */
import {formatCLP} from './formats.js';
import {formatPct} from './formats.js';

function helperFct(k, colorInterpolator, max) {
  return colorInterpolator(1. * k.total/max);
}


const makeVerticalBar = (svg, d) => {
  var colorInterpolator = d3.interpolateRgb("white", "blue");
  const data = d;
  console.log("Data bar chart", data);

  const svgWidth =  1300;
  const svgHeight = 450;

  const translateX = 790;
  const translateY = 250;

  // parse the date / time
  function parseTime(elem) {return elem.substring(0, 7);}

  // format the data
  data.forEach(function(d) {
      d.month = parseTime(d.month);
  });

  var maxValue = 1.1 * d3.max(data, (d) => d.monthly_total);
  if (maxValue > 1000) {
    maxValue = 4900000;
  }

  // set the dimensions and margins of the graph
var margin = {top: 0, right: 20, bottom: 60, left: 90},
    width = svgWidth - margin.left - margin.right,
    height = svgHeight - margin.top - margin.bottom;

// append the svg object to the body of the page
const g = svg
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr('transform', `translate( ${translateX}, ${translateY})`);

svg.selectAll('g').remove();
svg.selectAll('myRect').remove();
svg.selectAll('rect').remove();

// Add XY axis
var y = d3.scaleLinear()
  .domain([0, maxValue])
  .range([height, 0]);

  // X axis
var x = d3.scaleBand()
  .range([ 0, width ])
  .domain(data.map(function(d) { return d.month; }))
  .padding(.1);

svg.append("g")
  .attr("transform", "translate(" + (margin.left) + ",0)")
  .call(d3.axisLeft(y))
  .selectAll("text")
    .style("text-anchor", "end");

svg.append("g")
    .attr("transform", "translate(" + (margin.left) + "," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
      .attr("transform", "translate(0,0)rotate(-45)")
      .style("text-anchor", "end");


console.log("rendered the current bar chart");


//Bars
const path = svg.selectAll("myRect")
  .data(data)
  .enter()
  .append("rect")
  .attr("transform", "translate(" + (margin.left + x.bandwidth() / 4) + ",0)")
  .attr("y", function(d) { return y(d.monthly_total); })
  .attr("x", function(d) { return x(d.month); })
  .attr("height", function(d) { return height - y(d.monthly_total); })
  .attr("width", x.bandwidth() / 2 )
  .attr("fill", "#69b3a2")
  .append("svg:title")
    .text(function(d) { return format(d.monthly_total); })

return path;
}

function format(val) {
  if (val > 1000) {
    return formatCLP(val)
  }
  return formatPct(val)
}

export {
  makeVerticalBar,
}
