import * as React from "react";
// MUI
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Paper from "@mui/material/Paper";
import { ThemeProvider } from "@mui/material/styles";

// Components
import AgreementForm from "../components/AgreementForm"
import Footer from "../components/Footer";
import StepProgressBar from "../components/StepProgressBar";

// Style
import { canvasTheme } from "../Config";

export default function Agreement() {


  return (
    <ThemeProvider theme={canvasTheme}>
      <CssBaseline />
      <Container component="main" maxWidth="lg" sx={{ mb: 4 }}>
        <Paper
          variant="outlined"
          sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
        >

          {/* Stepper */}
          <StepProgressBar activeStep={1} />

          {/* Content */}
          <AgreementForm />
        </Paper>

        {/* Footer */}
        <Footer />
      </Container>
    </ThemeProvider>
  );
}
