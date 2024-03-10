/// React Default
import React from "react";
import { render } from "react-dom";
import { BrowserRouter } from "react-router-dom";
import reportWebVitals from "./reportWebVitals";

// Apollo
import { ApolloProvider } from "@apollo/client";
import client from "./Apollo";

// Style
import ThemeProvider from './theme';

// Routes
import Router from './routes';

const root = document.getElementById("root");
render(
  <ApolloProvider client={client}>
    <BrowserRouter>
      <ThemeProvider>
        <Router />
      </ThemeProvider>
    </BrowserRouter>
  </ApolloProvider>,
  root
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
