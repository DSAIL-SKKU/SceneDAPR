import React from 'react';
import { useRoutes } from 'react-router-dom';


// Components for data collection
import Agreement from "./routes/Agreement";
import Canvas from "./routes/Canvas";
import ExplainCanvas from "./routes/ExplainCanvas";
import Survey from "./routes/Survey";
import Thankyou from "./routes/Thankyou";

// ----------------------------------------------------------------------

export default function Router() {
  const routes = useRoutes([
    { path: '/', element: <Agreement /> },
    { path: 'explain', element: <ExplainCanvas /> },
    { path: 'canvas', element: <Canvas /> },
    { path: 'survey', element: <Survey /> },
    { path: 'thankyou', element: <Thankyou /> },
  ]);

  return routes;
}