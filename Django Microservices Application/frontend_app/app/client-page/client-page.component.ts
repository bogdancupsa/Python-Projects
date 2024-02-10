import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';

@Component({
  selector: 'app-client-page',
  templateUrl: './client-page.component.html',
  styleUrls: ['./client-page.component.css']
})
export class ClientPageComponent implements OnInit{

  devices: any[] = [];

  constructor(private userService: UserService) {}

  ngOnInit() {
    // Assuming you have the user ID available after login
    const userId = Number(localStorage.getItem('client_id')); // Replace with your actual user ID retrieval logic
    if (userId) {
      this.getUserDevices(userId);
    }
  }

  getUserDevices(userId: number) {
    this.userService.getUserDevices(userId).subscribe({
      next: (response: any) => {
        this.devices = response.devices;
      },
      error: (error: any)  => {
        console.error('Failed to fetch user devices', error);
      }
    });
  }

  openChat(): void {
    
  }

}
