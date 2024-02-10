
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { AdminOperationsComponent } from './admin-operations/admin-operations.component';
import { CardComponent } from './card/card.component';
import {ClientOperationsComponent} from "./client-operations/client-operations.component";
import { ClientPageComponent } from './client-page/client-page.component';
import { ChatComponent } from './chat/chat.component';
// Import other components and services as needed

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AdminOperationsComponent,
    CardComponent,
    ClientOperationsComponent,
    ClientPageComponent,
    ChatComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    FormsModule, // Add FormsModule here
    AppRoutingModule,
    // Include other modules here
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
