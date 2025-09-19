import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [ RouterOutlet, RouterModule ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App {}
