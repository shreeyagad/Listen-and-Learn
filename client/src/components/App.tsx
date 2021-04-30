import React from "react";
import DateFnsUtils from "@date-io/date-fns";
import { ThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import green from "@material-ui/core/colors/green";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import { Home } from "./Home";

const theme = createMuiTheme({
  palette: {
    primary: green,
    secondary: {
      main: "#000000",
    },
  },
});

export const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <Home />
      </MuiPickersUtilsProvider>
    </ThemeProvider>
  );
};
