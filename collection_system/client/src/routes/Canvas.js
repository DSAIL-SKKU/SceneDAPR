// React & Apollo
import React from "react";

// MUI Components
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import { ThemeProvider } from "@mui/material/styles";

// Components
import SketchForm from "../components/SketchForm"
import Footer from "../components/Footer";
import StepProgressBar from "../components/StepProgressBar";


// Style
import { canvasTheme } from "../Config";

export default function Canvas() {
  const participantId = localStorage.getItem("participantId");

  return (
    <ThemeProvider theme={canvasTheme}>
      <CssBaseline />

      <Container
        component="main"
        maxWidth="lg"
        sx={{ mb: 4 }}
        classes="no-drag"
      >
        <Paper
          variant="outlined"
          sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
        >

          {/* Stepper */}
          <StepProgressBar activeStep={2} />



          {/* Content */}
          <SketchForm />

          <Typography variant="body2" align="right">
            No.: {participantId}
          </Typography>
        </Paper>

        {/* Footer */}
        <Footer />
      </Container>
    </ThemeProvider>
  );
}
