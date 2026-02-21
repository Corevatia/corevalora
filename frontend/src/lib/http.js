const BASE_URL = "http://localhost:8000";

export async function request(path, options = {})
{
    const response = await fetch(BASE_URL + path, options)

    if (!response.ok) {
        throw new Error("HTTP Error " + response.status);
    }
    
    return response.json();
}