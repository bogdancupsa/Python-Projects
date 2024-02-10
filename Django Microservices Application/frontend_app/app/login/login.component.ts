import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private userService: UserService, private router: Router) { }

  onSubmit() {
    console.log('Form submitted!');
    this.login();
  }

  login() {
    localStorage.clear();
    console.log('Request data:', { username: this.username, password: this.password });
    this.userService.login({ username: this.username, password: this.password }).subscribe(
      response => {
        console.log('Response:', response);
        if (response) {
  
          const tokenKey = 'auth_token';
          const client_id = 'client_id'; 
          const roleKey = 'role';
          localStorage.setItem(tokenKey, response.access);
          localStorage.setItem(roleKey, response.role);
          console.log('Token stored:', localStorage.getItem(tokenKey));
  
          console.log(response.role);
          if (response.role === 'admin') {

          localStorage.setItem('admin_id', response.user_id);
            this.router.navigate(['/admin-operations']);
          } else if (response.role === 'client') {

          localStorage.setItem(client_id, response.user_id);
            this.router.navigate(['/client-page']);
          } else {
            console.error(`Unknown role: ${response.role}`);
          }
  
          this.username = '';
          this.password = '';
        } else {
          console.error('Login failed. No user_id received.');
        }
      },
      error => {
        console.error('Login failed', error);
        if (error.status === 401) {
          console.error('Invalid username or password');
        } else {
          console.error('An unexpected error occurred. Please try again later.');
        }
      }
    );
  }  
}
