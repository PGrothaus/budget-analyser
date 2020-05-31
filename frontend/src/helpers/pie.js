/* eslint-disable no-undef */
import {formatCLP} from './formats.js';

function helperFct(k, colorInterpolator, max) {
  return colorInterpolator(1. * k.total/max);
}


const animatePieSegment = (pathId, arc, arcHover) => {
  const path = d3.select(`path#${pathId}`);
  const parentNode = path.node().parentNode;


  d3.selectAll('.data-text')
    .classed('data-text--show', false);

  d3.selectAll('.data-path')
    .transition()
    .duration(250)
    .attr('d', arc);

  path.transition()
      .duration(250)
      .attr('d', arcHover);

  d3.select(parentNode).select('.data-text__value')
    .classed('data-text--show', true);
  d3.select(parentNode).select('.data-text__name')
    .classed('data-text--show', true);
}

const makePie = (svg, d) => {
  let activeSegmentId;
  var colorInterpolator = d3.interpolateRgb("white", "blue");
  const colorDomainLength = d.length;
  const data = d;
  console.log("Data pie chart", data);
  const max = d3.max(data, (d) => d.total );
  const thickness = 140,
        colorArray = data.map(k => helperFct(k, colorInterpolator, max)),
        color = d3.scaleOrdinal().range(colorArray);

  const svgWidth =  400;
  const svgHeight = 500;
  const radius = 700;
  const translateX = 790
  const translateY = 250

  const tots = d3.sum(data, (d) => d.total);

  data.forEach((d) => {
    d.percentage = d.total / tots;
  });

 svg
  .attr('viewBox', `0 0 ${window.innerWidth + thickness} ${svgHeight + thickness}`)
  .attr('class', 'pie')
  .attr('width', svgWidth)
  .attr('height', svgHeight);

  // Clear all previous svg data
  svg.selectAll('g').remove();
  svg.selectAll('path').remove();
  svg.selectAll('text').remove();

  const g = svg
    .append('g')
    .attr('transform', `translate( ${translateX}, ${translateY})`);

  const arc = d3.arc()
    .innerRadius(radius - thickness)
    .outerRadius(radius);

  const arcHover = d3.arc()
    .innerRadius(radius - ( thickness + 5 ))
    .outerRadius(radius + 8);

  const pie = d3.pie()
    .value(function(pieData) { return pieData.total; })
    .sort(null);


  const path = g.selectAll('path')
  .attr('class', 'data-path')
  .data(pie(data))
  .enter()
  .append('g')
  .attr('class', 'data-group')
  .each(function(pathData, i) {
    const group = d3.select(this)

    group.append('text')
      .text(() => {
        return (pathData.data.percentage % 1 === 0) ? `${d3.format('.0%')(pathData.data.percentage)}` : `${d3.format('.1%')(pathData.data.percentage)}`;
      })
      .attr('class', 'data-text data-text__value')
      .attr('text-anchor', 'middle')
      .attr('dy', '1rem')

    group.append('text')
      .attr('class', 'data-text data-text__name')
      .attr('text-anchor', 'middle')
      .attr('dy', '3.5rem')
      .append('tspan').attr('x', 0).attr('dy', '70').attr('class', 'data-tspan__name')
      .text(`${pathData.data.category}`)
      .append('tspan').attr('x', 0).attr('dy', '90').attr('class', 'data-tspan__value')
      .text(`(${formatCLP(pathData.data.total)} total)`);

    // Set default active segment
    if (pathData.data.total === max) {
      d3.select(this).select('.data-text__value')
      .classed('data-text--show', true);

      d3.select(this).select('.data-text__name')
      .classed('data-text--show', true);
    }

  })
  .append('path')
  .attr('d', arc)
  .attr('fill', (fillData, i) => color(fillData.data.category))
  .attr('class', 'data-path')
  .attr("id", function(d,i) { return "data-path-"+i; })
  .on('mouseover', function() {
    const segmentId = this.id;
    console.log("selected segment", segmentId);
    if (segmentId !== activeSegmentId) {
      activeSegmentId = segmentId;
      animatePieSegment(activeSegmentId, arc, arcHover);
    }
  })
  .each(function(v, i) {
    if (v.total === max) {
      d3.select(this).attr('d', arcHover);
      activeSegmentId = this.id;
    }
    this._current = i;
  });

  return path;
}

export {
  makePie,
}
