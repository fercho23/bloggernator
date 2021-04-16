

export const URL_BACKEND = "http://127.0.0.1:8000";

export const URL_API = '/api/';

// ACCOUNT
    export const URL_API_ACCOUNT = URL_API + 'account/';
    
    export const URL_API_ACCOUNT_SIGNUP = URL_API_ACCOUNT + 'signup/';
    export const URL_API_ACCOUNT_LOGOUT = URL_API_ACCOUNT + 'logout/';
    export const URL_API_ACCOUNT_LOGIN = URL_API_ACCOUNT + 'login/';
// -- ACCOUNT

// COMMUNITY
    export const URL_API_COMMUNITY = URL_API + 'community/';

    // export const URL_API_COMMUNITY_CREATE = URL_API_COMMUNITY + 'create/';
    export const URL_API_COMMUNITY_CURRENT_USER_LIST = URL_API_COMMUNITY + 'current_user/list/';
    export const URL_API_COMMUNITY_LIST = URL_API_COMMUNITY + 'list/';
    // export const URL_API_COMMUNITY_READ = URL_API_COMMUNITY + ':slug/';
    // export const URL_API_COMMUNITY_DELETE = URL_API_COMMUNITY + ':slug/delete/';
    // export const URL_API_COMMUNITY_UPDATE = URL_API_COMMUNITY + ':slug/update/';
// -- COMMUNITY

// language
    export const URL_API_LANGUAGE = URL_API + 'language/';

    export const URL_API_LANGUAGE_LIST = URL_API_LANGUAGE + 'list/';
// -- language

// POST
    export const URL_API_POST = URL_API + 'post/';

    export const URL_API_POST_CREATE = URL_API_POST + 'create/';
    export const URL_API_POST_LIST = URL_API_POST + 'list/';
    export const URL_API_POST_READ = URL_API_POST + ':slug/';
    export const URL_API_POST_DELETE = URL_API_POST + ':slug/delete/';
    export const URL_API_POST_UPDATE = URL_API_POST + ':slug/update/';
// -- POST
