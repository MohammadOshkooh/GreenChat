let user = {
    id: 0,
    name: "Anish",
    number: "+91 91231 40293",
    pic: "images/asdsd12f34ASd231.png"
};

let contactList = [
    {
        id: 1,
        name: "mphammad069",
        pic: "http://127.0.0.1:8001/media/http%3A/127.0.0.1%3A8000/static/img/index.png"
    },
    {
        id: 2,
        name: "q",
        pic: "http://127.0.0.1:8001/media/http%3A/127.0.0.1%3A8000/static/img/index.png"
    },
    {
        id: 3,
        name: "mohammad",
        pic: "http://127.0.0.1:8001/media/http%3A/127.0.0.1%3A8000/static/img/index.png"
    }
];

/*
let contactList = [
    {
        id: 0,
        name: "Anish",
        number: "+91 91231 40293",
        pic: "images/asdsd12f34ASd231.png",
        lastSeen: "Apr 29 2018 17:58:02"
    },

];*/
let groupList = [
    {
        "id": 1,
        "name": "chat",
        "members": [
            1
        ],
        "pic": "http://127.0.0.1:8001/media/profile/group/22/08/12/Screenshot_from_2022-08-13_00-52-44_ouzw2LT.png",
        "owner": 1,
        "link": "N2PiRZifuOkUzRGJQWXJKN"
    },
    {
        "id": 2,
        "name": "First_gp",
        "members": [
            2
        ],
        "pic": "http://127.0.0.1:8001/media/http%3A/127.0.0.1%3A8000/static/img/index.png",
        "owner": 2,
        "link": "08QTMi6bLOn52bYkO4MZGP"
    },
    {
        "id": 3,
        "name": "gp",
        "members": [
            3
        ],
        "pic": "http://127.0.0.1:8001/media/http%3A/127.0.0.1%3A8000/static/img/index.png",
        "owner": 3,
        "link": "hyYP6Y1VAiRBx9AMaj6gNc"
    }
];


// message status - 0:sent, 1:delivered, 2:read

let messages = [];

/*

let messages = [
    {
        "id": 1,
        "__str__": "mphammad069",
        "sender": 1,
        "body": "h\n",
        "time": "2022-08-12T20:13:35.448660Z",
        "status": 0,
        "recvId": 1,
        "recvIsGroup": true
    },
    {
        "id": 2,
        "__str__": "mphammad069",
        "sender": 1,
        "body": "hello\n",
        "time": "2022-08-12T20:13:39.764179Z",
        "status": 0,
        "recvId": 1,
        "recvIsGroup": true
    },
    {
        "id": 3,
        "__str__": "mphammad069",
        "sender": 1,
        "body": null,
        "time": "2022-08-12T20:41:41.751185Z",
        "status": 0,
        "recvId": 1,
        "recvIsGroup": true
    },
    {
        "id": 4,
        "__str__": "mphammad069",
        "sender": 1,
        "body": "ok\n",
        "time": "2022-08-12T20:41:46.512156Z",
        "status": 0,
        "recvId": 1,
        "recvIsGroup": true
    },
    {
        "id": 5,
        "__str__": "mohammad",
        "sender": 3,
        "body": "han",
        "time": "2022-08-15T10:19:02.491427Z",
        "status": 0,
        "recvId": 3,
        "recvIsGroup": true
    },
    {
        "id": 6,
        "__str__": "mohammad",
        "sender": 3,
        "body": "f",
        "time": "2022-08-15T18:48:08.527743Z",
        "status": 0,
        "recvId": 3,
        "recvIsGroup": true
    },
    {
        "id": 7,
        "__str__": "mohammad",
        "sender": 3,
        "body": "v",
        "time": "2022-08-15T18:49:47.602619Z",
        "status": 0,
        "recvId": 3,
        "recvIsGroup": true
    }]

*/

let MessageUtils = {
    getByGroupId: (groupId) => {
        return messages.filter(msg => msg.recvIsGroup && msg.recvId === groupId);
    },
    getByContactId: (contactId) => {
        return messages.filter(msg => {
            return !msg.recvIsGroup && ((msg.sender === user.id && msg.recvId === contactId) || (msg.sender === contactId && msg.recvId === user.id));
        });
    },
    getMessages: () => {
        return messages;
    },
    changeStatusById: (options) => {
        messages = messages.map((msg) => {
            if (options.isGroup) {
                if (msg.recvIsGroup && msg.recvId === options.id) msg.status = 2;
            } else {
                if (!msg.recvIsGroup && msg.sender === options.id && msg.recvId === user.id) msg.status = 2;
            }
            return msg;
        });
    },
    addMessage: (msg) => {
        msg.id = messages.length + 1;
        messages.push(msg);
    }
};