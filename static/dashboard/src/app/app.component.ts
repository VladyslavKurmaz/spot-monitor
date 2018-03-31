import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import { catchError, retry } from 'rxjs/operators';


import { hosts } from './../hosts';
import { Camera, CamerasResponse } from './models/camera'

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
  selectedCamera = null;
  selectedStream = "";

  constructor(private http: HttpClient){
    this.newCamera.ip = 'http://127.0.0.1:8008';
    this.newCamera.user = 'admin';
    this.newCamera.password = 'admin';
    this.newCamera.endpoint = 'http://127.0.0.1:8088';
    //
    this.resetSelectedCamera();
  }

  ngOnInit() {
    this.http.get<CamerasResponse>(hosts.cameraHost + '/cameras')
      .subscribe(
        cameras => {
          //
          this.cameras = cameras.data;
/*
          cameras.data.forEach(function (value) {
            let c = new Camera();
            c.ip = value.id;
            c.endpoint = value.endpoint;
            this.cameras.push(c);
          }.bind(this));
*/
        },
        error => this.handleError(error)
      );
  }

  onNewCamera() {
    this.addCamera(this.newCamera).subscribe(
      data => {
        this.addNew = false;
      }
    );
  }
  onDeleteCamera($event, cameraIndex: number, camera: Camera) {
    $event.stopPropagation();
    this.http.delete<any>(hosts.cameraHost + '/cameras/' + camera.id)
      .pipe(
      ).subscribe(
        data => {
          this.cameras.splice(cameraIndex, 1);
          if (this.selectedCamera){
            if (this.selectedCamera == camera){
              this.resetSelectedCamera();
            }
          }
        }
      );
  }
  onSelectCamera(camera: Camera){
    if (this.selectedCamera == camera){
      this.resetSelectedCamera();
    }else{
      this.selectedCamera = camera;
      this.selectedStream = this.selectedCamera.videoSource;
    }
  }
  //
  private addCamera(camera: Camera): Observable<Camera> {
    return this.http.post<Camera>(hosts.cameraHost + '/cameras', camera, httpOptions)
      .pipe(
        //catchError(this.handleError('addCamera'))
      );
  }
  //
  private resetSelectedCamera() {
    this.selectedCamera = null;
    this.selectedStream = "../assets/images/deck.jpg";
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
