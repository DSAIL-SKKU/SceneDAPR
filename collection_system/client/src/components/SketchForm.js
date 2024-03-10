// React & Apollo
import { gql, useMutation } from "@apollo/client";
import React, { useState } from "react";

import { useNavigate } from "react-router-dom";

// Canvas Components with react-konva
// Reference: https://konvajs.org/docs/react/Free_Drawing.html
import { Layer, Line, Stage } from "react-konva";

// MUI Components
import Paper from "@mui/material/Paper";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import Typography from '@mui/material/Typography';
import Stack from "@mui/material/Stack";

// MUI Icons
import ClearIcon from "@mui/icons-material/Clear";
import CreateIcon from "@mui/icons-material/Create";
import SaveIcon from '@mui/icons-material/Save';
import UndoIcon from '@mui/icons-material/Undo';

// Style
import { styled } from "@mui/material/styles";
import "../style.css";

// ----------------------------------------------------------------------

const CREATE_SKETCH = gql`
  mutation CreateSketch($newSketch: SketchInput!) {
    createSketch(input: $newSketch) {
      id
    }
  }
`;

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: "#fff",
  ...theme.typography.body2,
  margin: "0.5em",
  border: "0px",
  boxShadow: "none",
  color: theme.palette.text.secondary,

}));

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

// ----------------------------------------------------------------------
export default function SketchForm() {
  /*                          */
  /*      navigate, state     */
  /*                          */
  let navigate = useNavigate();
  const participantId = localStorage.getItem("participantId");
  const [startTime, setTime] = useState(new Date()); // for saving start time


  /*                 */
  /*       modal     */
  /*                 */

  const clearModalMessage = "Clearing the canvas will delete all your current sketches. Continue?";
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const submitModalMessage = "Submitting the sketch is final. Proceed?";
  const [openSubmit, setOpenSubmit] = React.useState(false);
  const handleOpenSubmit = () => setOpenSubmit(true);
  const handleCloseSubmit = () => setOpenSubmit(false);

  /*                         */
  /*     canvas settings     */
  /*                         */

  const [tool, setTool] = React.useState("pen");
  const [lines, setLines] = React.useState([]);
  const isDrawing = React.useRef(false);

  const width = 535;
  const height = 757;
  const stageRef = React.useRef(null);

  /*                */
  /*     submit     */
  /*                */
  const [createSketch, { data, loading, error }] = useMutation(CREATE_SKETCH, {
    onCompleted: (data) => {
      const sketchId = data.createSketch.id;
      localStorage.setItem("sketchId", sketchId);
      navigate("../survey", { replace: true });
    },
  });

  const onSubmit = (e) => {
    // close modal
    handleCloseSubmit();

    // submit sketch data
    const sketchData = {
      canvas: {
        height: stageRef.current.attrs.height,
        width: stageRef.current.attrs.width,
      },
      strokes: handleSketch(e),
    };

    const sketchInput = JSON.stringify(sketchData);
    const imageInput = stageRef.current.toDataURL();

    // save drawing end time
    const endTime = new Date();

    const inputData = {
      participantId: parseInt(participantId, 10),
      strokes: sketchInput,
      image: imageInput,
      allowToPublic: true,
      startedAt: startTime,
      endedAt: endTime,
    };

    createSketch({
      variables: { newSketch: inputData },
    });
  };

  /*                             */
  /* mouse, touch event handlers */
  /*                             */

  const [alignment, setAlignment] = React.useState("pen");

  const handleAlignment = (event, newAlignment) => {
    setAlignment(newAlignment);
    console.log(event.target.value);
  };

  // mouse events
  const handleMouseDown = (e) => {
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool, points: [pos.x, pos.y] }]);
  };

  const handleMouseMove = (e) => {
    // Skip if not currently drawing
    if (!isDrawing.current) {
      return;
    }
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastLine = lines[lines.length - 1];

    // Error Handler for {Error: lastLine is undefined} 
    // This can cause a "TypeError: Cannot read property 'points' of undefined" error
    try {
      // Add new point to the last line
      lastLine.points = lastLine.points.concat([point.x, point.y]);
      // Replace the last line in the array
      lines.splice(lines.length - 1, 1, lastLine);
      setLines(lines.concat());
    } catch (e) {
      console.log(e);
    }
  };

  const handleMouseUp = () => {
    isDrawing.current = false;
  };

  // touch events
  const handleTouchStart = (e) => {
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool, points: [pos.x, pos.y] }]);
  };

  const handleTouchMove = (e) => {
    // Skip if not currently drawing
    if (!isDrawing.current) {
      return;
    }
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastLine = lines[lines.length - 1];
    // Add new point to the last line
    lastLine.points = lastLine.points.concat([point.x, point.y]);

    // Replace the last line in the array
    lines.splice(lines.length - 1, 1, lastLine);
    setLines(lines.concat());
  };

  const handleTouchEnd = (e) => {
    isDrawing.current = false;
  };

  /*                       */
  /* canvas tools handlers */
  /*                       */

  // clear all
  const clearCanvas = (e) => {
    handleClose(); // close modal
    setLines([]);
  };

  // undo the last stroke
  const handleUndo = (e) => {
    lines.pop();
    setLines(lines.concat());
  };

  const handleSketch = (e) => {
    // Default format: Array([x1, y1, x2, y2, ..., xn, yn])
    // (0,0) is the top left corner
    // y increases downwards, x increases to the right

    // Reformat to Array([[x1, y1], [x2, y2], ..., [xn, yn]])
    // from Array([x1, y1, x2, y2, ..., xn, yn])
    let original_strokes = [];
    let new_strokes = [];
    lines.forEach((element) => {
      original_strokes.push(element["points"]);
    });

    // Pairing x, y
    original_strokes.forEach((sublist) => {
      let single_storke = [];

      sublist.forEach((element, index) => {
        let remainder = index % 2;
        if (remainder === 0) {
          single_storke.push([sublist[index], sublist[index + 1]]);
        }
      });

      new_strokes.push(single_storke);
    });
    return new_strokes;
  };

  /*                */
  /*       JSX      */
  /*                */

  return (
    <React.Fragment>

      {/* Modal */}
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-description" sx={{ mb: 2 }}>
            {clearModalMessage}
          </Typography>
          <Stack direction="row" justifyContent="flex-end"
            alignItems="flex-start" spacing={2}>

            <Button variant="outlined" onClick={clearCanvas} >예</Button>
            <Button variant="outlined" onClick={handleClose} >아니요</Button>
          </Stack>
        </Box>
      </Modal>

      <Modal
        open={openSubmit}
        onClose={handleCloseSubmit}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-description" sx={{ mb: 2 }}>
            {submitModalMessage}
          </Typography>
          <Stack direction="row" justifyContent="flex-end"

            alignItems="flex-start" spacing={2}>

            <Button variant="outlined" onClick={handleCloseSubmit} >아니요</Button>
            <Button variant="outlined" onClick={onSubmit} >예</Button>
          </Stack>
        </Box>
      </Modal>


      {/* Canvas */}
      <div className="no-drag konajs-frame">

        <Stack direction={{ xs: "column", sm: "row" }} justifyContent="center">
          <ToggleButtonGroup
            value={alignment}
            exclusive
            onChange={handleAlignment}
            aria-label="drawing tool"
          >
            <Item>
              <ToggleButton
                value="pen"
                aria-label="pen"
                onClick={(e) => {
                  setTool(e.target.value);
                }}
              >
                <CreateIcon />
                Pen
              </ToggleButton>
            </Item>

            <Item>
              <ToggleButton
                value="eraser"
                aria-label="eraser"
                onClick={(e) => {
                  handleUndo(e.target.value);
                }}
              >
                <UndoIcon /> Undo
              </ToggleButton>
            </Item>

            <Item>
              <ToggleButton
                value="clear"
                aria-label="clear"
                onClick={handleOpen}
              >
                <ClearIcon />
                Clear All
              </ToggleButton>
            </Item>

            <Item>
              {" "}
              <ToggleButton
                value="submit"
                aria-label="submit"
                onClick={handleOpenSubmit}
              >
                <SaveIcon />
                Submit
              </ToggleButton>
            </Item>
          </ToggleButtonGroup>

        </Stack>

        <Stage
          className="konajs-frame-conent"
          width={width}
          height={height}
          onMouseDown={handleMouseDown}
          onMousemove={handleMouseMove}
          onMouseup={handleMouseUp}
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
          ref={stageRef}

        >
          <Layer>
            {lines.map((line, i) => (
              <Line
                key={i}
                points={line.points}
                stroke="#00000"
                strokeWidth={2}
                tension={0.5}
                lineCap="round"
                bzier={true}
                globalCompositeOperation={
                  line.tool === "eraser" ? "destination-out" : "source-over"
                }
              />
            ))}
          </Layer>
        </Stage>

      </div ></React.Fragment>
  );
}
