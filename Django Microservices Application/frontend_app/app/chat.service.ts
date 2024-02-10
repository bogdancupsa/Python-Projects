import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

export interface ChatMessage {
  message: string;
  senderId: number;
  receiverId: number;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private chatSocket!: WebSocketSubject<ChatMessage>;

  constructor() {}

  initializeWebSocket(userId: number): void {
    this.chatSocket = webSocket<ChatMessage>({
      url: `ws://localhost:8024/ws/chat/${userId}/`,
    });
  }

  sendMessage(message: string, senderId: number, receiverId: number): void {
    if (this.chatSocket) {
      this.chatSocket.next({ message, senderId, receiverId });
    } else {
      console.error('WebSocket is not initialized!');
    }
  }

  getMessages(): Observable<ChatMessage> {
    if (!this.chatSocket) {
      throw new Error('WebSocket is not initialized!');
    }
    return this.chatSocket.asObservable();
  }
}
