import { Component, Input, Output, EventEmitter } from '@angular/core';
import { UserService } from '../user.service';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent {
  @Input() cardData: any;
  @Output() editEvent = new EventEmitter<any>();
  @Output() deleteEvent = new EventEmitter<number>();

  constructor(private userService: UserService) {
    console.log();
    
  }

  editCard() {
    console.log('Edit card', this.cardData);

    if (this.cardData.id) {
      this.editEvent.emit(this.cardData);
    }
  }

  deleteCard() {
    this.userService.deleteClient(this.cardData.id).subscribe({
      next: response => {
        console.log('cupsa da');
        
      },
      error: err => {
        console.error('cupsa nu');
        
      }
    })
  }
}
