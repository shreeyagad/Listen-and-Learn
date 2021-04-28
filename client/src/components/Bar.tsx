import React from "react";
import { makeStyles } from "@material-ui/core";

export interface BarProps {
  barHeight: number;
  children: React.ReactNode;
}

const useStyles = makeStyles({
  bar: {
    display: "flex",
    justifyContent: "center",
    padding: (props: BarProps) => `${props.barHeight}px 0px`,
    overflow: "auto",
  },
});

export const Bar = (props: BarProps) => {
  const classes = useStyles(props);
  return <div className={classes.bar}>{props.children}</div>;
};
