/* eslint-disable no-undef */
import {formatCLP} from './formats.js';

function helperFct(k, colorInterpolator, max) {
  return colorInterpolator(1. * k.total/max);
}


const makeBar = (svg, d) => {
  var colorInterpolator = d3.interpolateRgb("white", "blue");
  const colorDomainLength = d.length;
  const data = d;
  console.log("Data bar chart", data);

  const svgWidth =  400;
  const svgHeight = 500;

  const translateX = 790;
  const translateY = 250;

  const maxValue = d3.max(data, (d) => d.total );
  const tots = d3.sum(data, (d) => d.total);

  data.forEach((d) => {
    d.percentage = d.total / tots;
  });

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

// Add X axis
var x = d3.scaleLinear()
  .domain([0, maxValue])
  .range([ 0, width]);

svg.append("g")
    .attr("transform", "translate(" + (margin.left) + "," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
      .attr("transform", "translate(-10,0)rotate(-45)")
      .style("text-anchor", "end");

// Y axis
var y = d3.scaleBand()
  .range([ 0, height ])
  .domain(data.map(function(d) { return d.category; }))
  .padding(.1);
svg.append("g")
  .attr("transform", "translate(" + (margin.left) + ",0)")
  .call(d3.axisLeft(y))
  .selectAll("text")
    .attr("transform", "translate(-10,-15)rotate(-45)")
    .style("text-anchor", "end");

console.log("rendered the current bar chart");


//Bars
const path = svg.selectAll("myRect")
  .data(data)
  .enter()
  .append("rect")
  .attr("transform", "translate(" + (margin.left + 1) + ",0)")
  .attr("x", x(0) )
  .attr("y", function(d) { return y(d.category); })
  .attr("width", function(d) { return x(d.total); })
  .attr("height", y.bandwidth() )
  .attr("fill", "#69b3a2")
  .append("svg:title")
    .text(function(d) { return formatCLP(d.total); })

return path;
}


export {
  makeBar,
}
