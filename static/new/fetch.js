// GET request
const getData = () => {
    console.log('------------------ this is a fetch  --------------------')
    axios({
        method: "get",
        url: "http://127.0.0.1:8001/api/",
    })
        .then((response) => console.log(response))
        .catch((error) => console.log(error));
};
