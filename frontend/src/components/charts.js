/* eslint-disable no-undef */
import React from 'react';
import { makePie } from '../helpers/pie';
import { makeBar } from '../helpers/bar';
import { makeVerticalBar } from '../helpers/verticalBar';
import { makeArea } from '../helpers/area';
import { makeStackedArea } from '../helpers/stackedArea';
/* Component */
const Chart = (props) => {
    const { width, height } = props;
    /* The useRef Hook creates a variable that "holds on" to a value across rendering
       passes. In this case it will hold our component's SVG DOM element. It's
       initialized null and React will assign it later (see the return statement) */
    const d3Container = React.useRef(null);

    /* The useEffect Hook is for running side effects outside of React,
       for instance inserting elements into the DOM using D3 */
    React.useEffect(
        () => {
            const { data, type } = props;

            if (data && d3Container.current) {
              const svg = d3.select(d3Container.current);
              console.log('Going to do a render a pie of type:', type);
              switch (type) {
                  case 'pie': {
                    makePie(svg, data);
                    break;
                  }

                  case 'bar': {
                    makeBar(svg, data);
                    break;
                  }

                  case 'bar-vertical': {
                    makeVerticalBar(svg, data);
                    break;
                  }

                  case 'area': {
                    makeArea(svg, data);
                    break;
                  }

                  case 'stacked-area': {
                    makeStackedArea(svg, data);
                    break;
                  }
              }

              // path.exit().remove();
            }
        },

        /*
            useEffect has a dependency array (below). It's a list of dependency
            variables for this useEffect block. The block will run after mount
            and whenever any of these variables change. We still have to check
            if the variables are valid, but we do not have to compare old props
            to next props to decide whether to rerender.
        */
        [props.data, props.type])

    return (
      <div>
      <svg
          // style={{border: "2px solid gold"}}
          className="d3-component"
          ref={d3Container}
          width={width}
          height={height} />
      </div>
    );
};


export function StackedAreaChart(props) {
  return (
    <Chart
      type="stacked-area"
      data={props.data}
      />
  );
}


export function AreaChart(props) {
  return (
    <Chart
      type="area"
      data={props.data}
      />
  );
}


export function BarChart(props) {
  return (
    <Chart
      type="bar"
      data={props.elems}
      />
  )
}


export function VerticalBarChart(props) {
  return (
    <Chart
      type="bar-vertical"
      data={props.data}
      />
  )
}

export {
 Chart
};
