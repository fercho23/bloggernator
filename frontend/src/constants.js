

export const URL_BACKEND = "http://127.0.0.1:8000";

export const URL_API = '/api/';

// ACCOUNT
    export const URL_API_ACCOUNT = URL_API + 'account/';
    
    export const URL_API_ACCOUNT_SIGNUP = URL_API_ACCOUNT + 'signup/';
    export const URL_API_ACCOUNT_LOGOUT = URL_API_ACCOUNT + 'logout/';
    export const URL_API_ACCOUNT_LOGIN = URL_API_ACCOUNT + 'login/';
// -- ACCOUNT

// POST
    export const URL_API_POST = URL_API + 'post/';

    export const URL_API_POST_CREATE = URL_API_POST + 'create/';
    export const URL_API_POST_LIST = URL_API_POST + 'list/';
    export const URL_API_POST_READ = URL_API_POST + ':slug/';
    export const URL_API_POST_DELETE = URL_API_POST + ':slug/delete/';
    export const URL_API_POST_UPDATE = URL_API_POST + ':slug/update/';
// -- POST
