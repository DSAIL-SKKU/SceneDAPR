// React & Apollo
import React, { Fragment } from "react";

// MUI Components
import Typography from "@mui/material/Typography";


function AgreementTerms() {

  const contents = {

    "": `This research focuses on sketch data collection for training an artificial intelligence model. 
    The study is led by {your-research-principal-investigator}.
    Sketch is a widely used communication tool to intuitively express an individual's idea. 
    As sufficient sketch datasets are not available, this study aims to collect free-hand drawings.`,

    "Participation Instructions": `If you agree to participate in the study, 
    you will draw a sketch followed by the given instruction for about 15 minutes.`,

    "Benefits of Participating in this Study": `Although there are no direct benefit for participants, 
    the data obtained from this study can be published as an academic research paper and be open to everyone. 
    The research results could produce royalties in the future, 
    but these future benefits are not provided directly to you.`,

    "Privacy Rights and Confidentiality of Personal Information":
      `This research does not collect sensitive information or personal data.
    This research does not collect sensitive information or personal data. 
    The information provided by you, such as your sketch, gender, age, and self-reported description of the drawing, 
    may be used for presentation purposes (e.g., Sketch A was drawn by a 17-year-old female).`,

    "Potential Risks to Participants": `There is no potential risk to participants, 
    and the researchers will maintain anonymity.`,

    "Research Period and Total Number of Participant": `This research will be conducted from the date of research approval to
    {your-research-period}, and will be conducted for a total of {your-plan} participants.`,

    "Right to Consent and Withdraw": `Participation in this study is entirely voluntary, 
    and you have the right to withdraw your consent at any point during the project. 
    Regardless of your decision, there will be no penalties.`,

    "Consent to Future Uses": `Your data could be provided to other research or researchers outside {your-afflication} in the future.`,

    "Provision of Information on Rights and Interests as Research Subjects": `This study was reviewed and approved 
    by the Institutional Ethics Review Board (IRB) of {your-IRB-information}. 
    If any rights and interests of research subjects are damaged in the future, 
    the researchers will notify the participant as soon as possible. 
    If you have any questions about this research, you can contact the researcher at the top of the first page, 
    and if you have any questions about the infringement of the rights of research participants, 
    you can contact {your-IRB-contact-information}.`,
  };

  return (
    <Fragment>
      {Object.entries(contents).map(([key, value]) => (
        <Fragment>
          <Typography variant="subtitle1">
            {key}
          </Typography>
          <Typography variant="body2" align="justify" sx={{ fontWeight: 300, paddingX: '20px' }} gutterBottom>
            {value}
          </Typography>
        </Fragment>
      ))}
    </Fragment>
  );
}

export default AgreementTerms;
