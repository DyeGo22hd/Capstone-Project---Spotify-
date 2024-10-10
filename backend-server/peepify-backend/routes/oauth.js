const appwrite_project_id = process.env.PROJECT_ID;
const appwrite_sessions_api_key = process.env.APPWRITE_SESSIONS_KEY;

var appwrite_sdk = require('node-appwrite');

var express = require('express');
var router = express.Router();

const client = new appwrite_sdk.Client()
    .setEndpoint('https://cloud.appwrite.io/v1') // Appwrite API Endpoint
    .setProject(appwrite_project_id) // Appwrite project ID
    .setKey(appwrite_sessions_api_key); // Your secret API key

router.get('/login', async function (req, res, next) {
    const account = new appwrite_sdk.Account(client);

    const result = await account.createOAuth2Token(
        'spotify', // provider
        'http://localhost:5000/oauth/success', // success (optional)
        'http://localhost:5000/oauth/fail', // failure (optional)
        ['user-read-currently-playing'] // scopes (optional)
    );

    res.redirect(result);
})

router.get('/success', async function (req, res, next) {
    const account = new appwrite_sdk.Account(client);

    // Get the userId and secret from the URL parameters
    const { userId, secret } = req.query;

    try {
        // Create the session using the Appwrite client
        const session = await account.createSession(userId, secret);

        console.log('Session created successfully:', session);

        // Convert the ISO 8601 date string to a Date object and calculate the maxAge in milliseconds
        const expireDate = new Date(session.expire);
        const currentDate = new Date();
        const maxAge = expireDate - currentDate; // Difference in milliseconds maxAge = session.expire ? parseInt(session.expire, 10) : 3600000; // 1 hour in milliseconds

        // Set the session cookie
        res.cookie('session', session.secret, { // Use the session secret as the cookie value
            httpOnly: true,
            secure: true,
            sameSite: 'strict',
            maxAge: maxAge,
            path: '/',
        });

        res.status(200).json({ success: true });
    } catch (e) {
        res.status(400).json({ success: false, error: e.message });
    }

})

router.get('/fail', async function (req, res, next) {
    res.render('failed', { title: 'uh oh' });
})

module.exports = router;
