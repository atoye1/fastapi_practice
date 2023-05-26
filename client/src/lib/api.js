const fastapi = async (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = 'application/json'
    let body = JSON.stringify(params)

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

    if (method !== 'get') {
        options['body'] = body
    }
    const result = await fetch(_url, options)
    if (result.status >= 400)
        throw new Error(await result.text())
    return result
}

export default fastapi