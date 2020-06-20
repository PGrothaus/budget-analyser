import React from "react";

export function SummarisingValueRenderer(props) {
  return (
    <div onClick={props.onClickHandler}>
    <header className="jumbotron"
            style={{padding: '1rem', color: '#000000', backgroundColor: '#DDDDDD'}}
            >
      <h4>{props.title}:</h4>
      <h4>{props.total}</h4>
    </header>
    </div>
  );
}


function onClickHandler() {
  console.log("Clock from here!");
}
