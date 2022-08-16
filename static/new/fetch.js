// GET request
const fetchMessages = () => {
    let data = [];
    axios({
        method: "get",
        url: "http://127.0.0.1:8001/api/message/",
    })
        .then(response => {
            for (let i = 0; i < response.data.length; i++) {
                data.push(response.data[i]);
            }
        })
        .catch((error) => console.log(error));

    return data;
};

const fetchChat = () => {
    let data = [];
    axios({
        method: "get",
        url: "http://127.0.0.1:8001/api/chat/",
    })
        .then(response => {
            for (let i = 0; i < response.data.length; i++) {
                data.push(response.data[i]);
            }
        })
        .catch((error) => console.log(error));

    return data;
};

