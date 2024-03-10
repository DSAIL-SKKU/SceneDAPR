import { createTheme } from "@mui/material/styles";

export const lightTheme = createTheme({
  palette: {
    mode: "light",
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

export const theme = createTheme({
  palette: {
    mode: "dark",
    secondary: {
      main: "#1ae5be",
    },
  },
  typography: {
    fontFamily: [
      "GyeonggiTitleM",
      "-apple-system",
      "BlinkMacSystemFont",
      '"Segoe UI"',
      "Roboto",
      '"Helvetica Neue"',
      "Arial",
      "sans-serif",
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(","),
    fontWeightLight: 300,
    fontWeightRegular: 500,
    fontWeightMedium: 700,
    fontSize: 16.5,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `


      @font-face {
        font-family: 'GyeonggiTitleM';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_one@1.0/GyeonggiTitleM.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }
    
    
      `,
    },
  },
});

export const canvasTheme = createTheme({
  palette: {
    mode: "light",
  },
  typography: {
    fontFamily: [
      "GyeonggiTitleM",
      "-apple-system",
      "BlinkMacSystemFont",
      '"Segoe UI"',
      "Roboto",
      '"Helvetica Neue"',
      "Arial",
      "sans-serif",
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(","),
    fontWeightLight: 300,
    fontWeightRegular: 500,
    fontWeightMedium: 700,
    fontSize: 16.5,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `
      @font-face {
        font-family: 'GyeonggiTitleM';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_one@1.0/GyeonggiTitleM.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }
      `,
    },
  },
});