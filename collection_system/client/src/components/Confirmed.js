// React & Apollo
import React from "react";
import { gql, useQuery } from "@apollo/client";

// MUI Components
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

// Style
import "../style.css";

// Utils
import { calculateElapsedTime } from "../utils/formatTime";

const GET_RESULT = gql`
  query Participant($sketch_id: Int!) {
    getSketchCollectResultBySketchId(sketchId: $sketch_id) {
      id
      image
      imagePath
      strokes
      survey
      startedAt
      endedAt
      participant {
        age
        gender
        id
      }
      
    }
  }
`;

export default function Confirmed() {
  // get sketchId from localStorage
  const sketchId = parseInt(localStorage.getItem("sketchId", 10));

  // get query
  const { loading, error, data } = useQuery(GET_RESULT, {
    variables: { sketch_id: sketchId },
  });

  if (loading) {
    return "loading";
  }
  if (error) {
    console.log(error);
    return `Error! ${error}`;
  }
  if (data) {
    const response = data.getSketchCollectResultBySketchId;

    // Pre-processing data
    const imgUrl = response.image;
    const metaInfo = {
      Gender: response.participant.gender,
      Age: response.participant.age,
    };
    const sketchInfoData = JSON.parse(response.survey);

    // calcuate drawing Time = end time - start time
    const startTime = new Date(response.startedAt);
    const endTime = new Date(response.endedAt);
    const formattedTime = calculateElapsedTime(startTime, endTime);

    const sketchInfo = {
      "Drawing Time": formattedTime,
      "How does the main character in the picture feel?": sketchInfoData.emotion,
      "What is the person in the picture doing?": sketchInfoData.activity,
      "Who is the main character in the picture?": sketchInfoData.mainCharacter,
      "Why is the person in the picture standing in the rain?": sketchInfoData.situation,
      "What will happen to the person in the picture in the future?": sketchInfoData.expectation,
      "What does the person in the picture need?": sketchInfoData.need,
    };

    return (
      <React.Fragment>
        <Typography variant="h5" gutterBottom align="left">
          Thank you <span rolo="img">🙂</span>
          <br />
          Please confirm if the entered information is correct
        </Typography>

        {/* Participant Information */}
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={4} >

            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
              <span rolo="img">👤</span> Participant Information
            </Typography>

            <Grid container>
              {Object.entries(metaInfo).map(([key, value]) => (
                <React.Fragment key={key}>
                  <Grid item xs={6}>
                    <Typography gutterBottom>{key}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography gutterBottom>{value}</Typography>
                  </Grid>
                </React.Fragment>
              ))}
            </Grid>

          </Grid>
        </Grid>

        {/* Sketch Information  */}
        <Grid container spacing={3}>
          <Grid item xs={12} >
            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
              <span rolo="img">🎨</span> Sketch Information
            </Typography>

            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
                <img
                  className="img-frame"
                  src={imgUrl}
                  alt="This is the sketch that you submitted"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <Grid container>
                  {Object.entries(sketchInfo).map(([key, value]) => (
                    <React.Fragment key={key}>
                      <Grid item xs={12}>
                        <Typography gutterBottom style={{ fontWeight: 'bold' }} >{key}</Typography>
                      </Grid>
                      <Grid item xs={12}>
                        <Typography gutterBottom>{value}</Typography>
                      </Grid>
                    </React.Fragment>
                  ))}
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>



      </React.Fragment>
    );
  }
}
