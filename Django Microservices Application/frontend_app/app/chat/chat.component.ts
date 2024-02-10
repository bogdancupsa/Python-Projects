import { Component, OnInit } from '@angular/core';
import { ChatService, ChatMessage } from '../chat.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  message = '';
  messages: any[] = [];
  userId!: number;
  isAdmin!: boolean;

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    this.initializeUserIds();
    if (this.userId) {
      this.loadMessages();
      this.chatService.getMessages().subscribe({
        next: (chatMessage: any) => {
          console.log(chatMessage.sender_id);

          if(this.isAdmin && parseInt(sessionStorage.getItem('client_id') || '0') !== chatMessage.sender_id) {
            sessionStorage.setItem('client_id', chatMessage.sender_id.toString());
          }
          console.log(chatMessage.receiverId, this.userId);
          
          const shouldDisplay = (this.isAdmin && chatMessage.senderId !== this.userId) ||
                            (!this.isAdmin);
      
          if (shouldDisplay) {
            this.messages.push(chatMessage);
            this.updateMessagesInStorage();
          }
        },
        error: (error) => {
          console.error('Error receiving WebSocket message: ', error);
        }
      });
      
    }
  }
  
  initializeUserIds(): void {
    const adminId = localStorage.getItem('admin_id');
    const clientId = localStorage.getItem('client_id');

    if (adminId) {
      this.userId = parseInt(adminId, 10);
      this.isAdmin = true;
    } else if (clientId) {
      this.userId = parseInt(clientId, 10);
      this.isAdmin = false;
    } else {
      console.error('User ID not found for WebSocket connection');
      return; 
    }

    this.chatService.initializeWebSocket(this.userId);
  }

  sendMessage(): void {
    if (this.message.trim() && this.userId) {
      const receiverId = this.isAdmin ? this.determineReceiverId() : 1;
      if (receiverId > 0) { 
        const chatMessage: ChatMessage = {
          message: this.message,
          senderId: this.userId,
          receiverId: receiverId
        };
        // if (!this.isAdmin) {
          this.messages.push(chatMessage); 
          this.updateMessagesInStorage();
        // }
        this.chatService.sendMessage(chatMessage.message, chatMessage.senderId, chatMessage.receiverId);
        this.message = '';
      } else {
        console.error('Invalid receiver ID');
      }
    }
  }
  
  private loadMessages(): void {
    const storedMessages = sessionStorage.getItem('chatMessages');
    if (storedMessages) {
      this.messages = JSON.parse(storedMessages);
    }
  }

  private updateMessagesInStorage(): void {
    sessionStorage.setItem('chatMessages', JSON.stringify(this.messages));
  }

  private determineReceiverId(): number {
    const selectedClientId = sessionStorage.getItem('client_id');
    if (selectedClientId !== null) {
      return parseInt(selectedClientId, 10);
    }

    return 1;
    
  }
  
}
