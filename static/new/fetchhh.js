// GET request

const fetchFromApi = (url) => {
    let data = [];
    fetch(url)
        .then(response => response.json())

        .then(responseData => {
            for (let i = 0; i < responseData.length; i++) {
                data.push(responseData[i]);
            }
        })
        .catch((error) => console.log(error));
    return data;
};
