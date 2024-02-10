import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

export interface MonitoringMsg {
  message: string;
  device_id: number;
}

@Injectable({
  providedIn: 'root'
})
export class MonitoringService {
  private monitoringSocket!: WebSocketSubject<MonitoringMsg>;

  constructor() {}

  initializeWebSocket(userId: number): void {
    this.monitoringSocket = webSocket<MonitoringMsg>({
      url: `ws://localhost:8036/ws/monitoring`,
    });
  }

  getMessages(): Observable<MonitoringMsg> {
    if (!this.monitoringSocket) {
      throw new Error('WebSocket is not initialized!');
    }
    return this.monitoringSocket.asObservable();
  }
}