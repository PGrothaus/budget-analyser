import React from "react";

export function SummarisingValueRenderer(props) {
  return (
    <header className="jumbotron"
            style={{padding: '1rem', color: '#000000', backgroundColor: '#DDDDDD'}}>
      <h4>{props.title}:</h4>
      <h4>{props.total}</h4>
    </header>
  );
}
