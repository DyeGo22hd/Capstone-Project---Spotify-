import { Client, Account, OAuthProvider } from 'appwrite';

const appwrite_project_id = import.meta.env.VITE_PROJECT_ID;
//const appwrite_sessions_api_key = import.meta.env.VITE_APPWRITE_SESSIONS_KEY;

const client = new Client()
    .setEndpoint('https://cloud.appwrite.io/v1') // Your API Endpoint
    .setProject('66f9aeb700248be20f22'); // Your project ID

const account = new Account(client);

export { client, account, OAuthProvider };