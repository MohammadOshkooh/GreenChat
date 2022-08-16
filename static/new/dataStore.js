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
/*
var groupList = [
    {
        id: 1,
        name: "Programmers",
        members: [0, 1, 3],
        pic: "images/0923102932_aPRkoW.jpg"
    },
];*/
let groupList =
    [
        {
            id: 0,
            name: "chat",
            members: [
                1
            ],
            pic: "http://127.0.0.1:8001/media/profile/group/22/08/12/Screenshot_from_2022-08-13_00-52-44_ouzw2LT.png",
        },
        {
            id: 2,
            name: "First_gp",
            members: [
                2
            ],
            pic: "http://127.0.0.1:8001/media/http%3A/127.0.0.1%3A8000/static/img/index.png",
        },
    ];

// message status - 0:sent, 1:delivered, 2:read

/*let messages = [
    /!*    {
            id: 11,
            sender: 1,
            body: "yeah, i'm online",
            time: "April 28 2018 17:10:21",
            status: 0,
            recvId: 1,
            recvIsGroup: true
        }*!/
];*/

let messages = [
    {
        id: 4,
        sender: 1,
        body: "ok\n",
        time: "April 28 2018 17:10:21",
        status: 2,
        recvId: 1,
        recvIsGroup: true
    },
    {
        id: 5,
        sender: 3,
        body: "han",
        time: "April 28 2018 17:10:21",
        status: 2,
        recvId: 3,
        recvIsGroup: true
    },


];

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