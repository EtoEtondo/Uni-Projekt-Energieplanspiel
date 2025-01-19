import React, { useState, useEffect } from "react";
import { fetchInfo, fetchResults } from "../../Requests/GetRequests";
import Plot from "react-plotly.js";
import Carousel from "react-material-ui-carousel";
import { Button } from "@mui/material";
import { editAccess } from "../../Requests/PutRequest";

export const ResultsContent = (props) => {
  const [results, setResults] = useState();

  useEffect(() => {
    fetchResults(props.id).then((response) => {
      props.setError(response.status);
      if (response.status !== -1) {
        props.setMessage(response.message);
      }
      if (response.status === -1) {
        setResults(response.data);
      }
    });
  }, []);

  const giveAccess = () => {
    editAccess(props.id).then((response) => {
      props.setError(response.status);
      props.setMessage(response.message);
    });
  };

  return results ? (
    <React.Fragment>
      {props.role != "GROUP" ? (
        <Button variant="contained" onClick={() => giveAccess()}>
          Ergebnisse freigeben
        </Button>
      ) : (
        ""
      )}

      <Plot
        style={{
          width: "90%",
          height: "100%",
          margin: "2% 5%",
        }}
        useResizeHandler={true}
        data={results["table"].data}
        layout={results["table"].layout}
        config={{ displayModeBar: false}}
      />

      <Plot
        style={{ width: "50%", height: "100%", margin: "2% 25%" }}
        useResizeHandler={true}
        data={results["summary"].data}
        layout={results["summary"].layout}
        config={{ displayModeBar: false }}
      />

      <Carousel
        style={{ width: "90%", height: "100%", margin: "2% 5%" }}
        navButtonsAlwaysVisible={true}
        autoPlay={false}
        onChange={() => {
          window.dispatchEvent(new Event("resize"));
        }}
      >
        {Object.keys(results)
          .filter((keys) => {
            return ["summary", "table"].indexOf(keys) == -1;
          })
          .map((key) => {
            if (["table", "summary"].indexOf(key) == -1) {
              return (
                <Plot
                  divId={key + "0"}
                  style={{ width: "100%", height: "100%" }}
                  useResizeHandler={true}
                  key={key + "0"}
                  data={results[key][0].data}
                  layout={results[key][0].layout}
                  config={{ displayModeBar: false, responsive: true }}
                />
              );
            }
          })}
      </Carousel>

      <Carousel
        style={{ width: "90%", height: "100%", margin: "2% 5%" }}
        navButtonsAlwaysVisible={true}
        autoPlay={false}
        onChange={() => {
          window.dispatchEvent(new Event("resize"));
        }}
      >
        {Object.keys(results)
          .filter((keys) => {
            return ["summary", "table"].indexOf(keys) == -1;
          })
          .map((key) => {
            if (["table", "summary"].indexOf(key) == -1) {
              return (
                <Plot
                  divId={key + "1"}
                  style={{ width: "100%", height: "100%" }}
                  useResizeHandler={true}
                  key={key + "1"}
                  data={results[key][1].data}
                  layout={results[key][1].layout}
                  config={{ displayModeBar: false, responsive: true }}
                />
              );
            }
          })}
      </Carousel>

      <Carousel
        style={{ width: "90%", height: "100%", margin: "2% 5%" }}
        navButtonsAlwaysVisible={true}
        autoPlay={false}
        onChange={() => {
          window.dispatchEvent(new Event("resize"));
        }}
      >
        {Object.keys(results)
          .filter((keys) => {
            return ["summary", "table"].indexOf(keys) == -1;
          })
          .map((key) => {
            if (["table", "summary"].indexOf(key) == -1) {
              return (
                <Plot
                  divId={key + "2"}
                  style={{ width: "100%", height: "100%" }}
                  useResizeHandler={true}
                  key={key + "2"}
                  data={results[key][2].data}
                  layout={results[key][2].layout}
                  config={{ displayModeBar: false, responsive: true }}
                />
              );
            }
          })}
      </Carousel>
    </React.Fragment>
  ) : (
    ""
  );
};
