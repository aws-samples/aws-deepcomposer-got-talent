# Scoring melodies - AI Judge

The AI Judge accepts only compositions in the Musical Instrument Digital Interface (MIDI) format. The current solution is to let participants upload their compositions to S3 through a public-facing URL, and then scoring the melodies. This file provides comprehensive steps and necessary code to set up the architecture and run the AI judge.

### 1. Upload files to S3 using a frontend website

This [aws-samples repository]( https://github.com/aws-samples/amazon-s3-presigned-urls-aws-sam) uses the Serverless Application Model (SAM) to create an application that allows users to upload objects to S3 directly pre-signed URLs. Clone the repository to your local machine and update the following two files before deploying the template. The aws-samples repository has detailed instructions on installing the application. 
1. Replace `frontend/index.html` with the `index.html` file provided in this folder. We update the code to accept only MIDI files. 
2. Replace `getSignedURL/app.js` with the `app.js` code provided in this repository. We update the file to receive a unique name for the file.
3. Update line 34 in `index.html` with the API gateway URL created through the template.
Finally, copy `index.html` to an s3 bucket and host it publicly using CloudFront. Refer to `static-scoreboard/README.md` for instructions on setting up CloudFront.

### 2. Read the melodies from S3 and score
Open the `AI Judge.ipynb` notebook, and replace the S3 bucket name with the bucket created using the SAM template. The repository also contains the pretrained model and the inference code. Make sure all three files are in the same directory. If the pretrained model is saved under a sub-directory, update the path in `inference.py` (line 50). Execute all cells in the notebook, and the final cell will output the scores for each melody. 
