const chat = document.querySelector('.chat');


async function getAllMessages (){
const messagesArr = await get('messages')
//sort messagesArr by created_at
let sortedMessagesByDate = messagesArr.sort((a,b)=>{
  return new Date(b.created_at) - new Date(a.created_at)
})
  //  console.log(sortedMessagesByDate);
const formattedMessages = await messageFormat(sortedMessagesByDate);
Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
}

getAllMessages()
 

async function get(endpoint) {
    const response = await fetch(`http://127.0.0.1:8000/api/${endpoint}/`)
    data = await response.json();
    return data;
}

// functionality for getting messages from a specific room .
async function proccessMessages (wantedRoom) {
  chat.innerHTML = '' 
  let messages = await getMessagesFromRoom(wantedRoom);
  const formattedMessages = messageFormat(messages);
  Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
      }

      const getMessagesFromRoom = async (wantedRoom) => {
        const response = await fetch(`http://127.0.0.1:8000/api/messages/`);
        data = await response.json();
        const selectedRoom = data.filter(message => message.room.includes(wantedRoom));  
        return selectedRoom
      }
  
      async function messageFormat(messages)  {
        formattedMessagesArr = messages.map(async (message)=>{
          const userName = await getUserName(message.profile)
          const roomName = await getRoomName(message.room)
          const formatYmd = date => date.toISOString().slice(0, 10);
          const formatHms = new Date(message.created_at)+"";
          console.log(typeof(formatHms));
          console.log(formatHms);
          const outputMessage = 
          `Room: ${roomName}<br>
          <p>Sent by: ${userName}:, at: ${String(formatHms).slice(0,21)}</p>
          <p>${message.content}</p>

          <hr>`
          console.log();
          return outputMessage
          
        })
        return formattedMessagesArr;
      }

      async function getUserName(profileLink){
        const response = await fetch(`${profileLink}`)
        const data = await response.json()
        const userName = data.discord_name;
        return userName;
      }

      async function getRoomName(roomLink){
        const response = await fetch(`${roomLink}`)
        const data = await response.json()
        const roomName = data.__str__;
        return roomName;
      }

      function displayMessages(message){
        const messageDiv = document.createElement('div');
          messageDiv.innerHTML = message;
          return chat.appendChild(messageDiv);
      }
 


