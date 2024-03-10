// React & Apollo
import React from "react";
import { useNavigate } from "react-router-dom";

// MUI Components
import LiveHelpIcon from '@mui/icons-material/LiveHelp';
import WarningIcon from '@mui/icons-material/Warning';
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Paper from "@mui/material/Paper";
import { ThemeProvider } from "@mui/material/styles";
import Typography from "@mui/material/Typography";

// Components
import Footer from "../components/Footer";
import StepProgressBar from "../components/StepProgressBar"

// Style
import { canvasTheme } from "../Config";

// ----------------------------------------------------------------------

export default function ExplainCanvas() {



  let navigate = useNavigate(); // 페이지 이동용
  const handleClick = (e) => {
    navigate("../canvas", { replace: true });
  };

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
          <Typography align="center" sx={{ mb: '10px' }}>
            <LiveHelpIcon sx={{ color: canvasTheme.palette.primary.main }} />
          </Typography>
          <Typography variant="subtitle1" align="center" fontWeight={700}>
            Draw a person(s) in the rain.
          </Typography>

          <Typography variant="subtitle1" align="center" sx={{ mb: '10px' }}>
            There is no answer
            <br />

            <Typography align="center" sx={{ mb: '10px' }}>
              <WarningIcon sx={{ color: canvasTheme.palette.warning.main }} />
            </Typography>
            But do not draw a stick figure.
          </Typography>

          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button onClick={handleClick} variant="contained" sx={{ mt: 3, ml: 1 }}>
              Next
            </Button>
          </Box>
        </Paper>

        {/* Footer */}
        <Footer />
      </Container>
    </ThemeProvider>
  );
}
