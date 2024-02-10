import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000/';
  private baseUrl = 'http://localhost:8012/';

  constructor(private http: HttpClient) { }

  login(credentials: { username: string, password: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}api-token-auth/`, credentials);
  }

  getClients(): Observable<any[]> {
    const tokenKey = 'auth_token'; 
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
    });
    return this.http.get<any[]>(`${this.apiUrl}clients/`, { headers });
  }
  
  addClient(newClient: any): Observable<any> {
    console.log('Request Payload:', newClient);
    const tokenKey = 'auth_token'; 
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
    });

    return this.http.post<any>(`${this.apiUrl}clients/`, newClient, { headers });
  }
  
  editClient(clientId: number, updatedClient: any): Observable<any> {
    const tokenKey = 'auth_token'; 
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
    });
    return this.http.put<any>(`${this.apiUrl}clients/${clientId}/`, updatedClient, { headers });
  }
  
  deleteClient(clientId: number): Observable<any> {
    const tokenKey = 'auth_token'; 
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
    });
    return this.http.delete<any>(`${this.apiUrl}clients/${clientId}/`, { headers });
  }
  
  getAllDevices(): Observable<any> {
    const tokenKey = 'auth_token'; 
    const roleKey = 'role';
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
      'X-User-Role': localStorage.getItem(roleKey) || 'defaultRole'
    });
    return this.http.get<any>(`${this.baseUrl}get_all_devices/`, {headers: headers});
  }

  getUserDevices(userId: number): Observable<any> {
    const tokenKey = 'auth_token'; 
    const roleKey = 'role';
    const role = localStorage.getItem(roleKey) || 'defaultRole';
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
      'X-User-Role': role
    });
    return this.http.get<any>(`${this.baseUrl}get_user_devices/${userId}/`, {headers: headers});
  }

  addDevice(deviceData: any): Observable<any> {
    const tokenKey = 'auth_token'; 
    const roleKey = 'role';
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
      'X-User-Role': localStorage.getItem(roleKey) || 'defaultRole'
    });
  
    return this.http.post(`${this.baseUrl}add_device/`, deviceData, {headers: headers});
  }
  
  editDevice(deviceId: number, deviceData: any): Observable<any> {
    const tokenKey = 'auth_token'; 
    const roleKey = 'role';
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
      'X-User-Role': localStorage.getItem(roleKey) || 'defaultRole'
    });
    return this.http.put(`${this.baseUrl}edit_device/${deviceId}/`, deviceData, {headers: headers});
  }

  deleteDevice(deviceId: number): Observable<any> {
    const tokenKey = 'auth_token'; 
    const roleKey = 'role';
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem(tokenKey)}`,
      'X-User-Role': localStorage.getItem(roleKey) || 'defaultRole'
    });
    return this.http.delete(`${this.baseUrl}delete_device/${deviceId}/`, {headers: headers});
  }

}
