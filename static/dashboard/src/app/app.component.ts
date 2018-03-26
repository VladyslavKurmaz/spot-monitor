import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import { catchError, retry } from 'rxjs/operators';


import { hosts } from './../hosts';
import { Camera } from './models/camera'

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  })
};

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  errorMessage = '';
  cameras: Camera[] = [];
  addNew: Boolean = false;
  newCamera: Camera = new Camera();

  constructor(private http: HttpClient){
    this.newCamera.ip = 'http://127.0.0.1:8008';
    this.newCamera.user = 'admin';
    this.newCamera.password = 'admin';
    this.newCamera.endpoint = 'http://127.0.0.1:8088';
  }

  ngOnInit() {
    this.http.get<any[]>(hosts.cameraHost + '/cameras')
      .subscribe(
        data => {
          //
          data.forEach(function (value) {
            let c = new Camera();
            c.ip = value.id;
            c.endpoint = value.endpoint;
            this.cameras.push(c);
          }.bind(this));
        },
        error => this.handleError(error)
      );
  }

  onNewCamera() {
    this.addCamera(this.newCamera).subscribe(
      data => {
        console.log(data);
        this.addNew = false;
      }
    );
  }
  private addCamera(camera: Camera): Observable<Camera> {
    return this.http.post<Camera>(hosts.cameraHost + '/cameras', camera, httpOptions)
      .pipe(
        //catchError(this.handleError('addCamera'))
      );
  }

  private handleError(error: HttpErrorResponse) {
    let msg = 'Unknown error';
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
      msg = error.error.message;
    } else if (error.error instanceof ProgressEvent) {
      msg = 'Request initialization error [Camera host ip | possibly CORS]'
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      msg = `Backend returned code ${error.status}, ` +
            `body was: ${error.error}`;
    }
    console.error(msg);
    this.errorMessage = msg;
  };

}
