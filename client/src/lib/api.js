import qs from 'qs'
import { access_token, username, is_login } from './store';
import { get } from 'svelte/store';
import { push } from 'svelte-spa-router';

const fastapi = async (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = 'application/json'
    let body = JSON.stringify(params)


    if (operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }

    let _url = import.meta.env.VITE_SERVER_URL + url
    if (method === 'get') {
        _url += '?' + new URLSearchParams(params)
    }

    let options = {
        method,
        headers: {
            "Content-Type": content_type
        }
    }

    const _access_token = get(access_token)
    if (_access_token)  {
        options.headers['Authorization'] = 'Bearer ' + _access_token    
    }

    if (method !== 'get') {
        options['body'] = body
    }
    const result = await fetch(_url, options)

    if (operation !== 'login' && result.status === 401) {
        access_token.set('')
        username.set('')
        is_login.set(false)
        alert('Login Required')
        push('/user-login')
    }
    if (result.status >= 400)
        throw new Error(await result.text())
    return result
}

export default fastapi