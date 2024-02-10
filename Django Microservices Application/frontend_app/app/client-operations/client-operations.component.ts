import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';

@Component({
  selector: 'app-client-operations',
  templateUrl: './client-operations.component.html',
  styleUrls: ['./client-operations.component.css'],
})
export class ClientOperationsComponent implements OnInit {
  devices: any[] = [];
  newDevice: any = { description: '', address: '', max_hourly_energy_consumption: 0, client_id: 0 };
  editedDevice: any = {};
  isAdmin: boolean = false;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.getAllDevices();
    this.newDevice = {};
    this.isAdmin = localStorage.getItem('admin_id') !== null;
  }

  getAllDevices() {
    this.userService.getAllDevices().subscribe({
      next: (response: any) => {
        this.devices = response.devices;
        console.log('Devices retrieved successfully', this.devices);
      },
      error: (error: any) => {
        console.error('Failed to retrieve devices', error);
      },
    });
  }

  addNewDevice() {
    console.log(this.newDevice);
    
    this.userService.addDevice(this.newDevice).subscribe({
      next: (response) => {
        console.log('Device added successfully', response);
        this.getAllDevices();
        this.newDevice = {};
      },
      error: (error) => {
        console.error('Failed to add device', error);
      },
    });
  }

  saveEditedDevice() {
    this.userService.editDevice(this.editedDevice.id, this.editedDevice).subscribe({
      next: (response) => {
        console.log('Device updated successfully', response);
        this.getAllDevices();
        this.editedDevice = {};
      },
      error: (error) => {
        console.error('Failed to update device', error);
      },
    });
  }

  deleteDevice(deviceId: number) {
    console.log('Deleting device with ID:', deviceId);
    this.userService.deleteDevice(deviceId).subscribe({
      next: (response) => {
        console.log('Device deleted successfully', response);
        this.getAllDevices(); // 
      },
      error: (error) => {
        console.error('Failed to delete device', error);
      },
    });
  }

  setEdited(device: any){
    this.editedDevice = device;
  }
}
