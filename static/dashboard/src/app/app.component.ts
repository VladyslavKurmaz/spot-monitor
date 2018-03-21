import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { Camera } from './models/camera'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  errorMessage = '';
  cameras: Camera[] = [];//[{ip:'127.0.0.1:9900',user:'admin',password:'admin',endpoint:'9990'}];
  addNew: Boolean = false;

  constructor(private http: HttpClient){
  }

  ngOnInit() {
    this.http.get('http://46.101.7.84:8000/cameras')
      .subscribe(
        data => this.cameras,
        error => this.handleError(error)
      );
  }

  private handleError(error: HttpErrorResponse) {
    console.log('Error');
    console.log(error);
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
      this.errorMessage = error.error.message;
    } else if (error.error instanceof ProgressEvent) {
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      let msg = `Backend returned code ${error.status}, ` +
                `body was: ${error.error}`;
      console.error(msg);
      this.errorMessage = msg;
    }
  };

}
