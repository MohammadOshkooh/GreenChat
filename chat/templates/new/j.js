import axios from "axios";

const req = async () => {
    const response = await axios.get('http://127.0.0.1:8001/api/')
    console.log('thi is a log!!!!!!!!')
    console.log(response)
}
req();