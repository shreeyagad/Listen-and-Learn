import React from "react";
import DateFnsUtils from "@date-io/date-fns";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import { Home } from "./Home";

export const App = () => {
  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Home />
    </MuiPickersUtilsProvider>
  );
};
