// React & Apollo
import React, { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gql, useMutation } from "@apollo/client";
import { useForm } from "react-hook-form";

// MUI Components
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Paper from "@mui/material/Paper";

// Style
import { styled } from "@mui/material/styles";
import "../style.css";

// ----------------------------------------------------------------------


const UPDATE_SKETCHINFO = gql`
  mutation UpdateSketchInfo($newSketchInfo: SketchSurveyInput!) {
    updateSketchSurvey(input: $newSketchInfo) {
      id
    }
  }
`;

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body1,
  paddingLeft: theme.spacing(2.5),
  color: theme.palette.text.secondary,
  border: "0px",
  boxShadow: "none",
}));

export default function SurveyForm() {
  // get data from localStorage
  const sketchId = localStorage.getItem("sketchId");

  let navigate = useNavigate();
  const { register, handleSubmit } = useForm();
  const constEmotionOptions = [
    "Happy",
    "Joy",
    "Angery",
    "Lonely",
    "Sad",
    "Want to avoid",
  ];

  const questions = {
    mainCharacter: {
      question: "Who is the main character in the picture? (Optional)",
      placeholder: "Please only fill this field if there are multiple people in the picture. (e.g., the person on the far right)",
    },
    emotion: {
      question: "How does the main character in the picture feel?*",
    },
    activity: {
      question: "What is the person in the picture doing?*",
      placeholder: "Please describe what the main character is doing in the picture.",
    },
    situation: {
      question: "Why is the person in the picture standing in the rain?*",
    },
    expectation: {
      question: "What will happen to the person in the picture in the future?*",
    },
    need: {
      question: "What does the person in the picture need?*",
    },
  }


  /*                */
  /*     submit     */
  /*                */

  const [updateSketchSurvey, { data, loading, error }] = useMutation(
    UPDATE_SKETCHINFO,
    {
      onCompleted: (data) => {
        const updatedPartipantId = data.updateSketchSurvey.id;
        console.log("onCompleted:", updatedPartipantId);
        navigate("../thankyou", { replace: true });
      },
      onError: (error) => {
        console.log("onError:", error);
      },
    }
  );

  const onSubmit = (formData) => {
    let emotion = formData.emotion;
    const emotionExtra = formData.emotionExtra;
    if (emotionExtra) {
      emotion = emotionExtra;
    }

    const sketchInfoData = {
      mainCharacter: formData.mainCharacter,
      emotion: emotion,
      activity: formData.activity,
      situation: formData.situation,
      expectation: formData.expectation,
      need: formData.need,
    };

    console.log("onSubmit:", sketchInfoData);

    const sketchInfoInput = {
      id: parseInt(sketchId, 10),
      survey: JSON.stringify(sketchInfoData),
    };

    updateSketchSurvey({
      variables: { newSketchInfo: sketchInfoInput },
    });
  };

  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom align="center">
        Please describe the picture through the following survey
      </Typography>

      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={3}>

          {/* Question 1 -  mainCharacter */}

          <Grid item xs={12}>
            <label style={{ paddingTop: "1em" }} htmlFor={"mainCharacter"}>
              {questions.mainCharacter.question}
            </label>
            <input
              type="text"
              className="form-control"
              name={"mainCharacter"}
              placeholder={questions.mainCharacter.placeholder}
              {...register("mainCharacter")}
            />
          </Grid>

          {/* Question 2 -  emotion */}

          <Grid item xs={12}>
            <label style={{ paddingTop: "1em" }} htmlFor="emotion">
              How does the main character in the picture feel?
            </label>
            <Stack
              direction="row"
              justifyContent="flex-start"
              alignItems="flex-start"
              spacing={2}
            >
              {constEmotionOptions.map((value) => (
                <Item>
                  <input
                    required
                    className="form-check-input"
                    type="radio"
                    name="emotion"
                    value={value}
                    {...register("emotion")}
                  />
                  <label className="form-check-label" htmlFor={value}>
                    {value}
                  </label>
                </Item>
              ))}
            </Stack>
            {/* Other Emotion */}
            <Item>
              <input
                required
                className="form-check-input"
                type="radio"
                name="emotion"
                value="직접입력"
                {...register("emotion")}
              />
              <label className="form-check-label" htmlFor="">
                Other&nbsp;
              </label>
              <input
                className="form-control-radio"
                type="text"
                name="emotion"
                {...register("emotionExtra")}
              />
            </Item>
          </Grid>

          {/* Question 3 - activity */}
          <Grid item xs={12}>
            <label style={{ paddingTop: "1em" }} htmlFor={"activity"}>
              {questions.activity.question}
            </label>
            <input
              type="text"
              className="form-control"
              name={"activity"}
              {...register("activity")}
              required
            />
          </Grid>



          {/* Question 4 - situation */}
          <Grid item xs={12}>
            <label style={{ paddingTop: "1em" }} htmlFor={"situation"}>
              {questions.situation.question}
            </label>
            <input
              type="text"
              className="form-control"
              name={"situation"}
              {...register("situation")}
              required
            />
          </Grid>


          {/* Question 5 - expectation */}
          <Grid item xs={12}>
            <label style={{ paddingTop: "1em" }} htmlFor={"expectation"}>
              {questions.expectation.question}
            </label>
            <input
              type="text"
              className="form-control"
              name={"expectation"}
              {...register("expectation")}
              required
            />
          </Grid>


          {/* Question 6 - need */}
          <Grid item xs={12}>
            <label style={{ paddingTop: "1em" }} htmlFor={"need"}>
              {questions.need.question}
            </label>
            <input
              type="text"
              className="form-control"
              name={"need"}
              {...register("need")}
              required
            />
          </Grid>


        </Grid>

        <React.Fragment>
          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button type="submit" variant="contained" sx={{ mt: 3, ml: 1 }}>
              Next
            </Button>
          </Box>
        </React.Fragment>
      </form>
    </React.Fragment>
  );
}
