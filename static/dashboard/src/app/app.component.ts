import { Component } from '@angular/core';

import { Camera } from './models/camera'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  cameras: Camera[] = [{ip:'127.0.0.1:9900',user:'admin',password:'admin',endpoint:'9990'}];
  addNew: Boolean = false;
}
