# Static Scoreboard Deployment Guide

### Note: You need to update `static-scoreboard/js/index.js` on the 7th line to point to your API Gateway endpoint for your finals or preliminary scores API. Instructions to deploy the API(s) can be found in `lambda-connector/` in this repo

1. Upload the entire static-scoreboard directory to an S3 bucket, retaining the directory structure for `css/` `img/` and `js/`
2. Once uploaded, navigate to the `Properties` tab in the S3 UI, and scroll down to the bottom to find `Static website hosting`
3. Enable static website hosting, selecting to `Host a static website` and specify the index document as `index.html`
4. To securely direct traffic to your S3 site, create a [CloudFront](https://console.aws.amazon.com/cloudfront) distribution
5. Set your CloudFront distribution's `Origin Domain Name` to be your S3 bucket you configured static website hosting for.
    - For Origin Domain Name, select the bucket that you created.
    - Set your `Default Root Object` to be `index.html`
    - For Restrict Bucket Access, select Yes.
    - For Origin Access Identity, select Create a New Identity.
    - For Comment, you can choose to keep the default value. Or, you can enter a custom label for the OAI.
    - For Grant Read Permissions on Bucket, select Yes, Update Bucket Policy.
    - It's a best practice to use SSL (HTTPS) for your website. To set up SSL, for SSL Certificate, select Default CloudFront Certificate to use the default CloudFront DNS name. Or, select Custom SSL Certificate to use your own custom domain. You can choose Request or Import a Certificate with ACM to request a new certificate.
6. Once your distribution's statis becomes `Deployed` you can now access your static scoreboard at your distrubtion's `Domain Name`

Once your scoreboard is live, you can make changes to the JavaScript to point to the finals API, or change the static HTML `static-scoreboard/index.html` powering the scoreboard to add announcements or round timings. After uploading changes to your static scoreboard S3 bucket, you can clear our the old cached files by issuing a [CloudFront invalidation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)
