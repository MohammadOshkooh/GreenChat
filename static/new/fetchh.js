// GET request
const fetchData = () => {
    let data = [];
    axios({
        method: "get",
        url: "http://127.0.0.1:8001/api/",
    })
        .then(response => {
            console.log(response.data)
            console.log(response.data[0])
            console.log(response.data['body'])
            for (let i = 0; i < response.data.length; i++) {
                response.data['recvId'] = response.data['related_chat'];
                delete response.data['related_chat'];
            }
            console.log(response.data)
        })
        .catch((error) => console.log(error));

};


// function fetchMessagesFormApi(){
//     let data = fetchData()
//     console.log(data)
// }

