/*
// GET request

const fetchMessages = () => {
    let df = [];
    axios({
        method: "get", url: "http://127.0.0.1:8001/api/message/",
    })
        .then(response => {
            const dJson = JSON.parse(JSON.stringify(response.data));
            for (let i = 0; i < dJson.length; i++) {
                df.push(dJson[i]);
            }
            console.log(df)
         /!*   console.log('in fetch msg')
            console.log(messages.length, " <<<< ");
            console.log(messages)*!/
        })
        .catch((error) => console.log(error));
    return df;
};
*/
