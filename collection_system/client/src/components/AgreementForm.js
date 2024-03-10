// React & Apollo
import { gql, useMutation } from "@apollo/client";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

// MUI Components
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";

// Components for data collection
import AgreementTerms from "../components/AgreementTerms"

// Style
import "../style.css";

// ----------------------------------------------------------------------

const CREATE_USER = gql`
  mutation CreateParticipant($newPartipant: ParticipantInput!) {
    createParticipant(input: $newPartipant) {
      id
    }
  }
`;

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body1,
  padding: theme.spacing(0),
  textAlign: "center",
  color: theme.palette.text.secondary,
  border: "0px",
  boxShadow: "none",
  marginLeft: "2em",
  // marginRight: "2em",
}));

// ----------------------------------------------------------------------

export default function AgreementForm() {
  /*                 */
  /*     content     */
  /*                 */

  const genderOptions = [
    "Woman", "Man", "Other"
  ];
  const checkboxNote = `I have been informed about the contents of this agreement, 
  comprehended its content, and received answers to my questions. 
  I voluntarily agree to participate in this research, so I sign the consent form.`;

  /*                                   */
  /*      navigate, handler, state     */
  /*                                   */

  let navigate = useNavigate(); // For page navigation
  const { register, handleSubmit } = useForm(); // For form handling
  const [agree, setAgree] = useState(false);
  const handleCheckbox = () => {
    // if agree === true, it will be set to false
    // if agree === false, it will be set to true
    setAgree(!agree);
    // Don't miss the exclamation mark
  };



  /*                */
  /*     submit     */
  /*                */

  const [createParticipant, { data, loading, error }] = useMutation(
    CREATE_USER,
    {
      onCompleted: (data) => {
        const newPartipantId = data.createParticipant.id;
        const newPartipantName = `참가자+${newPartipantId}번`;
        localStorage.setItem("participantId", newPartipantId);
        localStorage.setItem("participantName", newPartipantName);
        navigate("../explain", { replace: true });
      },

      onError: (error) => {
        console.log("onError:", error);
      },
    }
  );

  const onSubmit = (formData) => {
    const inputData = {
      name: '',
      age: parseInt(formData.age, 10),
      gender: formData.gender,
    };
    console.log("제출하기", inputData);
    createParticipant({
      variables: { newPartipant: inputData },
    });
  };


  /*                */
  /*       JSX      */
  /*                */

  return (
    <React.Fragment>

      <Typography variant="h6" gutterBottom align="left">
        Participant Information
      </Typography>


      <form onSubmit={handleSubmit(onSubmit)}>

        {/* Participant Information Form */}
        <Grid container spacing={3} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6}>
            <label htmlFor="age">
              Age*
              {/* 나이* */}
            </label>
            <input
              type="number"
              className="form-control"
              required
              {...register("age")}
            />
          </Grid>
        </Grid>


        <Grid container spacing={3} >
          <Grid item xs={12} sm={6}>
            <label htmlFor="gender">
              Gender*
              {/* 성별* */}
            </label>
            <Stack
              direction="row"
              justifyContent="flex-start"
              alignItems="flex-start"
              spacing={3}
            >
              {genderOptions.map((value) => (
                <Item>
                  <input
                    className="form-check-input"
                    type="radio"
                    name="gender"
                    value={value}
                    required
                    {...register("gender")}
                  />
                  <label htmlFor={value}>&nbsp;{value}&nbsp;&nbsp;&nbsp;&nbsp;</label>
                </Item>
              ))}
            </Stack>
            <br />
          </Grid>
        </Grid>


        {/* Agreement Form */}
        <Typography variant="h6" gutterBottom align="left">
          Agreement Form
          {/* 연구참여자 동의서 */}
        </Typography>
        <AgreementTerms />


        <Grid item xs={12} sx={{ paddingY: '20px' }}>
          <FormControlLabel
            control={
              <Checkbox
                color="primary"
                name="agree"
                onChange={handleCheckbox}
              />
            }
            label={checkboxNote}
          />
        </Grid>

        {/* Submit & Start Button */}
        <React.Fragment>
          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button
              type="submit"
              variant="contained"
              sx={{ mt: 3, ml: 1 }}
              disabled={!agree}
            >
              Start
              {/* 시작하기 */}
            </Button>
          </Box>
        </React.Fragment>
      </form>
    </React.Fragment>
  );
}
