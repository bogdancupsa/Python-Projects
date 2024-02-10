import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-admin-operations',
  templateUrl: './admin-operations.component.html',
  styleUrls: ['./admin-operations.component.css']
})
export class AdminOperationsComponent implements OnInit {
  clients: any[] = [];
  newClient: any = { name: '', role: '' };
  selectedClient: any;
  updatedClient: any = { name: '', role: '' };
  isAdmin: boolean = false;

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit() {
    this.getClients();
    this.isAdmin = localStorage.getItem('admin_id') !== null;
  }

  getClients() {
    this.userService.getClients().subscribe(
      response => {
        this.clients = response;
        console.log(response);
        
      },
      error => {
        console.error('Failed to fetch clients', error);
      }
    );
  }

  addNewClient() {
    this.userService.addClient(this.newClient).subscribe({
      next: response => {
        console.log('Client added successfully', response);
        this.getClients();
        this.newClient = {};
      },
      error: error => {
        console.error('Failed to add client', error);
      }
    });
  }

  editClient(client: any) {
    console.log('Editing client:', client);
    this.selectedClient = client;
    this.updatedClient = { name: client.name, role: client.role };
  }

  saveChanges() {
    this.userService.editClient(this.selectedClient.id, this.updatedClient).subscribe({
        next: response => {
          console.log('Client updated successfully', response);
          this.getClients();
          this.selectedClient = null;
          this.updatedClient = { name: '', role: '' };
        },
        error: error => {
          console.error('Failed to update client', error);
        }
    });
  }

  goToDevices() {
    this.router.navigate(['client-operations']);
  }

  openChat() {
    this.router.navigate(['chat']);
  }

}
