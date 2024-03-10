import React from "react";
import { useNavigate } from "react-router-dom";

// MUI Components
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Paper from "@mui/material/Paper";
import { ThemeProvider } from "@mui/material/styles";

// Components
import Confirmed from "../components/Confirmed";
import Footer from "../components/Footer";
import StepProgressBar from "../components/StepProgressBar";

// Style
import { canvasTheme } from "../Config";

export default function App() {

  let navigate = useNavigate(); // 페이지 이동용
  const handleClick = (e) => {
    localStorage.clear();

    navigate("../", { replace: true });
  };

  return (
    <ThemeProvider theme={canvasTheme}>
      <CssBaseline />
      {/* Header */}
      {/* <Header /> */}

      <Container component="main" maxWidth="lg" sx={{ mb: 4 }}>
        <Paper
          variant="outlined"
          sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
        >
          {/* <Typography component="h4" variant="h5" align="center">
            인공지능 훈련을 위한 스케치 데이터 수집
          </Typography> */}
          {/* 단계표시 */}
          <StepProgressBar activeStep={3} />

          {/* 단계내용 */}
          <React.Fragment>
            <Confirmed />
          </React.Fragment>


          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button onClick={handleClick} variant="contained" sx={{ mt: 3, ml: 1 }}>
              홈으로
            </Button>
          </Box>



        </Paper>

        {/* Footer */}
        <Footer />
      </Container>
    </ThemeProvider>
  );
}
