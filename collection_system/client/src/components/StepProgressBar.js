// React & Apollo
import React from "react";

// MUI Components
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";

// Style
import "../style.css";

const steps = ["Agreement", "Drawing", "Complete"];

export default function StepProgressBar({ activeStep }) {
  return (
    <React.Fragment>
      <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
    </React.Fragment>
  );
}
